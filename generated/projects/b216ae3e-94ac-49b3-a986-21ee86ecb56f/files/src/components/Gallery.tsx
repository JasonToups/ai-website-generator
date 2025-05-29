import React, { useState } from 'react';

interface GalleryProps {
  fullPage?: boolean;
}

const Gallery: React.FC<GalleryProps> = ({ fullPage = false }) => {
  const [filter, setFilter] = useState('all');

  const images = [
    { id: 1, src: 'https://source.unsplash.com/random/800x600?portrait', category: 'portrait' },
    { id: 2, src: 'https://source.unsplash.com/random/800x600?landscape', category: 'landscape' },
    { id: 3, src: 'https://source.unsplash.com/random/800x600?event', category: 'event' },
    { id: 4, src: 'https://source.unsplash.com/random/800x600?portrait', category: 'portrait' },
    { id: 5, src: 'https://source.unsplash.com/random/800x600?landscape', category: 'landscape' },
    { id: 6, src: 'https://source.unsplash.com/random/800x600?event', category: 'event' },
  ];

  const filteredImages = filter === 'all' ? images : images.filter(img => img.category === filter);

  return (
    <section className={`bg-gray-100 ${fullPage ? 'py-20' : 'py-12'}`}>
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-bold mb-8 text-center">Photo Gallery</h2>
        <div className="flex justify-center mb-8">
          <button
            className={`mx-2 px-4 py-2 rounded ${filter === 'all' ? 'bg-blue-500 text-white' : 'bg-white text-blue-500'}`}
            onClick={() => setFilter('all')}
          >
            All
          </button>
          <button
            className={`mx-2 px-4 py-2 rounded ${filter === 'portrait' ? 'bg-blue-500 text-white' : 'bg-white text-blue-500'}`}
            onClick={() => setFilter('portrait')}
          >
            Portraits
          </button>
          <button
            className={`mx-2 px-4 py-2 rounded ${filter === 'landscape' ? 'bg-blue-500 text-white' : 'bg-white text-blue-500'}`}
            onClick={() => setFilter('landscape')}
          >
            Landscapes
          </button>
          <button
            className={`mx-2 px-4 py-2 rounded ${filter === 'event' ? 'bg-blue-500 text-white' : 'bg-white text-blue-500'}`}
            onClick={() => setFilter('event')}
          >
            Events
          </button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredImages.map(image => (
            <div key={image.id} className="relative overflow-hidden rounded-lg shadow-lg">
              <img
                src={image.src}
                alt={`Gallery image ${image.id}`}
                className="w-full h-64 object-cover transform hover:scale-105 transition duration-300"
              />
              <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center opacity-0 hover:opacity-100 transition duration-300">
                <button className="bg-white text-gray-800 font-bold py-2 px-4 rounded">
                  View
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Gallery;