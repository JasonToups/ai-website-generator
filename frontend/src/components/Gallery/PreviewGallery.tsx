import { useState, useEffect } from 'react';
import { ProjectCard } from './ProjectCard';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

interface ProjectMetadata {
  website_type: string;
  technologies: string[];
  file_size: number;
}

interface Project {
  project_id: string;
  title: string;
  description: string;
  status: string;
  created_at: string;
  updated_at: string;
  file_count: number;
  has_preview: boolean;
  thumbnail_url?: string;
  preview_url?: string;
  download_url: string;
  metadata: ProjectMetadata;
}

interface PreviewGalleryProps {
  onProjectPreview: (projectId: string) => void;
  onProjectDownload: (projectId: string) => void;
  onProjectDelete: (projectId: string) => void;
}

export function PreviewGallery({
  onProjectPreview,
  onProjectDownload,
  onProjectDelete,
}: PreviewGalleryProps) {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState<string>('all');

  // Load projects from gallery API
  const loadProjects = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch('http://localhost:8000/api/v1/projects/gallery');
      if (!response.ok) {
        throw new Error(`Failed to load projects: ${response.statusText}`);
      }

      const data = await response.json();
      setProjects(data.projects || []);
    } catch (err) {
      console.error('Error loading projects:', err);
      setError(err instanceof Error ? err.message : 'Failed to load projects');
    } finally {
      setLoading(false);
    }
  };

  // Load projects on component mount
  useEffect(() => {
    loadProjects();
  }, []);

  // Handle project deletion
  const handleProjectDelete = async (projectId: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/projects/${projectId}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error('Failed to delete project');
      }

      // Remove project from local state
      setProjects((prev) => prev.filter((p) => p.project_id !== projectId));

      // Call parent handler
      onProjectDelete(projectId);
    } catch (err) {
      console.error('Error deleting project:', err);
      alert('Failed to delete project. Please try again.');
    }
  };

  // Handle download
  const handleProjectDownload = (projectId: string) => {
    // Open download URL in new tab
    window.open(`http://localhost:8000/api/v1/projects/${projectId}/download`, '_blank');
    onProjectDownload(projectId);
  };

  // Filter projects based on search and status
  const filteredProjects = projects.filter((project) => {
    const matchesSearch =
      project.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      project.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
      project.metadata.website_type.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesStatus = filterStatus === 'all' || project.status === filterStatus;

    return matchesSearch && matchesStatus;
  });

  // Get unique statuses for filter
  const uniqueStatuses = Array.from(new Set(projects.map((p) => p.status)));

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading projects...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <Card className="w-full max-w-md">
          <CardHeader>
            <CardTitle className="text-red-600">Error Loading Projects</CardTitle>
            <CardDescription>{error}</CardDescription>
          </CardHeader>
          <CardContent>
            <Button onClick={loadProjects} className="w-full">
              Try Again
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Project Gallery</h2>
          <p className="text-gray-600">
            {projects.length} project{projects.length !== 1 ? 's' : ''} generated
          </p>
        </div>

        <Button onClick={loadProjects} variant="outline">
          🔄 Refresh
        </Button>
      </div>

      {/* Search and Filters */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="flex-1">
          <Input
            placeholder="Search projects..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full"
          />
        </div>

        <div className="sm:w-48">
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent">
            <option value="all">All Status</option>
            {uniqueStatuses.map((status) => (
              <option key={status} value={status}>
                {status.charAt(0).toUpperCase() + status.slice(1)}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Projects Grid */}
      {filteredProjects.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-6xl mb-4">🎨</div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            {searchTerm || filterStatus !== 'all' ? 'No matching projects' : 'No projects yet'}
          </h3>
          <p className="text-gray-600 mb-6">
            {searchTerm || filterStatus !== 'all'
              ? 'Try adjusting your search or filter criteria.'
              : 'Create your first website to see it appear here.'}
          </p>
          {(searchTerm || filterStatus !== 'all') && (
            <Button
              onClick={() => {
                setSearchTerm('');
                setFilterStatus('all');
              }}
              variant="outline">
              Clear Filters
            </Button>
          )}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredProjects.map((project) => (
            <ProjectCard
              key={project.project_id}
              project={project}
              onPreview={onProjectPreview}
              onDownload={handleProjectDownload}
              onDelete={handleProjectDelete}
            />
          ))}
        </div>
      )}

      {/* Results summary */}
      {filteredProjects.length > 0 && (
        <div className="text-center text-sm text-gray-500">
          Showing {filteredProjects.length} of {projects.length} projects
        </div>
      )}
    </div>
  );
}
