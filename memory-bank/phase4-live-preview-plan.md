# Phase 4: Live Preview System Implementation Plan

## 🎯 **Objective**

Create a live preview environment for generated websites that allows users to see their AI-generated websites running in real-time.

## 🏗️ **Architecture Overview**

### **Backend Components**

1. **ProjectPreviewManager** - Core preview management
2. **Preview Server** - Serves individual projects on unique ports
3. **Static File Server** - Serves project files with proper MIME types
4. **Preview API Endpoints** - Control preview lifecycle

### **Frontend Components**

1. **Preview Frame** - Embedded iframe for website preview
2. **Preview Controls** - Start/stop/refresh preview
3. **Device Simulation** - Mobile/tablet/desktop views
4. **Preview Status** - Loading states and error handling

## 🔧 **Technical Implementation**

### **Phase 4A: Backend Preview Infrastructure**

#### **1. ProjectPreviewManager Class**

```python
class ProjectPreviewManager:
    def start_preview(project_id: str) -> Dict[str, Any]
    def stop_preview(project_id: str) -> Dict[str, Any]
    def get_preview_status(project_id: str) -> Dict[str, Any]
    def get_preview_url(project_id: str) -> str
```

#### **2. Preview Server Implementation**

- **Dynamic Port Allocation**: Each project gets unique port (3001, 3002, etc.)
- **Static File Serving**: Serve React projects with proper routing
- **Hot Reload**: Watch for file changes and auto-refresh
- **Process Management**: Start/stop preview servers as needed

#### **3. Enhanced API Endpoints**

- `POST /api/v1/projects/{id}/preview/start` - Start preview server
- `DELETE /api/v1/projects/{id}/preview/stop` - Stop preview server
- `GET /api/v1/projects/{id}/preview/status` - Get preview status
- `GET /api/v1/projects/{id}/preview/url` - Get preview URL

### **Phase 4B: Frontend Preview Interface**

#### **1. Preview Component**

- **Responsive iframe** for website display
- **Device simulation** (mobile, tablet, desktop)
- **Loading states** and error handling
- **Refresh controls**

#### **2. Preview Dashboard**

- **Project list** with preview status
- **Quick preview** buttons
- **Preview management** controls

## 🚀 **Implementation Steps**

### **Step 1: Backend Preview Manager**

1. Create `ProjectPreviewManager` class
2. Implement dynamic port allocation
3. Add process management for preview servers
4. Create preview API endpoints

### **Step 2: Static File Server**

1. Configure proper MIME types for React files
2. Handle SPA routing (fallback to index.html)
3. Serve assets (CSS, JS, images)
4. Enable CORS for cross-origin requests

### **Step 3: Frontend Preview Interface**

1. Create Preview component with iframe
2. Add device simulation controls
3. Implement preview status management
4. Add error handling and loading states

### **Step 4: Integration & Testing**

1. Test with generated React projects
2. Verify hot reload functionality
3. Test device simulation
4. End-to-end preview workflow testing

## 🎯 **Success Criteria**

- ✅ Generated websites preview in real-time
- ✅ Multiple projects can be previewed simultaneously
- ✅ Device simulation (mobile/tablet/desktop)
- ✅ Automatic refresh when files change
- ✅ Clean preview URL management
- ✅ Proper error handling and status reporting

## 🔄 **Future Enhancements**

- **Live Editing**: Edit code and see changes instantly
- **Performance Metrics**: Load times, bundle sizes
- **Accessibility Testing**: Built-in a11y checks
- **SEO Preview**: Meta tags, social sharing preview
- **Deployment Integration**: One-click deploy to hosting

## 📋 **Current Status**

- **Phase 3**: ✅ Complete - API Integration with file management
- **Phase 4A**: 🚧 In Progress - Backend preview infrastructure
- **Phase 4B**: ⏳ Planned - Frontend preview interface
