"""Quick check if the preview server is running."""

import requests
import sys
sys.path.append('backend')

from backend.utils.project_preview import preview_manager

def check_preview():
    """Check if the preview is running and accessible."""
    
    project_id = 'b216ae3e-94ac-49b3-a986-21ee86ecb56f'
    
    print('🔍 Checking PhotoLens Portfolio Preview Status...')
    print('=' * 50)
    
    # Check preview status
    status = preview_manager.get_preview_status(project_id)
    
    if status['success'] and status.get('running'):
        url = status['url']
        port = status['port']
        uptime = status.get('uptime', 0)
        
        print(f'✅ Preview server is RUNNING!')
        print(f'📍 URL: {url}')
        print(f'🔌 Port: {port}')
        print(f'⏱️  Uptime: {uptime:.1f} seconds')
        
        # Test HTTP access
        print('\n🌐 Testing website access...')
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f'✅ Website is accessible!')
                print(f'📄 Content length: {len(response.text)} bytes')
                
                # Check for PhotoLens content
                content = response.text
                if 'PhotoLens' in content:
                    print('✅ PhotoLens branding found!')
                if 'Capturing moments' in content:
                    print('✅ Hero section content found!')
                if 'About the Photographer' in content:
                    print('✅ About section found!')
                if 'Photo Gallery' in content:
                    print('✅ Gallery section found!')
                    
                print('\n🎉 SUCCESS! PhotoLens Portfolio is live and accessible!')
                print(f'🌐 Visit: {url}')
                
            else:
                print(f'❌ Website returned status: {response.status_code}')
                
        except requests.exceptions.RequestException as e:
            print(f'❌ Failed to access website: {str(e)}')
            
    else:
        print('❌ Preview server is not running')
        print('   Starting preview server...')
        
        # Try to start it
        start_result = preview_manager.start_preview(project_id)
        if start_result['success']:
            print(f'✅ Preview started! URL: {start_result["url"]}')
        else:
            print(f'❌ Failed to start: {start_result.get("error")}')

if __name__ == "__main__":
    check_preview()
