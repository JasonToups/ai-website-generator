import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { PreviewGallery } from '@/components/Gallery/PreviewGallery';
import './App.css';

interface ProjectError {
  message: string;
  timestamp: string;
}

interface Project {
  project_id: string;
  status: string;
  progress: number;
  current_step: string;
  files_generated: string[];
  errors: ProjectError[];
  description: string;
  created_at: string;
}

type ActiveTab = 'dashboard' | 'gallery';

function App() {
  const [activeTab, setActiveTab] = useState<ActiveTab>('gallery');
  const [description, setDescription] = useState('');
  const [requirements, setRequirements] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [currentProject, setCurrentProject] = useState<Project | null>(null);
  const [projects, setProjects] = useState<Project[]>([]);

  const handleGenerate = async () => {
    if (!description.trim()) return;

    setIsGenerating(true);

    try {
      const response = await fetch('http://localhost:8000/api/v1/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          description: description.trim(),
          requirements: requirements.split('\n').filter((r) => r.trim()),
          style_preferences: {},
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to start generation');
      }

      const result = await response.json();

      // Start polling for status
      pollProjectStatus(result.project_id);
    } catch (error) {
      console.error('Error starting generation:', error);
      alert('Failed to start website generation');
    } finally {
      setIsGenerating(false);
    }
  };

  const pollProjectStatus = async (projectId: string) => {
    const poll = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/v1/projects/${projectId}/status`);
        if (response.ok) {
          const project = await response.json();
          setCurrentProject(project);

          if (project.status === 'completed' || project.status === 'failed') {
            loadProjects();
            return;
          }
        }
      } catch (error) {
        console.error('Error polling status:', error);
      }

      // Continue polling every 2 seconds
      setTimeout(poll, 2000);
    };

    poll();
  };

  const loadProjects = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/projects');
      if (response.ok) {
        const data = await response.json();
        setProjects(data.projects);
      }
    } catch (error) {
      console.error('Error loading projects:', error);
    }
  };

  // Load projects on component mount
  useState(() => {
    loadProjects();
  });

  // Gallery event handlers
  const handleProjectPreview = async (projectId: string) => {
    try {
      // Start preview server
      const response = await fetch(
        `http://localhost:8000/api/v1/projects/${projectId}/preview/start`,
        {
          method: 'POST',
        }
      );

      if (response.ok) {
        const result = await response.json();
        if (result.success && result.url) {
          // Open preview in new tab
          window.open(result.url, '_blank');
        } else {
          alert('Failed to start preview server');
        }
      } else {
        alert('Failed to start preview server');
      }
    } catch (error) {
      console.error('Error starting preview:', error);
      alert('Failed to start preview server');
    }
  };

  const handleProjectDownload = (projectId: string) => {
    console.log('Download project:', projectId);
    // Download is handled by the gallery component
  };

  const handleProjectDelete = (projectId: string) => {
    console.log('Project deleted:', projectId);
    // Refresh the basic projects list if needed
    loadProjects();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">AI Website Generator</h1>
              <p className="text-gray-600">
                Powered by CrewAI - Let our team of AI agents build your website
              </p>
            </div>
          </div>

          {/* Tab Navigation */}
          <div className="flex space-x-8">
            <button
              onClick={() => setActiveTab('gallery')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'gallery'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}>
              🖼️ Gallery
            </button>
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'dashboard'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}>
              🏠 Dashboard
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'gallery' ? (
          <PreviewGallery
            onProjectPreview={handleProjectPreview}
            onProjectDownload={handleProjectDownload}
            onProjectDelete={handleProjectDelete}
          />
        ) : (
          <div className="max-w-4xl mx-auto space-y-6">
            {/* Generation Form */}
            <Card>
              <CardHeader>
                <CardTitle>Create New Website</CardTitle>
                <CardDescription>
                  Describe your website and our AI team will build it for you
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="description">Website Description</Label>
                  <Input
                    id="description"
                    placeholder="Describe the website you want to build..."
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    className="mt-1"
                  />
                </div>

                <div>
                  <Label htmlFor="requirements">Requirements (one per line)</Label>
                  <textarea
                    id="requirements"
                    placeholder="- Responsive design&#10;- Contact form&#10;- Modern styling"
                    value={requirements}
                    onChange={(e) => setRequirements(e.target.value)}
                    className="mt-1 w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    rows={4}
                  />
                </div>

                <Button
                  onClick={handleGenerate}
                  disabled={isGenerating || !description.trim()}
                  className="w-full">
                  {isGenerating ? 'Starting Generation...' : 'Generate Website'}
                </Button>
              </CardContent>
            </Card>

            {/* Current Project Status */}
            {currentProject && (
              <Card>
                <CardHeader>
                  <CardTitle>Generation Progress</CardTitle>
                  <CardDescription>Project ID: {currentProject.project_id}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-medium">Status: {currentProject.status}</span>
                      <span className="text-sm text-gray-500">{currentProject.progress}%</span>
                    </div>

                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${currentProject.progress}%` }}
                      />
                    </div>

                    <p className="text-sm text-gray-600">{currentProject.current_step}</p>

                    {currentProject.files_generated.length > 0 && (
                      <div>
                        <p className="text-sm font-medium">Files Generated:</p>
                        <ul className="text-sm text-gray-600 list-disc list-inside">
                          {currentProject.files_generated.map((file, index) => (
                            <li key={index}>{file}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {currentProject.errors.length > 0 && (
                      <div>
                        <p className="text-sm font-medium text-red-600">Errors:</p>
                        <ul className="text-sm text-red-600 list-disc list-inside">
                          {currentProject.errors.map((error, index) => (
                            <li key={index}>{typeof error === 'string' ? error : error.message}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Projects List */}
            {projects.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle>Recent Projects</CardTitle>
                  <CardDescription>Your generated websites</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {projects.slice(0, 5).map((project) => (
                      <div
                        key={project.project_id}
                        className="flex justify-between items-center p-3 border rounded-lg">
                        <div>
                          <p className="font-medium truncate max-w-md">{project.description}</p>
                          <p className="text-sm text-gray-500">
                            {new Date(project.created_at).toLocaleDateString()} • {project.status}
                          </p>
                        </div>
                        <div className="flex items-center space-x-2">
                          <span
                            className={`px-2 py-1 text-xs rounded-full ${
                              project.status === 'completed'
                                ? 'bg-green-100 text-green-800'
                                : project.status === 'failed'
                                ? 'bg-red-100 text-red-800'
                                : 'bg-yellow-100 text-yellow-800'
                            }`}>
                            {project.status}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>

                  {projects.length > 5 && (
                    <div className="mt-4 text-center">
                      <Button variant="outline" onClick={() => setActiveTab('gallery')}>
                        View All Projects in Gallery
                      </Button>
                    </div>
                  )}
                </CardContent>
              </Card>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
