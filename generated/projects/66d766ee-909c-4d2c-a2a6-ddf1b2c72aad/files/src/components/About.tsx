import React from 'react';

interface AboutProps {
  fullPage?: boolean;
}

const About: React.FC<AboutProps> = ({ fullPage = false }) => {
  return (
    <section className={`py-12 md:py-16 lg:py-20 ${fullPage ? 'min-h-screen' : ''}`}>
      <div className="container mx-auto px-4">
        <h2 className="font-montserrat font-bold text-3xl md:text-4xl text-gray-900 mb-8 text-center">
          About Me
        </h2>
        <div className="flex flex-col md:flex-row items-center">
          <div className="md:w-1/2 mb-8 md:mb-0">
            <img
              src="/photographer-portrait.jpg"
              alt="Photographer"
              className="rounded-lg shadow-lg"
            />
          </div>
          <div className="md:w-1/2 md:pl-8">
            <p className="text-lg mb-4">
              Hello! I'm Jane Doe, a professional photographer with over 10 years of experience
              capturing life's most precious moments. My passion for photography started at a
              young age and has grown into a successful career.
            </p>
            <p className="text-lg mb-4">
              I specialize in portrait, wedding, and event photography. My style is a blend of
              candid and posed shots, always aiming to capture the genuine emotions and
              personalities of my subjects.
            </p>
            <p className="text-lg">
              When I'm not behind the camera, you can find me exploring nature trails, trying
              new recipes in the kitchen, or spending time with my family and our golden
              retriever, Max.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;