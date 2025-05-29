import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const Navbar: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="bg-white shadow-md">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center py-4">
          <Link to="/" className="font-montserrat font-bold text-2xl text-blue-700">
            Photographer
          </Link>
          <div className="hidden md:flex space-x-4">
            <NavLink to="/">Home</NavLink>
            <NavLink to="/about">About</NavLink>
            <NavLink to="/gallery">Gallery</NavLink>
            <NavLink to="/contact">Contact</NavLink>
          </div>
          <button
            className="md:hidden focus:outline-none"
            onClick={() => setIsOpen(!isOpen)}
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
          </button>
        </div>
      </div>
      {isOpen && (
        <div className="md:hidden absolute top-full left-0 right-0 bg-white shadow-md py-2">
          <NavLink to="/" mobile onClick={() => setIsOpen(false)}>
            Home
          </NavLink>
          <NavLink to="/about" mobile onClick={() => setIsOpen(false)}>
            About
          </NavLink>
          <NavLink to="/gallery" mobile onClick={() => setIsOpen(false)}>
            Gallery
          </NavLink>
          <NavLink to="/contact" mobile onClick={() => setIsOpen(false)}>
            Contact
          </NavLink>
        </div>
      )}
    </nav>
  );
};

interface NavLinkProps {
  to: string;
  children: React.ReactNode;
  mobile?: boolean;
  onClick?: () => void;
}

const NavLink: React.FC<NavLinkProps> = ({ to, children, mobile, onClick }) => {
  const baseClasses = "text-gray-700 hover:text-blue-700 transition duration-300";
  const mobileClasses = mobile ? "block px-4 py-2" : "";

  return (
    <Link
      to={to}
      className={`${baseClasses} ${mobileClasses}`}
      onClick={onClick}
    >
      {children}
    </Link>
  );
};

export default Navbar;