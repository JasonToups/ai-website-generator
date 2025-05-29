import React from 'react';
import { Link } from 'react-router-dom';
import { Facebook, Instagram, Twitter } from 'react-feather';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-100 py-8">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li><Link to="/" className="text-gray-600 hover:text-primary">Home</Link></li>
              <li><Link to="/shop" className="text-gray-600 hover:text-primary">Shop</Link></li>
              <li><Link to="/about" className="text-gray-600 hover:text-primary">About Us</Link></li>
              <li><Link to="/contact" className="text-gray-600 hover:text-primary">Contact</Link></li>
            </ul>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-4">Customer Service</h3>
            <ul className="space-y-2">
              <li><Link to="/shipping" className="text-gray-600 hover:text-primary">Shipping</Link></li>
              <li><Link to="/returns" className="text-gray-600 hover:text-primary">Returns</Link></li>
              <li><Link to="/faq" className="text-gray-600 hover:text-primary">FAQ</Link></li>
            </ul>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-4">Connect With Us</h3>
            <div className="flex space-x-4">
              <a href="#" className="text-gray-600 hover:text-primary">
                <Facebook size={20} />
              </a>
              <a href="#" className="text-gray-600 hover:text-primary">
                <Instagram size={20} />
              </a>
              <a href="#" className="text-gray-600 hover:text-primary">
                <Twitter size={20} />
              </a>
            </div>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-4">Newsletter</h3>
            <p className="text-gray-600 mb-2">Subscribe to our newsletter for updates and exclusive offers.</p>
            <form className="flex">
              <input
                type="email"
                placeholder="Your email"
                className="flex-grow border border-gray-300 rounded-l-md py-2 px-3 focus:outline-none focus:ring-2 focus:ring-primary"
              />
              <button
                type="submit"
                className="bg-primary text-white font-semibold py-2 px-4 rounded-r-md hover:bg-primary-dark transition duration-300"
              >
                Subscribe
              </button>
            </form>
          </div>
        </div>
        <div className="mt-8 pt-8 border-t border-gray-200 text-center">
          <p className="text-gray-600">&copy; 2023 Artisan Gems. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;