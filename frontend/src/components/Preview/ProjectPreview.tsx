import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface Project {
  project_id: string;
  title: string;
  description: string;
  status: string;
  created_at: string;
  file_count: number;
  metadata: {
    website_type: string;
    technologies: string[];
  };
}

export function ProjectPreview() {
  const { projectId } = useParams<{ projectId: string }>();
  const navigate = useNavigate();
  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!projectId) {
      setError('No project ID provided');
      setLoading(false);
      return;
    }

    loadProject();
  }, [projectId]);

  const loadProject = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/projects/${projectId}/status`);
      if (response.ok) {
        const projectData = await response.json();
        setProject(projectData);
      } else {
        setError('Project not found');
      }
    } catch (err) {
      setError('Failed to load project');
      console.error('Error loading project:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    navigate('/gallery');
  };

  const handleDownload = () => {
    if (projectId) {
      const downloadUrl = `http://localhost:8000/api/v1/projects/${projectId}/download`;
      window.open(downloadUrl, '_blank');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex items-center justify-center h-64">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
              <p className="mt-4 text-gray-600">Loading project...</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-gray-900 mb-4">Error</h1>
            <p className="text-gray-600 mb-6">{error}</p>
            <Button onClick={handleBack}>Back to Gallery</Button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header with Navigation */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between py-6">
            <div className="flex items-center space-x-4">
              <Button variant="outline" onClick={handleBack}>
                ← Back to Gallery
              </Button>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  Project Preview: {project?.title || project?.description || 'Untitled'}
                </h1>
                <p className="text-gray-600">
                  {project?.metadata?.website_type} • Created{' '}
                  {new Date(project?.created_at || '').toLocaleDateString()}
                </p>
              </div>
            </div>

            {/* Action Toolbar */}
            <div className="flex items-center space-x-3">
              <Button variant="outline" onClick={handleDownload}>
                ⬇️ Download
              </Button>
              <Button variant="outline">🔗 Share</Button>
              <Button variant="outline">⚙️ Settings</Button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Preview Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Card>
          <CardHeader>
            <CardTitle>Project Preview</CardTitle>
            <div className="flex items-center space-x-4 text-sm text-gray-600">
              <span>📁 {project?.file_count} files</span>
              <span>🔧 {project?.metadata?.technologies?.join(', ')}</span>
              <span
                className={`px-2 py-1 rounded-full text-xs ${
                  project?.status === 'completed'
                    ? 'bg-green-100 text-green-800'
                    : 'bg-yellow-100 text-yellow-800'
                }`}>
                {project?.status}
              </span>
            </div>
          </CardHeader>
          <CardContent>
            {project?.status === 'completed' ? (
              <div className="space-y-4">
                {/* Preview Iframe */}
                <div className="border rounded-lg overflow-hidden" style={{ height: '600px' }}>
                  <iframe
                    src={`http://localhost:8000/api/v1/projects/${projectId}/preview-content`}
                    className="w-full h-full border-0"
                    title={`Preview of ${project.title || project.description}`}
                    onError={() => setError('Failed to load preview content')}
                  />
                </div>

                {/* Device Preview Toggles */}
                <div className="flex justify-center space-x-2">
                  <Button variant="outline" size="sm">
                    📱 Mobile
                  </Button>
                  <Button variant="outline" size="sm">
                    💻 Tablet
                  </Button>
                  <Button variant="outline" size="sm">
                    🖥️ Desktop
                  </Button>
                </div>
              </div>
            ) : (
              <div className="text-center py-12">
                <p className="text-gray-600 mb-4">
                  This project is not yet completed and cannot be previewed.
                </p>
                <p className="text-sm text-gray-500">Status: {project?.status}</p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
