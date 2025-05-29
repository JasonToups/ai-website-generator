# Phase 3: API Integration Implementation Plan

## 🎯 Overview

**Goal**: Connect our file parsing modules (Phases 1 & 2) with the existing API to provide file downloads, ZIP archives, and full live preview capability.

**Status**: Ready to implement (Phases 1 & 2 complete)
**Timeline**: Week 2 of file parsing implementation
**Priority**: High - Foundation for live preview feature

## 📋 Implementation Scope

### **Primary Objectives:**

1. **API Integration**: Connect file parsing modules with existing endpoints
2. **New Endpoints**: Add 4 new file operation endpoints
3. **Enhanced Generation**: Automatic parsing in project generation flow
4. **Preview Foundation**: Infrastructure for full live website preview

### **User Experience Goals:**

- Download individual files from generated projects
- Download complete projects as ZIP archives
- View file tree structure in browser
- **Preview full, interactive websites** (foundation for Phase 4)

## 🛠️ Technical Implementation

### **4 New API Endpoints:**

#### **1. `GET /api/v1/projects/{id}/files/tree`**

**Purpose**: Return hierarchical file structure for frontend display

**Implementation**:

```python
@router.get("/projects/{project_id}/files/tree")
async def get_project_file_tree(project_id: str):
    manager = ProjectStructureManager(project_id)
    result = manager.get_file_tree()
    return result
```

**Response Format**:

```json
{
  "success": true,
  "tree": {
    "name": "project-{id}",
    "type": "folder",
    "children": [
      {
        "name": "src",
        "type": "folder",
        "children": [...]
      }
    ]
  },
  "total_files": 8,
  "total_size": 12246
}
```

#### **2. `GET /api/v1/projects/{id}/files/{path:path}`**

**Purpose**: Return individual file content with metadata

**Implementation**:

```python
@router.get("/projects/{project_id}/files/{file_path:path}")
async def get_project_file(project_id: str, file_path: str):
    manager = ProjectStructureManager(project_id)
    result = manager.get_individual_file(file_path)
    return result
```

**Response Format**:

```json
{
  "success": true,
  "path": "src/App.tsx",
  "name": "App.tsx",
  "extension": ".tsx",
  "content": "import React from 'react'...",
  "size": 1423,
  "modified_time": 1640995200.0
}
```

#### **3. `GET /api/v1/projects/{id}/download`**

**Purpose**: Return ZIP file for download

**Implementation**:

```python
@router.get("/projects/{project_id}/download")
async def download_project_zip(project_id: str):
    manager = ProjectStructureManager(project_id)
    zip_path = manager.project_path / "project.zip"

    if not zip_path.exists():
        # Generate ZIP if it doesn't exist
        zip_result = manager.create_zip_archive()
        if not zip_result['success']:
            raise HTTPException(status_code=404, detail="ZIP generation failed")

    return FileResponse(
        path=str(zip_path),
        filename=f"project-{project_id}.zip",
        media_type="application/zip"
    )
```

#### **4. `GET /api/v1/projects/{id}/preview`**

**Purpose**: Serve full, live website preview

**Implementation**:

```python
@router.get("/projects/{project_id}/preview")
async def get_project_preview(project_id: str):
    manager = ProjectStructureManager(project_id)
    preview_manager = ProjectPreviewManager(project_id)

    # Build and serve the project
    result = await preview_manager.start_preview()
    return result
```

**Response Format**:

```json
{
  "success": true,
  "preview_url": "http://localhost:3001",
  "status": "building|ready|error",
  "build_logs": ["Installing dependencies...", "Starting dev server..."],
  "port": 3001
}
```

### **Enhanced Generation Flow:**

#### **Current Flow:**

```
Generate → Save crew_output.txt → Return status
```

#### **New Enhanced Flow:**

```
Generate → Save crew_output.txt → Parse files → Create structure → Generate ZIP → Return enhanced status
```

#### **Implementation in `/api/v1/generate`:**

```python
# After crew execution completes:
if crew_result.success:
    # Existing: Save crew output
    save_crew_output(project_id, crew_result.output)

    # NEW: Parse files and create structure
    parser = ProjectFileParser(crew_result.output, project_id)
    parsed_result = parser.parse()

    if parsed_result['success']:
        # Create project structure
        structure_result = create_project_structure(project_id, parsed_result)

        # Update project status with file metadata
        update_project_with_files(project_id, structure_result)
```

### **Enhanced Status Endpoint:**

#### **Current `/api/v1/projects/{id}/status`:**

