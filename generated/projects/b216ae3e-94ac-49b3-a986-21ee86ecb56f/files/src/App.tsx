import React from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import About from './components/About';
import Gallery from './components/Gallery';
import Contact from './components/Contact';
import Footer from './components/Footer';

const App: React.FC = () => {
  return (
    <div className="font-open-sans text-gray-800">
      <Navbar />
      <Hero />
      <About />
      <Gallery />
      <Contact />
      <Footer />
    </div>
  );
};

export default App;
