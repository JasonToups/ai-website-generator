import React from 'react';
import { Link } from 'react-router-dom';

const Hero: React.FC = () => {
  return (
    <section className="bg-secondary py-16 md:py-24">
      <div className="container mx-auto px-4">
        <div className="max-w-3xl mx-auto text-center">
          <h1 className="text-4xl md:text-5xl font-serif font-bold text-white mb-6">
            Handcrafted Jewelry for Every Occasion
          </h1>
          <p className="text-xl text-white mb-8">
            Discover unique, artisanal pieces that tell a story and elevate your style.
          </p>
          <Link
            to="/shop"
            className="bg-white text-primary font-semibold py-3 px-6 rounded-full hover:bg-primary hover:text-white transition duration-300"
          >
            Shop Now
          </Link>
        </div>
      </div>
    </section>
  );
};

export default Hero;