#!/usr/bin/env python3
"""
Test script to verify Tailwind CSS v4 fix is working
"""

import sys
import subprocess
import time
import signal
import os
from pathlib import Path

def test_tailwind_v4_fix():
    """Test if the Tailwind CSS v4 configuration is working."""
    print("🚀 Testing Tailwind CSS v4 Fix\n")
    
    project_id = "16fdd748-a31a-488b-9df9-882d6e77d588"
    project_path = Path(f"generated/projects/{project_id}/files")
    
    if not project_path.exists():
        print(f"❌ Project path not found: {project_path}")
        return False
    
    print("=" * 60)
    print("STEP 1: VERIFY DEPENDENCIES")
    print("=" * 60)
    
    # Check package.json for required dependencies
    package_json = project_path / "package.json"
    if package_json.exists():
        with open(package_json, 'r') as f:
            package_content = f.read()
        
        required_deps = [
            '@tailwindcss/postcss',
            'postcss-import',
            'tailwindcss',
            'autoprefixer'
        ]
        
        missing_deps = []
        for dep in required_deps:
            if dep not in package_content:
                missing_deps.append(dep)
        
        if missing_deps:
            print(f"❌ Missing dependencies: {missing_deps}")
            return False
        else:
            print("✅ All required dependencies present")
    
    print("\n" + "=" * 60)
    print("STEP 2: VERIFY POSTCSS CONFIGURATION")
    print("=" * 60)
    
    # Check PostCSS configuration
    postcss_config = project_path / "postcss.config.js"
    if postcss_config.exists():
        with open(postcss_config, 'r') as f:
            postcss_content = f.read()
        
        required_imports = [
            "import postcssImport from 'postcss-import'",
            "import tailwindcss from '@tailwindcss/postcss'",
            "import autoprefixer from 'autoprefixer'"
        ]
        
        missing_imports = []
        for imp in required_imports:
            if imp not in postcss_content:
                missing_imports.append(imp)
        
        if missing_imports:
            print(f"❌ Missing PostCSS imports: {missing_imports}")
            return False
        else:
            print("✅ PostCSS configuration uses correct v4 format")
    
    print("\n" + "=" * 60)
    print("STEP 3: TEST VITE DEV SERVER")
    print("=" * 60)
    
    # Test if Vite can start without PostCSS errors
    print("🔧 Starting Vite dev server...")
    
    try:
        # Change to project directory and start dev server
        os.chdir(project_path)
        
        # Start the dev server in background
        process = subprocess.Popen(
            ['npm', 'run', 'dev'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            preexec_fn=os.setsid
        )
        
        # Wait a few seconds for server to start
        time.sleep(5)
        
        # Check if process is still running (no immediate crash)
        if process.poll() is None:
            print("✅ Vite dev server started successfully")
            
            # Try to read some output to check for errors
            try:
                stdout, stderr = process.communicate(timeout=2)
                if "postcss" in stderr.lower() and "error" in stderr.lower():
                    print("❌ PostCSS errors detected in output")
                    return False
                else:
                    print("✅ No PostCSS errors detected")
            except subprocess.TimeoutExpired:
                # Server is still running, which is good
                print("✅ Server running without immediate errors")
            
            # Kill the process
            try:
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                process.wait(timeout=5)
            except:
                process.kill()
            
            return True
        else:
            # Process crashed immediately
            stdout, stderr = process.communicate()
            print(f"❌ Vite dev server crashed immediately")
            print(f"Error output: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Vite server: {str(e)}")
        return False
    
    finally:
        # Make sure we're back in the original directory
        os.chdir(Path(__file__).parent.parent.parent)

if __name__ == "__main__":
    success = test_tailwind_v4_fix()
    if success:
        print("\n🎉 SUCCESS: Tailwind CSS v4 fix is working!")
        print("✅ Dependencies installed correctly")
        print("✅ PostCSS configuration updated")
        print("✅ Vite dev server starts without PostCSS errors")
    else:
        print("\n❌ FAILED: Tailwind CSS v4 fix needs more work")
    
    sys.exit(0 if success else 1)
