import React from 'react';

interface AboutProps {
  fullPage?: boolean;
}

const About: React.FC<AboutProps> = ({ fullPage = false }) => {
  return (
    <section className={`bg-white ${fullPage ? 'py-20' : 'py-12'}`}>
      <div className="container mx-auto px-4">
        <div className="flex flex-wrap items-center">
          <div className="w-full md:w-1/2 mb-8 md:mb-0">
            <h2 className="text-3xl font-bold mb-4">About the Photographer</h2>
            <p className="text-gray-700 mb-4">
              With over 10 years of experience in capturing life's most precious moments, I've developed a keen eye for detail and a passion for storytelling through imagery. My journey in photography began as a hobby and quickly blossomed into a fulfilling career.
            </p>
            <p className="text-gray-700 mb-4">
              I specialize in portrait, landscape, and event photography, always striving to capture the essence and emotion of each unique moment. My work has been featured in various publications and exhibitions, earning recognition for its creativity and technical excellence.
            </p>
            {fullPage && (
              <>
                <h3 className="text-2xl font-bold mt-8 mb-4">Equipment and Techniques</h3>
                <ul className="list-disc list-inside text-gray-700 mb-4">
                  <li>Professional-grade DSLR and mirrorless cameras</li>
                  <li>Wide range of prime and zoom lenses</li>
                  <li>Studio lighting and portable flash systems</li>
                  <li>Advanced post-processing techniques</li>
                </ul>
                <h3 className="text-2xl font-bold mt-8 mb-4">Awards and Recognitions</h3>
                <ul className="list-disc list-inside text-gray-700 mb-4">
                  <li>Best Portrait Photographer - Local Photography Awards 2020</li>
                  <li>Featured Artist - National Geographic Your Shot 2019</li>
                  <li>1st Place - International Landscape Photography Contest 2018</li>
                </ul>
              </>
            )}
          </div>
          <div className="w-full md:w-1/2">
            <img
              src="https://images.unsplash.com/photo-1542038784456-1ea8e935640e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2700&q=80"
              alt="Photographer"
              className="rounded-lg shadow-lg"
            />
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;