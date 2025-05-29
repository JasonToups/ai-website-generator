# File Parsing Implementation Plan

## 🎯 Project Overview

**Goal**: Transform the AI Website Generator from outputting single text files to creating proper project structures with individual files that users can download and use immediately.

**Current State**: Generated websites are saved as single `crew_output.txt` files containing all code in a structured text format.

**Target State**: Each generated project should have:

- Individual React component files (`.tsx`)
- Configuration files (`package.json`, `README.md`, etc.)
- Proper folder structure (`src/`, `src/components/`, etc.)
- Downloadable ZIP archive of complete project

## 📋 Current Format Analysis

Based on analysis of `generated/projects/9e5c696f-96e4-445a-8bd9-a909b0b37a33/crew_output.txt`:

### Current Structure Pattern:

````
Here's the complete implementation of the [Project Name]:

1. src/App.tsx

```tsx
[React component code]
````

2. src/components/Navbar.tsx

```tsx
[React component code]
```

3. src/components/Hero.tsx
   ...

4. package.json

```json
[package.json content]
```

8. README.md

```markdown
[README content]
```

````

### Parsing Challenges Identified:
1. **File Identification**: Files are numbered (1., 2., 3., etc.) with paths
2. **Code Block Extraction**: Code is wrapped in triple backticks with language identifiers
3. **Multiple File Types**: `.tsx`, `.json`, `.md` files with different syntax
4. **Nested Folder Structure**: Files are in `src/`, `src/components/`, etc.
5. **Content Validation**: Need to ensure extracted code is syntactically valid

## 🏗️ Implementation Architecture

### Phase 1: Backend File Parser Module

#### 1.1 Create File Parser (`backend/utils/file_parser.py`)

```python
class ProjectFileParser:
    """Parse crew output text into individual project files."""

    def __init__(self, crew_output: str):
        self.crew_output = crew_output
        self.files = {}
        self.project_structure = {}

    def parse(self) -> Dict[str, Any]:
        """Main parsing method."""
        # 1. Extract file blocks
        # 2. Parse each file
        # 3. Validate content
        # 4. Create project structure
        # 5. Return parsed data

    def extract_file_blocks(self) -> List[Dict]:
        """Extract numbered file blocks from text."""
        # Regex pattern: r'(\d+)\.\s+([^\n]+)\n\n```(\w+)\n(.*?)\n```'

    def parse_file_content(self, file_block: Dict) -> Dict:
        """Parse individual file content and metadata."""
        # Extract file path, extension, content
        # Validate syntax for different file types

    def create_project_structure(self) -> Dict:
        """Create proper folder structure."""
        # Organize files into folders
        # Create directory tree

    def validate_content(self, content: str, file_type: str) -> bool:
        """Validate file content syntax."""
        # TypeScript/TSX validation
        # JSON validation
        # Markdown validation
````

#### 1.2 File Structure Creation (`backend/utils/project_structure.py`)

```python
class ProjectStructureManager:
    """Manage project folder structure and file creation."""

    def create_project_folder(self, project_id: str, parsed_files: Dict):
        """Create physical folder structure with files."""
        # Create base project directory
        # Create subdirectories (src/, src/components/, etc.)
        # Write individual files
        # Generate file manifest

    def create_zip_archive(self, project_id: str) -> str:
        """Create downloadable ZIP archive."""
        # Zip entire project folder
        # Return path to ZIP file

    def get_file_tree(self, project_id: str) -> Dict:
        """Get project file tree for frontend display."""
        # Return hierarchical file structure
```

### Phase 2: API Enhancements

#### 2.1 New Endpoints

```python
# In backend/api/routes.py

@app.get("/api/v1/projects/{project_id}/files/tree")
async def get_project_file_tree(project_id: str):
    """Get hierarchical file structure."""
    # Return file tree with metadata

@app.get("/api/v1/projects/{project_id}/files/{file_path:path}")
async def get_individual_file(project_id: str, file_path: str):
    """Get individual file content."""
    # Return specific file content with metadata

@app.get("/api/v1/projects/{project_id}/download")
async def download_project_zip(project_id: str):
    """Download complete project as ZIP."""
    # Return ZIP file for download

@app.get("/api/v1/projects/{project_id}/files/preview")
async def preview_project_files(project_id: str):
    """Get all files for preview (limited content)."""
    # Return truncated file contents for preview
```

#### 2.2 Enhanced Project Generation Flow

```python
# Modified generation process
async def generate_website(request: WebsiteRequest):
    # 1. Run CrewAI crew (existing)
    # 2. Parse crew output into files (NEW)
    # 3. Create project structure (NEW)
    # 4. Update project status with file info (ENHANCED)
    # 5. Generate ZIP archive (NEW)
```

### Phase 3: Frontend Enhancements

#### 3.1 File Browser Component (`frontend/src/components/FileBrowser.tsx`)

```typescript
interface FileNode {
  name: string;
  type: 'file' | 'folder';
  path: string;
  size?: number;
  extension?: string;
  children?: FileNode[];
}

const FileBrowser: React.FC<{
  projectId: string;
  files: FileNode[];
}> = ({ projectId, files }) => {
  // Tree view of project files
  // Click to preview individual files
  // Download individual files
  // Download complete project
};
```

#### 3.2 File Preview Component (`frontend/src/components/FilePreview.tsx`)

