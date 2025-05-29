import React, { useState } from 'react';

interface GalleryProps {
  fullPage?: boolean;
}

const Gallery: React.FC<GalleryProps> = ({ fullPage = false }) => {
  const [category, setCategory] = useState('all');

  const images = [
    { id: 1, src: '/gallery/image1.jpg', category: 'portrait' },
    { id: 2, src: '/gallery/image2.jpg', category: 'landscape' },
    { id: 3, src: '/gallery/image3.jpg', category: 'event' },
    { id: 4, src: '/gallery/image4.jpg', category: 'portrait' },
    { id: 5, src: '/gallery/image5.jpg', category: 'landscape' },
    { id: 6, src: '/gallery/image6.jpg', category: 'event' },
    { id: 7, src: '/gallery/image7.jpg', category: 'portrait' },
    { id: 8, src: '/gallery/image8.jpg', category: 'landscape' },
    { id: 9, src: '/gallery/image9.jpg', category: 'event' },
  ];

  const filteredImages = category === 'all'
    ? images
    : images.filter(image => image.category === category);

  return (
    <section className={`py-12 md:py-16 lg:py-20 ${fullPage ? 'min-h-screen' : ''}`}>
      <div className="container mx-auto px-4">
        <h2 className="font-montserrat font-bold text-3xl md:text-4xl text-gray-900 mb-8 text-center">
          Gallery
        </h2>
        <div className="flex justify-center mb-8">
          <button
            className={`mx-2 px-4 py-2 rounded ${
              category === 'all' ? 'bg-blue-700 text-white' : 'bg-gray-200'
            }`}
            onClick={() => setCategory('all')}
          >
            All
          </button>
          <button
            className={`mx-2 px-4 py-2 rounded ${
              category === 'portrait' ? 'bg-blue-700 text-white' : 'bg-gray-200'
            }`}
            onClick={() => setCategory('portrait')}
          >
            Portrait
          </button>
          <button
            className={`mx-2 px-4 py-2 rounded ${
              category === 'landscape' ? 'bg-blue-700 text-white' : 'bg-gray-200'
            }`}
            onClick={() => setCategory('landscape')}
          >
            Landscape
          </button>
          <button
            className={`mx-2 px-4 py-2 rounded ${
              category === 'event' ? 'bg-blue-700 text-white' : 'bg-gray-200'
            }`}
            onClick={() => setCategory('event')}
          >
            Event
          </button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredImages.map(image => (
            <div key={image.id} className="relative overflow-hidden group">
              <img
                src={image.src}
                alt={`Gallery image ${image.id}`}
                className="w-full h-full object-cover transition duration-300 group-hover:scale-105"
              />
              <div className="absolute inset-0 bg-black bg-opacity-50 opacity-0 group-hover:opacity-100 transition duration-300 flex items-center justify-center">
                <button className="bg-white text-gray-900 font-bold py-2 px-4 rounded">
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