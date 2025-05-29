"""Project preview manager for serving generated websites."""

import os
import sys
import subprocess
import time
import socket
from pathlib import Path
from typing import Dict, Any, Optional, Set
import json
import threading
import signal
import psutil


class ProjectPreviewManager:
    """Manage live preview servers for generated projects."""
    
    def __init__(self, base_port: int = 3001):
        self.base_port = base_port
        self.active_previews: Dict[str, Dict[str, Any]] = {}
        self.port_pool: Set[int] = set(range(base_port, base_port + 100))  # 100 available ports
        self.used_ports: Set[int] = set()
        
    def start_preview(self, project_id: str) -> Dict[str, Any]:
        """Start a preview server for a project."""
        try:
            # Check if preview is already running
            if project_id in self.active_previews:
                preview_info = self.active_previews[project_id]
                if self._is_server_running(preview_info['port']):
                    return {
                        'success': True,
                        'message': 'Preview already running',
                        'url': preview_info['url'],
                        'port': preview_info['port'],
                        'status': 'running'
                    }
                else:
                    # Clean up stale entry
                    self._cleanup_preview(project_id)
            
            # Check if project files exist
            project_path = Path(f"generated/projects/{project_id}/files")
            if not project_path.exists():
                return {
                    'success': False,
                    'error': 'Project files not found',
                    'status': 'error'
                }
            
            # Check if it's a valid React project
            package_json_path = project_path / "package.json"
            if not package_json_path.exists():
                return {
                    'success': False,
                    'error': 'Not a valid React project (package.json not found)',
                    'status': 'error'
                }
            
            # Allocate a port
            port = self._allocate_port()
            if not port:
                return {
                    'success': False,
                    'error': 'No available ports',
                    'status': 'error'
                }
            
            # Start the preview server
            server_result = self._start_server(project_id, project_path, port)
            
            if server_result['success']:
                preview_url = f"http://localhost:{port}"
                
                # Store preview info
                self.active_previews[project_id] = {
                    'port': port,
                    'url': preview_url,
                    'process': server_result['process'],
                    'project_path': str(project_path),
                    'started_at': time.time(),
                    'status': 'starting'
                }
                
                # Wait a moment for server to start
                time.sleep(2)
                
                # Check if server is actually running
                if self._is_server_running(port):
                    self.active_previews[project_id]['status'] = 'running'
                    return {
                        'success': True,
                        'message': 'Preview server started successfully',
                        'url': preview_url,
                        'port': port,
                        'status': 'running'
                    }
                else:
                    # Server failed to start
                    self._cleanup_preview(project_id)
                    return {
                        'success': False,
                        'error': 'Server failed to start',
                        'status': 'error'
                    }
            else:
                self._release_port(port)
                return {
                    'success': False,
                    'error': server_result['error'],
                    'status': 'error'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'status': 'error'
            }
    
    def stop_preview(self, project_id: str) -> Dict[str, Any]:
        """Stop a preview server for a project."""
        try:
            if project_id not in self.active_previews:
                return {
                    'success': False,
                    'error': 'Preview not running',
                    'status': 'stopped'
                }
            
            preview_info = self.active_previews[project_id]
            
            # Stop the server process
            try:
                process = preview_info['process']
                if process and process.poll() is None:  # Process is still running
                    # Try graceful shutdown first
                    process.terminate()
                    
                    # Wait for graceful shutdown
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        # Force kill if graceful shutdown fails
                        process.kill()
                        process.wait()
                
                # Also kill any child processes on the port
                self._kill_processes_on_port(preview_info['port'])
                
            except Exception as e:
                # Process might already be dead, that's okay
                pass
            
            # Clean up
            self._cleanup_preview(project_id)
            
            return {
                'success': True,
                'message': 'Preview server stopped',
                'status': 'stopped'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'status': 'error'
            }
    
    def get_preview_status(self, project_id: str) -> Dict[str, Any]:
        """Get the status of a preview server."""
        try:
            if project_id not in self.active_previews:
                return {
                    'success': True,
                    'status': 'stopped',
                    'running': False
                }
            
            preview_info = self.active_previews[project_id]
            port = preview_info['port']
            
            # Check if server is actually running
            is_running = self._is_server_running(port)
            
            if not is_running:
                # Server died, clean up
                self._cleanup_preview(project_id)
                return {
                    'success': True,
                    'status': 'stopped',
                    'running': False
                }
            
            return {
                'success': True,
                'status': preview_info['status'],
                'running': True,
                'url': preview_info['url'],
                'port': port,
                'started_at': preview_info['started_at'],
                'uptime': time.time() - preview_info['started_at']
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'status': 'error'
            }
    
    def get_preview_url(self, project_id: str) -> Optional[str]:
        """Get the preview URL for a project."""
        if project_id in self.active_previews:
            preview_info = self.active_previews[project_id]
            if self._is_server_running(preview_info['port']):
                return preview_info['url']
        return None
    
    def list_active_previews(self) -> Dict[str, Any]:
        """List all active preview servers."""
        active = {}
        
        # Clean up dead servers
        dead_projects = []
        for project_id, preview_info in self.active_previews.items():
            if not self._is_server_running(preview_info['port']):
                dead_projects.append(project_id)
            else:
                active[project_id] = {
                    'url': preview_info['url'],
                    'port': preview_info['port'],
                    'status': preview_info['status'],
                    'started_at': preview_info['started_at'],
                    'uptime': time.time() - preview_info['started_at']
                }
        
        # Clean up dead servers
        for project_id in dead_projects:
            self._cleanup_preview(project_id)
        
        return {
            'success': True,
            'active_previews': active,
            'total_active': len(active)
        }
    
    def cleanup_all_previews(self) -> Dict[str, Any]:
        """Stop all preview servers."""
        stopped_count = 0
        errors = []
        
        for project_id in list(self.active_previews.keys()):
            result = self.stop_preview(project_id)
            if result['success']:
                stopped_count += 1
            else:
                errors.append(f"{project_id}: {result['error']}")
        
        return {
            'success': len(errors) == 0,
            'stopped_count': stopped_count,
            'errors': errors
        }
    
    def _allocate_port(self) -> Optional[int]:
        """Allocate an available port."""
        available_ports = self.port_pool - self.used_ports
        
        for port in sorted(available_ports):
            if self._is_port_available(port):
                self.used_ports.add(port)
                return port
        
        return None
    
    def _release_port(self, port: int) -> None:
        """Release a port back to the pool."""
        self.used_ports.discard(port)
    
    def _is_port_available(self, port: int) -> bool:
        """Check if a port is available."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                result = sock.connect_ex(('localhost', port))
                return result != 0  # Port is available if connection fails
        except Exception:
            return False
    
    def _is_server_running(self, port: int) -> bool:
        """Check if a server is running on a port."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                result = sock.connect_ex(('localhost', port))
                return result == 0  # Server is running if connection succeeds
        except Exception:
            return False
    
    def _start_server(self, project_id: str, project_path: Path, port: int) -> Dict[str, Any]:
        """Start a static file server for the project."""
        try:
            # Create a simple HTTP server using Python
            # FIXED: Use current directory (.) since we set cwd to project_path
            server_script = f"""
import http.server
import socketserver
import os
import sys
from pathlib import Path

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Use current directory since we're running from project directory
        super().__init__(*args, directory='.', **kwargs)
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()
    
    def guess_type(self, path):
        # Handle React/JS files properly
        mimetype, encoding = super().guess_type(path)
        if path.endswith('.js'):
            return 'application/javascript', encoding
        elif path.endswith('.jsx'):
            return 'application/javascript', encoding
        elif path.endswith('.ts'):
            return 'application/typescript', encoding
        elif path.endswith('.tsx'):
            return 'application/typescript', encoding
        elif path.endswith('.css'):
            return 'text/css', encoding
        elif path.endswith('.json'):
            return 'application/json', encoding
        return mimetype, encoding
    
    def do_GET(self):
        # For SPA routing, serve index.html for non-file requests
        if not Path('.' + self.path).exists() and not self.path.startswith('/static'):
            self.path = '/index.html'
        return super().do_GET()

# Start server
PORT = {port}
print(f"Starting server on port {{PORT}}")
print(f"Serving from: {{os.getcwd()}}")

try:
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"Server running on http://localhost:{{PORT}}")
        httpd.serve_forever()
except Exception as e:
    print(f"Server error: {{e}}")
    import traceback
    traceback.print_exc()
"""
            
            # Write server script to temp file
            script_path = project_path / f"preview_server_{port}.py"
            with open(script_path, 'w') as f:
                f.write(server_script)
            
            # Start the server process with cwd set to project directory
            process = subprocess.Popen(
                [sys.executable, f"preview_server_{port}.py"],  # Use relative path
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(project_path)  # Set working directory to project path
            )
            
            return {
                'success': True,
                'process': process,
                'script_path': str(script_path)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _cleanup_preview(self, project_id: str) -> None:
        """Clean up preview resources."""
        if project_id in self.active_previews:
            preview_info = self.active_previews[project_id]
            
            # Release port
            self._release_port(preview_info['port'])
            
            # Clean up server script
            try:
                script_path = Path(preview_info['project_path']) / f"preview_server_{preview_info['port']}.py"
                if script_path.exists():
                    script_path.unlink()
            except Exception:
                pass
            
            # Remove from active previews
            del self.active_previews[project_id]
    
    def _kill_processes_on_port(self, port: int) -> None:
        """Kill any processes running on a specific port."""
        try:
            for proc in psutil.process_iter(['pid', 'name', 'connections']):
                try:
                    connections = proc.info['connections']
                    if connections:
                        for conn in connections:
                            if conn.laddr.port == port:
                                proc.kill()
                                break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        except Exception:
            pass


# Global preview manager instance
preview_manager = ProjectPreviewManager()
