import React from 'react';
import { Link } from 'react-router-dom';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-800 text-white py-8">
      <div className="container mx-auto px-4">
        <div className="flex flex-wrap justify-between">
          <div className="w-full md:w-1/3 mb-6 md:mb-0">
            <h3 className="text-2xl font-bold mb-4">PhotoLens</h3>
            <p className="mb-4">Capturing moments that last forever</p>
            <div className="flex space-x-4">
              <a href="#" className="text-white hover:text-blue-500">
                <i className="fab fa-facebook-f"></i>
              </a>
              <a href="#" className="text-white hover:text-blue-500">
                <i className="fab fa-instagram"></i>
              </a>
              <a href="#" className="text-white hover:text-blue-500">
                <i className="fab fa-twitter"></i>
              </a>
            </div>
          </div>
          <div className="w-full md:w-1/3 mb-6 md:mb-0">
            <h4 className="text-lg font-bold mb-4">Quick Links</h4>
            <ul className="space-y-2">
              <li>
                <Link to="/" className="hover:text-blue-500">Home</Link>
              </li>
              <li>
                <Link to="/about" className="hover:text-blue-500">About</Link>
              </li>
              <li>
                <Link to="/gallery" className="hover:text-blue-500">Gallery</Link>
              </li>
              <li>
                <Link to="/contact" className="hover:text-blue-500">Contact</Link>
              </li>
            </ul>
          </div>
          <div className="w-full md:w-1/3">
            <h4 className="text-lg font-bold mb-4">Contact Info</h4>
            <p className="mb-2">123 Photography St, Lens City, PC 12345</p>
            <p className="mb-2">Phone: +1 (123) 456-7890</p>
            <p className="mb-2">Email: info@photolens.com</p>
          </div>
        </div>
        <div className="border-t border-gray-700 mt-8 pt-8 text-center">
          <p>&copy; 2023 PhotoLens. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;