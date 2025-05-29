import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { ShoppingCart, User, Search, Menu } from 'react-feather';

const Navbar: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <nav className="bg-white shadow-md">
      <div className="container mx-auto px-4 py-3">
        <div className="flex items-center justify-between">
          <Link to="/" className="text-2xl font-serif font-bold text-primary">
            Artisan Gems
          </Link>
          <div className="hidden md:flex items-center space-x-4">
            <Link to="/" className="text-gray-600 hover:text-primary">Home</Link>
            <Link to="/shop" className="text-gray-600 hover:text-primary">Shop</Link>
            <Link to="/about" className="text-gray-600 hover:text-primary">About Us</Link>
            <Link to="/contact" className="text-gray-600 hover:text-primary">Contact</Link>
          </div>
          <div className="flex items-center space-x-4">
            <button className="text-gray-600 hover:text-primary">
              <Search size={20} />
            </button>
            <Link to="/cart" className="text-gray-600 hover:text-primary">
              <ShoppingCart size={20} />
            </Link>
            <button className="text-gray-600 hover:text-primary">
              <User size={20} />
            </button>
            <button
              className="md:hidden text-gray-600 hover:text-primary"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              <Menu size={20} />
            </button>
          </div>
        </div>
      </div>
      {isMenuOpen && (
        <div className="md:hidden bg-white py-2">
          <div className="container mx-auto px-4">
            <Link to="/" className="block py-2 text-gray-600 hover:text-primary">Home</Link>
            <Link to="/shop" className="block py-2 text-gray-600 hover:text-primary">Shop</Link>
            <Link to="/about" className="block py-2 text-gray-600 hover:text-primary">About Us</Link>
            <Link to="/contact" className="block py-2 text-gray-600 hover:text-primary">Contact</Link>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;