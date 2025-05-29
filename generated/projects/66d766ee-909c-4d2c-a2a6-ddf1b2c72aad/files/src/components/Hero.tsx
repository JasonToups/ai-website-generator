import React from 'react';
import { Link } from 'react-router-dom';

const Hero: React.FC = () => {
  return (
    <section className="relative h-screen">
      <div
        className="absolute inset-0 bg-cover bg-center"
        style={{ backgroundImage: "url('/hero-image.jpg')" }}
      ></div>
      <div className="absolute inset-0 bg-black bg-opacity-50"></div>
      <div className="relative container mx-auto px-4 h-full flex flex-col justify-center items-center text-center text-white">
        <h1 className="font-montserrat font-bold text-4xl md:text-5xl lg:text-6xl mb-4">
          Capturing Life's Moments
        </h1>
        <p className="text-xl md:text-2xl mb-8">
          Professional photography for every occasion
        </p>
        <Link
          to="/contact"
          className="bg-blue-700 hover:bg-blue-800 text-white font-bold py-3 px-6 rounded-lg transition duration-300"
        >
          Book a Session
        </Link>
      </div>
    </section>
  );
};

export default Hero;