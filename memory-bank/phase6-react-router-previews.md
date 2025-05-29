# Phase 6: In-App Project Previews with React Router

## 🎯 **Project Overview**

**Goal**: Replace external preview servers with seamless in-app project previews using React Router, creating a unified user experience within the main application.

**Priority**: **HIGH** - User Experience Enhancement  
**Status**: Planning Phase - Ready for Implementation  
**Trigger**: User feedback that external preview servers (localhost:3003) break the application flow

---

## 📊 **Current State Analysis**

### **Phase 5 Gallery - COMPLETED** ✅

- ✅ **Gallery Tab**: Beautiful project grid with search and filtering
- ✅ **Project Cards**: Metadata display with action buttons
- ✅ **Download Functionality**: ZIP downloads working perfectly
- ✅ **Project Management**: Delete projects with confirmation
- ✅ **Responsive Design**: Works on all device sizes

### **Current Preview Issue** ❌

- ❌ **External Servers**: Preview buttons open localhost:3001, 3002, 3003, etc.
- ❌ **Context Loss**: Users leave the main application
- ❌ **Poor UX**: New browser tabs/windows break the flow
- ❌ **Navigation Issues**: No easy way back to gallery

### **User Experience Gap**

**Current Flow** (Problematic):

```
Gallery → Click Preview → New Tab (localhost:3003) → Lost Context
```

**Target Flow** (Seamless):

```
Gallery → Click Preview → /preview/project-id → Back to Gallery
```

---

## 🏗️ **Technical Architecture**

### **React Router Structure**

```
/ (root)
├── /gallery (current gallery view)
├── /dashboard (current dashboard view)
└── /preview/:projectId (NEW - in-app preview)
    ├── Full-screen project preview
    ├── Navigation breadcrumbs
    └── Action toolbar
```

### **Component Architecture**

```
App.tsx (Router Provider)
├── Header (Navigation + Breadcrumbs)
├── Routes
│   ├── /gallery → PreviewGallery.tsx
│   ├── /dashboard → Dashboard.tsx
│   └── /preview/:id → ProjectPreview.tsx (NEW)
└── Footer
```

---

## 🔧 **Implementation Plan**

### **Phase 6.1: React Router Setup** (Day 1)

#### **1. Install Dependencies**

```bash
cd frontend
npm install react-router-dom @types/react-router-dom
```

#### **2. Router Configuration**

```typescript
// main.tsx - Add Router Provider
import { BrowserRouter } from 'react-router-dom';

// App.tsx - Add Routes
import { Routes, Route, Navigate } from 'react-router-dom';
```

#### **3. Route Structure**

```typescript
<Routes>
  <Route path="/" element={<Navigate to="/gallery" replace />} />
  <Route path="/gallery" element={<PreviewGallery />} />
  <Route path="/dashboard" element={<Dashboard />} />
  <Route path="/preview/:projectId" element={<ProjectPreview />} />
</Routes>
```

### **Phase 6.2: ProjectPreview Component** (Day 1-2)

#### **Component Structure**

```typescript
interface ProjectPreviewProps {
  // Auto-populated from URL params
}

const ProjectPreview = () => {
  const { projectId } = useParams();
  const navigate = useNavigate();

  // Features:
  // - Load project content from API
  // - Render in iframe or direct component
  // - Navigation breadcrumbs
  // - Action toolbar (download, edit, share)
  // - Full-screen toggle
  // - Mobile-responsive
};
```

#### **Preview Rendering Options**

**Option A: Iframe Rendering** (Recommended)

```typescript
// Serve project content through dedicated endpoint
<iframe
  src={`/api/v1/projects/${projectId}/preview-content`}
  className="w-full h-full border-0"
  title={`Preview of ${project.title}`}
/>
```

**Option B: Direct Component Rendering**

```typescript
// Parse and render React components directly
// More complex but more integrated
const ProjectContent = dynamic(() => import(`/projects/${projectId}/App`));
```

### **Phase 6.3: Backend API Enhancement** (Day 2)

#### **New Endpoint: Preview Content**

```python
@router.get("/projects/{project_id}/preview-content")
async def get_project_preview_content(project_id: str):
    """Serve project content for in-app preview."""
    # Return HTML content with proper headers
    # Handle CSS/JS assets
    # Ensure proper CORS for iframe
```

#### **Enhanced File Serving**