```typescript
const FilePreview: React.FC<{
  file: FileNode;
  content: string;
}> = ({ file, content }) => {
  // Syntax highlighting based on file type
  // Copy to clipboard functionality
  // Download individual file
};
```

#### 3.3 Enhanced Project View

```typescript
const ProjectView: React.FC = () => {
  // Tabs: Overview | Files | Preview | Download
  // File browser integration
  // Download options (individual files, ZIP)
  // Live preview iframe (future enhancement)
};
```

## 🔧 Technical Implementation Details

### File Parsing Algorithm

````python
def parse_crew_output(text: str) -> Dict[str, Any]:
    """
    Parse crew output using regex patterns:

    1. Main pattern: r'(\d+)\.\s+([^\n]+)\n\n```(\w+)\n(.*?)\n```'
       - Group 1: File number
       - Group 2: File path
       - Group 3: Language/type
       - Group 4: File content

    2. Extract and validate each file
    3. Create folder structure
    4. Return structured data
    """
````

### File Validation

```python
def validate_file_content(content: str, file_type: str) -> bool:
    """
    Validate different file types:

    - .tsx/.ts: TypeScript syntax validation
    - .json: JSON parsing validation
    - .md: Markdown structure validation
    - .css: CSS syntax validation
    """
```

### Project Structure

```
generated/projects/{project_id}/
├── crew_output.txt          # Original output (keep for reference)
├── parsed_files.json        # File metadata and structure
├── project.zip             # Downloadable archive
└── files/                  # Individual project files
    ├── src/
    │   ├── App.tsx
    │   ├── main.tsx
    │   └── components/
    │       ├── Navbar.tsx
    │       ├── Hero.tsx
    │       └── Footer.tsx
    ├── package.json
    ├── README.md
    ├── tailwind.config.js
    └── tsconfig.json
```

## 📊 Database Schema Updates

### Enhanced Project Model

```python
class Project(BaseModel):
    # Existing fields...
    files_parsed: bool = False
    file_count: int = 0
    project_structure: Dict[str, Any] = {}
    zip_file_path: Optional[str] = None
    parsing_errors: List[str] = []
```

## 🎯 Implementation Timeline

### Phase 1: Core Parser (Week 1)

- [ ] Create `file_parser.py` module
- [ ] Implement regex-based file extraction
- [ ] Add content validation
- [ ] Create unit tests

### Phase 2: Project Structure (Week 1)

- [ ] Create `project_structure.py` module
- [ ] Implement folder creation
- [ ] Add ZIP archive generation
- [ ] Integrate with existing project flow

### Phase 3: API Integration (Week 2)

- [ ] Add new API endpoints
- [ ] Enhance existing endpoints
- [ ] Update project generation flow
- [ ] Add error handling

### Phase 4: Frontend Components (Week 2)

- [ ] Create FileBrowser component
- [ ] Create FilePreview component
- [ ] Add syntax highlighting
- [ ] Integrate download functionality

### Phase 5: Testing & Polish (Week 3)

- [ ] End-to-end testing
- [ ] Error handling improvements
- [ ] Performance optimization
- [ ] Documentation updates

## 🧪 Testing Strategy

### Unit Tests

- File parsing accuracy
- Content validation
- Project structure creation
- ZIP archive generation

### Integration Tests

- API endpoint functionality
- Frontend-backend communication
- File download workflows
- Error handling scenarios

### End-to-End Tests

- Complete project generation and parsing
- File browser functionality
- Download and extraction verification

## 🚀 Success Metrics

### Technical Metrics

- **Parsing Accuracy**: 100% of generated files correctly extracted
- **File Validation**: 95%+ of extracted files syntactically valid
- **Performance**: Parsing completes within 5 seconds
- **Reliability**: 99%+ success rate for file extraction

### User Experience Metrics

- **Download Success**: 100% of ZIP files downloadable and extractable
- **File Preview**: All file types properly displayed with syntax highlighting
- **Navigation**: Intuitive file browser with folder structure
- **Usability**: One-click download for individual files and complete projects

## 🔄 Future Enhancements

### Phase 2 Features (Post-MVP)

- **Live Preview**: In-browser preview of generated websites
- **File Editing**: Basic in-browser file editing capabilities
- **Version Control**: Track changes and iterations
- **Template Library**: Save successful projects as templates

### Advanced Features

- **Deployment Integration**: One-click deploy to Vercel/Netlify
- **Collaboration**: Share projects with team members
- **Analytics**: Track file usage and popular components
- **AI Assistance**: AI-powered code suggestions and improvements

## 📝 Documentation Requirements

### Technical Documentation

- API endpoint specifications
- File parsing algorithm documentation
- Frontend component documentation
- Database schema updates

### User Documentation

- File browser usage guide
- Download and setup instructions
- Troubleshooting guide
- FAQ for common issues

## 🎉 Expected Impact

### For Users

- **Immediate Usability**: Download and run generated projects instantly
- **Professional Workflow**: Proper project structure matches industry standards
- **Development Ready**: Projects ready for further development and customization
- **Learning Tool**: Users can study generated code structure and patterns

### For System

- **Enhanced Value Proposition**: Complete, usable projects vs. text output
- **Improved User Retention**: Users more likely to return for additional projects
- **Scalability**: Foundation for advanced features like live preview and deployment
- **Quality Assurance**: File validation ensures higher quality output

---

_This implementation plan provides a comprehensive roadmap for transforming the AI Website Generator into a professional-grade tool that delivers complete, usable projects to users._
