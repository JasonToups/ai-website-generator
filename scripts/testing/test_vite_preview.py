#!/usr/bin/env python3
"""
Test the updated Vite preview system

This script tests the new Vite-aware preview system with the shopping list project.
"""

import sys
import time
from pathlib import Path

# Add the backend directory to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent / "backend"))

from utils.project_preview import ProjectPreviewManager

def test_vite_preview():
    """Test the Vite preview system."""
    print("🚀 Testing Vite Preview System\n")
    
    project_id = '9ab87061-070a-43b2-b967-b58d734706ad'
    
    # Initialize preview manager
    preview_manager = ProjectPreviewManager()
    
    print(f"📋 Testing project: {project_id}")
    
    # Check if it's detected as a Vite project
    project_path = Path(f"generated/projects/{project_id}/files")
    is_vite = preview_manager._is_vite_project(project_path)
    print(f"🔍 Vite project detected: {is_vite}")
    
    if not is_vite:
        print("❌ Project not detected as Vite project")
        return False
    
    # Start preview
    print("🎬 Starting preview server...")
    result = preview_manager.start_preview(project_id)
    
    if result['success']:
        print(f"✅ Preview started successfully!")
        print(f"   URL: {result['url']}")
        print(f"   Port: {result['port']}")
        print(f"   Status: {result['status']}")
        
        # Wait a bit for Vite to fully start
        print("⏳ Waiting for Vite server to fully start...")
        time.sleep(10)
        
        # Check status
        status = preview_manager.get_preview_status(project_id)
        print(f"📊 Current status: {status}")
        
        # Get preview URL
        url = preview_manager.get_preview_url(project_id)
        if url:
            print(f"🌐 Preview URL: {url}")
            print("💡 You can now open this URL in your browser to see the shopping list app!")
            
            # Keep server running for manual testing
            print("\n🔄 Server is running. Press Ctrl+C to stop...")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Stopping server...")
                
                # Stop preview
                stop_result = preview_manager.stop_preview(project_id)
                if stop_result['success']:
                    print("✅ Preview stopped successfully")
                else:
                    print(f"❌ Error stopping preview: {stop_result['error']}")
        else:
            print("❌ Could not get preview URL")
            return False
        
        return True
    else:
        print(f"❌ Failed to start preview: {result['error']}")
        return False

def main():
    """Test the Vite preview system."""
    try:
        success = test_vite_preview()
        return success
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