```python
@router.get("/projects/{project_id}/assets/{file_path:path}")
async def serve_project_asset(project_id: str, file_path: str):
    """Serve project assets (CSS, JS, images)."""
    # Serve static files from project directory
    # Proper MIME types
    # Security checks
```

### **Phase 6.4: Navigation Integration** (Day 2-3)

#### **Update Gallery Navigation**

```typescript
// PreviewGallery.tsx - Update preview handler
const handleProjectPreview = (projectId: string) => {
  navigate(`/preview/${projectId}`);
};
```

#### **Breadcrumb Navigation**

```typescript
// Header.tsx - Add breadcrumbs
const Breadcrumbs = () => {
  const location = useLocation();

  // Gallery > Project Preview
  // Dashboard > Project Preview
};
```

#### **Back Navigation**

```typescript
// ProjectPreview.tsx - Back button
const handleBack = () => {
  navigate(-1); // Go back to previous page
  // Or navigate('/gallery') for explicit return
};
```

---

## 🎨 **User Interface Design**

### **ProjectPreview Layout**

```
┌─────────────────────────────────────────────────────────┐
│ ← Gallery | Project Preview: PhotoLens Portfolio    [⚙️] │
├─────────────────────────────────────────────────────────┤
│ [🔍] [⬇️] [🔗] [⚙️]                          [📱] [💻] [🖥️] │
├─────────────────────────────────────────────────────────┤
│                                                         │
│                                                         │
│              PROJECT PREVIEW IFRAME                     │
│                                                         │
│                                                         │
│                                                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### **Action Toolbar**

- **🔍 Zoom**: Zoom in/out of preview
- **⬇️ Download**: Download project ZIP
- **🔗 Share**: Copy preview URL
- **⚙️ Settings**: Preview options
- **📱💻🖥️ Responsive**: Toggle device views

### **Responsive Preview Modes**

- **Mobile**: 375px width
- **Tablet**: 768px width
- **Desktop**: Full width
- **Custom**: User-defined dimensions

---

## 🔄 **Migration Strategy**

### **Backward Compatibility**

1. **Keep External Preview System**: Maintain as fallback option
2. **Gradual Migration**: Add router previews alongside external
3. **User Choice**: Allow users to choose preview method
4. **Fallback Logic**: Use external if in-app fails

### **Implementation Phases**

#### **Phase 6.1: Basic Router Setup**

- Add React Router to project
- Create basic routes
- Update navigation to use router

#### **Phase 6.2: Preview Component**

- Build ProjectPreview component
- Implement iframe rendering
- Add basic navigation

#### **Phase 6.3: Enhanced Features**

- Add responsive preview modes
- Implement action toolbar
- Add breadcrumb navigation

#### **Phase 6.4: Polish & Optimization**

- Performance optimization
- Error handling
- Loading states
- Mobile responsiveness

---

## 📱 **Responsive Design**

### **Desktop (1200px+)**

- Full-screen preview with sidebar
- Complete action toolbar
- Breadcrumb navigation
- Device preview toggles

### **Tablet (768px - 1199px)**

- Full-width preview
- Collapsible toolbar
- Touch-friendly navigation
- Swipe gestures

### **Mobile (< 768px)**

- Full-screen preview
- Bottom action sheet
- Simplified toolbar
- Native-like navigation

---

## 🎯 **Success Metrics**

### **User Experience Goals**

- [ ] **Seamless Navigation**: No context loss when previewing
- [ ] **Fast Loading**: Preview loads in < 2 seconds
- [ ] **Intuitive Controls**: Easy navigation back to gallery
- [ ] **Responsive Design**: Works on all device sizes

### **Technical Goals**

- [ ] **Router Integration**: Clean URL structure
- [ ] **Performance**: No impact on main app performance
- [ ] **Reliability**: 99% preview success rate
- [ ] **Compatibility**: Works with all generated projects

### **Feature Completeness**

- [ ] **All Projects Previewable**: Every project can be previewed in-app
- [ ] **Full Functionality**: All preview features working
- [ ] **Navigation**: Smooth transitions between views
- [ ] **Actions**: Download, share, settings all functional

---

## 🔧 **Technical Implementation Details**

### **Frontend Changes**

#### **1. Package.json Updates**

```json
{
  "dependencies": {
    "react-router-dom": "^6.8.0",
    "@types/react-router-dom": "^5.3.3"
  }
}
```

#### **2. Main.tsx Router Setup**

```typescript
import { BrowserRouter } from 'react-router-dom';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);
```

#### **3. App.tsx Route Configuration**

```typescript
import { Routes, Route, Navigate } from 'react-router-dom';
import { ProjectPreview } from '@/components/Preview/ProjectPreview';

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <Header />
      <Routes>
        <Route path="/" element={<Navigate to="/gallery" replace />} />
        <Route path="/gallery" element={<GalleryPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/preview/:projectId" element={<ProjectPreview />} />
      </Routes>
    </div>
  );
}
```

### **Backend Changes**

#### **1. Preview Content Endpoint**

```python
@router.get("/projects/{project_id}/preview-content")
async def get_project_preview_content(project_id: str):
    """Serve project HTML content for iframe preview."""
    try:
        manager = ProjectStructureManager(project_id)
        index_file = manager.get_individual_file("index.html")

        if not index_file['success']:
            raise HTTPException(status_code=404, detail="Project index.html not found")

        # Modify HTML to include proper base URL for assets
        html_content = index_file['content']
        base_url = f"/api/v1/projects/{project_id}/assets/"

        # Inject base tag for relative URLs
        html_content = html_content.replace(
            '<head>',
            f'<head><base href="{base_url}">'
        )

        return Response(
            content=html_content,
            media_type="text/html",
            headers={"X-Frame-Options": "SAMEORIGIN"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to serve preview: {str(e)}")
```

#### **2. Asset Serving Endpoint**

```python
@router.get("/projects/{project_id}/assets/{file_path:path}")
async def serve_project_asset(project_id: str, file_path: str):
    """Serve project assets for preview."""
    try:
        manager = ProjectStructureManager(project_id)
        file_result = manager.get_individual_file(file_path)

        if not file_result['success']:
            raise HTTPException(status_code=404, detail="Asset not found")

        # Determine MIME type
        mime_type = "text/plain"
        if file_path.endswith('.css'):
            mime_type = "text/css"
        elif file_path.endswith('.js'):
            mime_type = "application/javascript"
        elif file_path.endswith('.json'):
            mime_type = "application/json"

        return Response(
            content=file_result['content'],
            media_type=mime_type
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to serve asset: {str(e)}")
```

---

## 🚀 **Implementation Timeline**

### **Day 1: Router Foundation**

- [ ] Install React Router dependencies
- [ ] Set up basic routing structure
- [ ] Update navigation to use router
- [ ] Test basic route transitions

### **Day 2: Preview Component**

- [ ] Create ProjectPreview component
- [ ] Implement iframe rendering
- [ ] Add backend preview content endpoint
- [ ] Test with one project

### **Day 3: Navigation & Polish**

- [ ] Add breadcrumb navigation
- [ ] Implement back button functionality
- [ ] Add action toolbar
- [ ] Test with all projects

### **Day 4: Responsive & Optimization**

- [ ] Responsive design implementation
- [ ] Performance optimization
- [ ] Error handling
- [ ] Final testing and polish

---

## 📋 **Development Checklist**

### **Frontend Tasks**

- [ ] Install and configure React Router
- [ ] Update App.tsx with route structure
- [ ] Create ProjectPreview component
- [ ] Add navigation breadcrumbs
- [ ] Implement responsive design
- [ ] Add loading and error states
- [ ] Update gallery preview buttons

### **Backend Tasks**

- [ ] Create preview content endpoint
- [ ] Add asset serving endpoint
- [ ] Handle CORS for iframe
- [ ] Add proper MIME type detection
- [ ] Implement error handling
- [ ] Test with all project types

### **Integration Tasks**

- [ ] Update gallery navigation
- [ ] Test route transitions
- [ ] Verify iframe rendering
- [ ] Test responsive behavior
- [ ] Performance testing
- [ ] Cross-browser compatibility

---

## 🎉 **Expected Outcome**

Upon completion of Phase 6, users will experience:

1. **Seamless Previews**: Click preview in gallery → instant in-app preview
2. **Unified Experience**: Never leave the main application
3. **Easy Navigation**: Clear breadcrumbs and back buttons
4. **Responsive Previews**: Test projects on different device sizes
5. **Enhanced Actions**: Download, share, and manage from preview
6. **Better Performance**: Faster loading than external servers

**This will complete the transformation of the AI Website Generator into a professional, unified website management platform with seamless user experience!**

---

## 🔄 **Future Enhancements** (Phase 7+)

- **Live Editing**: Edit projects directly in preview
- **Collaboration**: Share preview links with others
- **Version Control**: Compare different versions
- **Analytics**: Track preview usage and performance
- **Export Options**: Deploy directly to hosting platforms