```json
{
  "id": "project-id",
  "status": "completed",
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### **Enhanced Status Response:**

```json
{
  "id": "project-id",
  "status": "completed",
  "created_at": "2024-01-01T00:00:00Z",
  "files": {
    "parsed": true,
    "file_count": 8,
    "has_zip": true,
    "zip_size": 5876,
    "structure_created": true,
    "preview_available": true
  }
}
```

## 🏗️ New Infrastructure Components

### **ProjectPreviewManager Class:**

```python
class ProjectPreviewManager:
    """Manage live preview of generated projects."""

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.files_path = Path(f"generated/projects/{project_id}/files")
        self.port = self._get_available_port()

    async def start_preview(self):
        """Build and serve the project for live preview."""
        # 1. Install dependencies (npm install)
        # 2. Start dev server (npm start)
        # 3. Return preview URL

    def stop_preview(self):
        """Stop the preview server."""

    def get_preview_status(self):
        """Get current preview status."""
```

### **Port Management:**

- Dynamic port allocation (3001, 3002, 3003, etc.)
- Port cleanup when previews are stopped
- Conflict resolution for multiple previews

### **Build System Integration:**

- Execute `npm install` in project directory
- Start `npm start` on allocated port
- Capture build logs and errors
- Health check for preview readiness

## 📊 Database Schema Updates

### **Enhanced Project Model:**

```json
{
  "id": "project-id",
  "status": "completed",
  "created_at": "2024-01-01T00:00:00Z",
  "crew_output": "...",

  // NEW: File parsing metadata
  "files": {
    "parsed": true,
    "parse_timestamp": "2024-01-01T00:05:00Z",
    "file_count": 8,
    "parsing_errors": [],
    "structure_created": true,
    "zip_generated": true,
    "zip_size": 5876
  },

  // NEW: Preview metadata
  "preview": {
    "available": true,
    "port": 3001,
    "status": "ready|building|stopped|error",
    "last_started": "2024-01-01T00:10:00Z"
  }
}
```

## 🧪 Testing Strategy

### **Unit Tests:**

- Test each new endpoint with mock data
- Validate file parsing integration
- Test error scenarios (missing files, parsing failures)

### **Integration Tests:**

- End-to-end project generation with file parsing
- ZIP download functionality
- Preview server startup and shutdown

### **Test Data:**

- Use existing project `9e5c696f-96e4-445a-8bd9-a909b0b37a33` for testing
- Validate with multiple project types (different file counts)

## 🚀 Implementation Order

### **Step 1: Basic File Endpoints (Day 1)**

1. Implement file tree endpoint
2. Implement individual file endpoint
3. Test with existing parsed project

### **Step 2: ZIP Download (Day 1)**

1. Implement ZIP download endpoint
2. Add FileResponse handling
3. Test download functionality

### **Step 3: Enhanced Generation Flow (Day 2)**

1. Modify generate endpoint to include parsing
2. Update status endpoint with file metadata
3. Test complete generation workflow

### **Step 4: Preview Infrastructure (Day 2-3)**

1. Create ProjectPreviewManager class
2. Implement preview endpoint
3. Add port management and build system
4. Test live preview functionality

### **Step 5: Error Handling & Polish (Day 3)**

1. Add comprehensive error handling
2. Improve status tracking
3. Add cleanup mechanisms
4. Performance optimization

## 📈 Success Metrics

### **Functional Requirements:**

- ✅ All 4 new endpoints working correctly
- ✅ File downloads functioning (individual + ZIP)
- ✅ Enhanced generation flow with automatic parsing
- ✅ Live preview serving complete React applications

### **Performance Requirements:**

- File tree response < 500ms
- Individual file response < 200ms
- ZIP generation < 2 seconds
- Preview build time < 30 seconds

### **User Experience Requirements:**

- Intuitive file browsing
- Fast downloads
- **Full interactive website preview**
- Clear error messages and status updates

## 🔄 Phase 4 Preparation

### **Frontend Components Ready For:**

- File browser with tree view
- File preview with syntax highlighting
- Download buttons (individual + ZIP)
- **Live preview iframe component**

### **Infrastructure Ready For:**

- Multiple concurrent previews
- Preview management UI
- Build status tracking
- Error handling and recovery

## 🎯 Expected Outcome

After Phase 3 completion, users will experience:

1. **Generate Website** (existing functionality)
2. **Browse Files** in hierarchical tree view
3. **Download Individual Files** for inspection
4. **Download Complete ZIP** for development
5. **Preview Live Website** in full interactive mode

This creates a complete, professional AI website generation experience that rivals any existing solution in the market.

## 🏆 Strategic Impact

### **Immediate Value:**

- Professional file delivery system
- Complete project downloads
- Live website previews

### **Competitive Advantage:**

- Full interactive preview (rare in AI generators)
- Professional developer workflow
- Complete project delivery

### **Foundation for Future:**

- Live preview infrastructure ready
- Scalable file management system
- Enhanced user experience platform

**Phase 3 transforms our AI Website Generator from a "text output tool" to a "complete website delivery platform".**
