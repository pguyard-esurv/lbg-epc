import React from 'react';
import './index.css';
import Header from './Header.js';
import InfoCard from './InfoCard.js';
import FormCard from './FormCard.js';
import Footer from './Footer.js';

function App() {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <main className="flex-grow">
        <div className="container mx-auto p-4">
          <InfoCard />
          <FormCard />
        </div>
      </main>
      <Footer />
    </div>
  );
}

export default App;
