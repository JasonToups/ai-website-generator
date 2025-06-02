"""Debug the preview server startup process."""

import sys
import subprocess
import time
from pathlib import Path
sys.path.append('backend')

from backend.utils.project_preview import preview_manager

def debug_preview_server():
    """Debug the preview server startup."""
    
    project_id = 'b216ae3e-94ac-49b3-a986-21ee86ecb56f'
    project_path = Path(f"generated/projects/{project_id}/files")
    
    print('🔍 Debugging Preview Server Startup')
    print('=' * 50)
    
    # Check if project path exists
    print(f'📁 Project path: {project_path}')
    print(f'   Exists: {project_path.exists()}')
    
    if project_path.exists():
        print(f'   Contents:')
        for item in project_path.iterdir():
            print(f'     - {item.name}')
    
    # Check package.json
    package_json = project_path / "package.json"
    print(f'\n📦 Package.json: {package_json.exists()}')
    
    # Try to manually start a simple server
    print('\n🧪 Testing manual server startup...')
    
    # Create a simple test server script
    test_port = 3001
    server_script = f"""
import http.server
import socketserver
import os
import sys
from pathlib import Path

print("Starting test server...")
print(f"Working directory: {{os.getcwd()}}")
print(f"Serving from: {project_path}")

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory='{project_path}', **kwargs)
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

PORT = {test_port}
try:
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"Server running on http://localhost:{{PORT}}")
        httpd.serve_forever()
except Exception as e:
    print(f"Server error: {{e}}")
    import traceback
    traceback.print_exc()
"""
    
    # Write test script
    script_path = project_path / "debug_server.py"
    with open(script_path, 'w') as f:
        f.write(server_script)
    
    print(f'   Created debug server script: {script_path}')
    
    # Try to run the server
    print('   Starting debug server...')
    try:
        process = subprocess.Popen(
            [sys.executable, str(script_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(project_path),
            text=True
        )
        
        # Wait a moment and check output
        time.sleep(2)
        
        # Check if process is still running
        if process.poll() is None:
            print('   ✅ Debug server started successfully!')
            print(f'   🌐 Test URL: http://localhost:{test_port}')
            
            # Kill the process
            process.terminate()
            process.wait()
            print('   🛑 Debug server stopped')
        else:
            # Process died, get error output
            stdout, stderr = process.communicate()
            print('   ❌ Debug server failed to start')
            print(f'   STDOUT: {stdout}')
            print(f'   STDERR: {stderr}')
            
    except Exception as e:
        print(f'   ❌ Exception starting debug server: {e}')
    
    # Clean up
    if script_path.exists():
        script_path.unlink()
        print('   🧹 Cleaned up debug script')

if __name__ == "__main__":
    debug_preview_server()
