import React from 'react';
import { Link } from 'react-router-dom';

const Home: React.FC = () => {
  return (
    <div className="text-center">
      <h1 className="text-4xl font-bold mb-4">Welcome to Shopping List App</h1>
      <p className="text-xl mb-8">Organize your shopping efficiently</p>
      <Link to="/lists" className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded transition duration-300">
        Create New List
      </Link>
    </div>
  );
};

export default Home;