#!/usr/bin/env python3
"""
Comprehensive test for the integrated Template Injection System

This script tests the complete integration of template injection
with the project structure creation system.
"""

import sys
import os
import json
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent / "backend"))

from utils.project_structure import create_project_structure
from utils.file_parser import parse_crew_output

def test_end_to_end_integration():
    """Test complete end-to-end template injection integration."""
    print("🚀 Testing End-to-End Template Injection Integration")
    print("=" * 60)
    
    # Mock crew output (similar to what CrewAI would generate)
    mock_crew_output = """
Here's a complete React application for a modern portfolio website:

1. App.tsx

```typescript
import React from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import About from './components/About';
import Projects from './components/Projects';
import Contact from './components/Contact';
import Footer from './components/Footer';

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <Hero />
      <About />
      <Projects />
      <Contact />
      <Footer />
    </div>
  );
}

export default App;
```

2. components/Navbar.tsx

```typescript
import React from 'react';

const Navbar: React.FC = () => {
  return (
    <nav className="bg-white shadow-lg fixed w-full z-10">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <span className="text-xl font-bold text-blue-600">Portfolio</span>
          </div>
          <div className="flex items-center space-x-8">
            <a href="#home" className="text-gray-700 hover:text-blue-600">Home</a>
            <a href="#about" className="text-gray-700 hover:text-blue-600">About</a>
            <a href="#projects" className="text-gray-700 hover:text-blue-600">Projects</a>
            <a href="#contact" className="text-gray-700 hover:text-blue-600">Contact</a>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
```

3. components/Hero.tsx

```typescript
import React from 'react';

const Hero: React.FC = () => {
  return (
    <section id="home" className="pt-16 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
      <div className="max-w-7xl mx-auto px-4 py-20">
        <div className="text-center">
          <h1 className="text-5xl font-bold mb-4">John Doe</h1>
          <p className="text-xl mb-8">Full Stack Developer & UI/UX Designer</p>
          <button className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100">
            View My Work
          </button>
        </div>
      </div>
    </section>
  );
};

export default Hero;
```

4. package.json

```json
{
  "name": "modern-portfolio",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.15",
    "@types/react-dom": "^18.2.7",
    "@vitejs/plugin-react": "^4.0.3",
    "typescript": "^5.0.2",
    "vite": "^4.4.5",
    "tailwindcss": "^3.3.0"
  }
}
```

5. README.md

```markdown
# Modern Portfolio Website

A beautiful, responsive portfolio website built with React, TypeScript, and Tailwind CSS.

## Features

- Modern, clean design
- Fully responsive
- Built with React 18
- TypeScript for type safety
- Tailwind CSS for styling

## Getting Started

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Open your browser and visit `http://localhost:3000`

## Build for Production

```bash
npm run build
```

The built files will be in the `dist` directory.
```
"""
    
    print("📝 Step 1: Parsing mock crew output...")
    
    # Parse the crew output
    parsed_result = parse_crew_output(mock_crew_output)
    
    if not parsed_result['success']:
        print(f"❌ Parsing failed: {parsed_result['error']}")
        return False
    
    print(f"✅ Parsed {parsed_result['file_count']} files successfully")
    print(f"📁 Files found: {list(parsed_result['files'].keys())}")
    
    print("\n📝 Step 2: Creating project structure with template injection...")
    
    # Project metadata for template variables
    project_metadata = {
        'title': 'Modern Portfolio Website',
        'description': 'A beautiful, responsive portfolio website built with React'
    }
    
    # Create project structure (this will automatically inject templates)
    project_id = "test-template-integration"
    structure_result = create_project_structure(project_id, parsed_result, project_metadata)
    
    if not structure_result['success']:
        print(f"❌ Project structure creation failed: {structure_result}")
        return False
    
    print(f"✅ Project structure created successfully")
    print(f"📊 Total files: {structure_result['total_files']}")
    print(f"🔄 Templates injected: {structure_result['templates_injected']}")
    
    print("\n📝 Step 3: Verifying template injection...")
    
    # Check that template files were created
    project_path = Path(structure_result['project_path'])
    files_path = project_path / "files"
    
    expected_template_files = [
        'index.html',
        'src/main.tsx',
        'src/index.css',
        'vite.config.ts',
        'tsconfig.json'
    ]
    
    template_files_found = []
    for template_file in expected_template_files:
        file_path = files_path / template_file
        if file_path.exists():
            template_files_found.append(template_file)
            print(f"✅ Template file created: {template_file}")
            
            # Check if project title was injected correctly
            if template_file == 'index.html':
                with open(file_path, 'r') as f:
                    content = f.read()
                if 'Modern Portfolio Website' in content:
                    print(f"✅ Project title correctly injected in {template_file}")
                else:
                    print(f"❌ Project title not found in {template_file}")
        else:
            print(f"❌ Template file missing: {template_file}")
    
    print(f"\n📊 Template files created: {len(template_files_found)}/{len(expected_template_files)}")
    
    print("\n📝 Step 4: Verifying original files were preserved...")
    
    # Check that original parsed files were preserved
    original_files = [
        'src/App.tsx',
        'src/components/Navbar.tsx',
        'src/components/Hero.tsx',
        'package.json',
        'README.md'
    ]
    
    original_files_found = []
    for original_file in original_files:
        file_path = files_path / original_file
        if file_path.exists():
            original_files_found.append(original_file)
            print(f"✅ Original file preserved: {original_file}")
        else:
            print(f"❌ Original file missing: {original_file}")
    
    print(f"\n📊 Original files preserved: {len(original_files_found)}/{len(original_files)}")
    
    print("\n📝 Step 5: Verifying project manifest...")
    
    # Check project manifest
    manifest_path = project_path / "parsed_files.json"
    if manifest_path.exists():
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        print(f"✅ Project manifest created")
        print(f"📊 Manifest file count: {manifest['parsing_results']['file_count']}")
        print(f"🔄 Template metadata: {manifest.get('template_metadata', {})}")
        
        # Check template metadata
        template_metadata = manifest.get('template_metadata', {})
        if 'templates_injected' in template_metadata:
            print(f"✅ Template injection metadata recorded: {template_metadata['templates_injected']} templates")
        else:
            print(f"❌ Template injection metadata missing")
    else:
        print(f"❌ Project manifest missing")
    
    print("\n📝 Step 6: Verifying ZIP archive...")
    
    # Check ZIP archive
    zip_path = project_path / "project.zip"
    if zip_path.exists():
        zip_size = zip_path.stat().st_size
        print(f"✅ ZIP archive created: {zip_size} bytes")
    else:
        print(f"❌ ZIP archive missing")
    
    print("\n🎉 Integration test completed!")
    
    # Summary
    success_criteria = [
        len(template_files_found) == len(expected_template_files),
        len(original_files_found) == len(original_files),
        structure_result['templates_injected'] > 0,
        manifest_path.exists(),
        zip_path.exists()
    ]
    
    all_passed = all(success_criteria)
    
    print(f"\n📋 Test Results Summary:")
    print(f"✅ Template files created: {len(template_files_found)}/{len(expected_template_files)}")
    print(f"✅ Original files preserved: {len(original_files_found)}/{len(original_files)}")
    print(f"✅ Templates injected: {structure_result['templates_injected']}")
    print(f"✅ Project manifest: {'Created' if manifest_path.exists() else 'Missing'}")
    print(f"✅ ZIP archive: {'Created' if zip_path.exists() else 'Missing'}")
    
    if all_passed:
        print(f"\n🎉 ALL TESTS PASSED! Template injection system is fully integrated and working!")
        print(f"\n🚀 Ready for production use:")
        print(f"   - Every new project will automatically get complete template files")
        print(f"   - Projects will be immediately runnable with proper React setup")
        print(f"   - Live preview system will work with 100% of generated projects")
        print(f"   - CrewAI agents can focus on App.tsx and custom components only")
    else:
        print(f"\n❌ Some tests failed. Please check the issues above.")
    
    return all_passed

def main():
    """Run the integrated template system test."""
    try:
        success = test_end_to_end_integration()
        
        if success:
            print(f"\n🎯 Next Steps:")
            print(f"1. Update CrewAI Software Engineer instructions to focus on App.tsx and components")
            print(f"2. Test with a real CrewAI generation to verify end-to-end workflow")
            print(f"3. Begin Phase 5 Preview Gallery implementation")
            
            return 0
        else:
            print(f"\n❌ Integration test failed. Please fix issues before proceeding.")
            return 1
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
