"""Main FastAPI application for the AI Website Generator."""

import os
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from dotenv import load_dotenv

from backend.api.routes import router as api_router
from backend.utils.project_structure import ProjectStructureManager

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    print("🚀 AI Website Generator starting up...")
    yield
    # Shutdown
    print("🛑 AI Website Generator shutting down...")


# Create FastAPI app
app = FastAPI(
    title="AI Website Generator",
    description="CrewAI-powered website builder with AI agents",
    version="0.1.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root() -> Dict[str, Any]:
    """Root endpoint."""
    return {
        "message": "AI Website Generator API",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/preview/{project_id}")
async def preview_project_in_new_tab(project_id: str):
    """Serve complete project for new tab preview."""
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
            media_type="text/html"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to serve preview: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
