import { useState } from 'react';
import { Button } from '@/components/ui/button';
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

interface ProjectCardProps {
  project: Project;
  onPreview: (projectId: string) => void;
  onDownload: (projectId: string) => void;
  onDelete: (projectId: string) => void;
}

export function ProjectCard({ project, onPreview, onDownload, onDelete }: ProjectCardProps) {
  const [isDeleting, setIsDeleting] = useState(false);

  const handleDelete = async () => {
    if (
      window.confirm(
        `Are you sure you want to delete "${project.title}"? This action cannot be undone.`
      )
    ) {
      setIsDeleting(true);
      try {
        await onDelete(project.project_id);
      } finally {
        setIsDeleting(false);
      }
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  };

  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  const getStatusColor = (status: string): string => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      case 'in_progress':
        return 'bg-yellow-100 text-yellow-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <Card className="h-full flex flex-col hover:shadow-lg transition-shadow duration-200">
      <CardHeader className="pb-3">
        {/* Thumbnail placeholder */}
        <div className="w-full h-32 bg-gradient-to-br from-blue-50 to-indigo-100 rounded-md mb-3 flex items-center justify-center">
          <div className="text-center">
            <div className="text-2xl mb-1">🌐</div>
            <div className="text-xs text-gray-500">{project.metadata.website_type}</div>
          </div>
        </div>

        <div className="space-y-1">
          <CardTitle className="text-lg line-clamp-2">{project.title}</CardTitle>
          <CardDescription className="text-sm line-clamp-2">{project.description}</CardDescription>
        </div>
      </CardHeader>

      <CardContent className="flex-1 flex flex-col justify-between">
        <div className="space-y-3">
          {/* Project metadata */}
          <div className="space-y-2">
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-500">Created:</span>
              <span>{formatDate(project.created_at)}</span>
            </div>

            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-500">Files:</span>
              <span>
                {project.file_count} files • {formatFileSize(project.metadata.file_size)}
              </span>
            </div>

            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-500">Status:</span>
              <span className={`px-2 py-1 text-xs rounded-full ${getStatusColor(project.status)}`}>
                {project.status}
              </span>
            </div>
          </div>

          {/* Technologies */}
          {project.metadata.technologies.length > 0 && (
            <div>
              <div className="text-sm text-gray-500 mb-1">Technologies:</div>
              <div className="flex flex-wrap gap-1">
                {project.metadata.technologies.slice(0, 3).map((tech) => (
                  <span
                    key={tech}
                    className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-md">
                    {tech}
                  </span>
                ))}
                {project.metadata.technologies.length > 3 && (
                  <span className="px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded-md">
                    +{project.metadata.technologies.length - 3} more
                  </span>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Action buttons */}
        <div className="flex gap-2 mt-4">
          <Button
            variant="outline"
            size="sm"
            onClick={() => onPreview(project.project_id)}
            disabled={!project.has_preview}
            className="flex-1">
            👁️ Preview
          </Button>

          <Button
            variant="outline"
            size="sm"
            onClick={() => onDownload(project.project_id)}
            className="flex-1">
            ⬇️ Download
          </Button>

          <Button
            variant="outline"
            size="sm"
            onClick={handleDelete}
            disabled={isDeleting}
            className="text-red-600 hover:text-red-700 hover:bg-red-50">
            {isDeleting ? '...' : '🗑️'}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
