import { PreviewGallery } from '@/components/Gallery/PreviewGallery';

export function GalleryPage() {
  const handleProjectPreview = (projectId: string) => {
    // Open preview in new tab using our new backend endpoint
    window.open(`http://localhost:8000/preview/${projectId}`, '_blank');
  };

  const handleProjectDownload = (projectId: string) => {
    console.log('Download project:', projectId);
    // Download is handled by the gallery component
  };

  const handleProjectDelete = (projectId: string) => {
    console.log('Project deleted:', projectId);
    // Gallery component handles the deletion
  };

  return (
    <PreviewGallery
      onProjectPreview={handleProjectPreview}
      onProjectDownload={handleProjectDownload}
      onProjectDelete={handleProjectDelete}
    />
  );
}
