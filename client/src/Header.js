import React from 'react';
import './index.css';
import logo from './path-to-your-logo.png'; // Replace with the actual path to your logo

const Header = () => {
  return (
    <header className="bg-[#0c2538] text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        {/* Logo and Link */}
        <a href="https://www.esurv.co.uk/" target="_blank" rel="noopener noreferrer" className="flex items-center">
          <img src={logo} alt="Logo" className="h-10 mr-4" />
          <span className="text-lg font-semibold">Company Name</span>
        </a>
      </div>
    </header>
  );
};

export default Header;
