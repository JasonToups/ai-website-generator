import React, { useState } from 'react';

const Navbar: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
    setIsOpen(false);
  };

  return (
    <nav className="bg-white shadow-md">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <a href="#" className="text-2xl font-bold text-blue-500">
              PhotoLens
            </a>
          </div>
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4">
              <button
                onClick={() => scrollToSection('hero')}
                className="text-gray-800 hover:text-blue-500 px-3 py-2 rounded-md text-sm font-medium">
                Home
              </button>
              <button
                onClick={() => scrollToSection('about')}
                className="text-gray-800 hover:text-blue-500 px-3 py-2 rounded-md text-sm font-medium">
                About
              </button>
              <button
                onClick={() => scrollToSection('gallery')}
                className="text-gray-800 hover:text-blue-500 px-3 py-2 rounded-md text-sm font-medium">
                Gallery
              </button>
              <button
                onClick={() => scrollToSection('contact')}
                className="text-gray-800 hover:text-blue-500 px-3 py-2 rounded-md text-sm font-medium">
                Contact
              </button>
            </div>
          </div>
          <div className="md:hidden">
            <button
              onClick={toggleMenu}
              className="inline-flex items-center justify-center p-2 rounded-md text-gray-800 hover:text-blue-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white">
              <span className="sr-only">Open main menu</span>
              {isOpen ? (
                <svg
                  className="block h-6 w-6"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  aria-hidden="true">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              ) : (
                <svg
                  className="block h-6 w-6"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  aria-hidden="true">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                </svg>
              )}
            </button>
          </div>
        </div>
      </div>
      {isOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            <button
              onClick={() => scrollToSection('hero')}
              className="text-gray-800 hover:text-blue-500 block px-3 py-2 rounded-md text-base font-medium w-full text-left">
              Home
            </button>
            <button
              onClick={() => scrollToSection('about')}
              className="text-gray-800 hover:text-blue-500 block px-3 py-2 rounded-md text-base font-medium w-full text-left">
              About
            </button>
            <button
              onClick={() => scrollToSection('gallery')}
              className="text-gray-800 hover:text-blue-500 block px-3 py-2 rounded-md text-base font-medium w-full text-left">
              Gallery
            </button>
            <button
              onClick={() => scrollToSection('contact')}
              className="text-gray-800 hover:text-blue-500 block px-3 py-2 rounded-md text-base font-medium w-full text-left">
              Contact
            </button>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
