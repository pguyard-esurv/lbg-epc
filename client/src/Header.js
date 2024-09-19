import React from 'react';
import './index.css';
import logo from './esurv-logo.png';

function Header() {
  return (
    <header className="bg-primary-dark text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        {/* Logo and Link */}
        <a href="https://www.esurv.co.uk/" target="_blank" rel="noopener noreferrer" className="flex items-center">
          <img src={logo} alt="Logo" className="h-10 mr-4" />
        </a>
      </div>
    </header>
  );
};

export default Header;
