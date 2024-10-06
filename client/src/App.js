import React from 'react';
import './index.css';
import Header from './Header.js';
import Footer from './Footer.js';
import InputCard from './InputCard.js';

function App() {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <main className="flex-grow">
        <div className="container mx-auto p-4">
          <InputCard />
        </div>
      </main>
      <Footer />
    </div>
  );
}

export default App;
