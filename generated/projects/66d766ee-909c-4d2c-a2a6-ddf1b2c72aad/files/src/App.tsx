import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import About from './components/About';
import Gallery from './components/Gallery';
import Contact from './components/Contact';
import Footer from './components/Footer';

const App: React.FC = () => {
  return (
    <Router>
      <div className="font-open-sans text-gray-700">
        <Navbar />
        <Switch>
          <Route exact path="/">
            <Hero />
            <About />
            <Gallery />
          </Route>
          <Route path="/about">
            <About fullPage={true} />
          </Route>
          <Route path="/gallery">
            <Gallery fullPage={true} />
          </Route>
          <Route path="/contact">
            <Contact />
          </Route>
        </Switch>
        <Footer />
      </div>
    </Router>
  );
};

export default App;