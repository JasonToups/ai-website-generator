import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import About from './components/About';
import Contact from './components/Contact';
import Footer from './components/Footer';
import ProductCatalog from './components/ProductCatalog';
import ProductPage from './components/ProductPage';
import Cart from './components/Cart';
import Checkout from './components/Checkout';

const App: React.FC = () => {
  return (
    <Router>
      <div className="flex flex-col min-h-screen">
        <Navbar />
        <main className="flex-grow">
          <Switch>
            <Route exact path="/">
              <Hero />
              <ProductCatalog featured={true} />
            </Route>
            <Route path="/shop">
              <ProductCatalog />
            </Route>
            <Route path="/product/:id">
              <ProductPage />
            </Route>
            <Route path="/about">
              <About />
            </Route>
            <Route path="/contact">
              <Contact />
            </Route>
            <Route path="/cart">
              <Cart />
            </Route>
            <Route path="/checkout">
              <Checkout />
            </Route>
          </Switch>
        </main>
        <Footer />
      </div>
    </Router>
  );
};

export default App;