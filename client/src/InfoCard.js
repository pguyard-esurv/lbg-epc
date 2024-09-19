import React from 'react';
import './index.css';

function InfoCard() {
  const titleLeft = 'Book your free energy performance certificate';
  const titleRightText = 'Learn more about e.surv';
  const descriptionPart1 = "Booking your Energy Performance Certificate couldn't be easier. Simply provide your details and we will arrange for a Domestic Energy Assessor to complete your free EPC. Please complete the form below to get started. However, if you would like to speak to one of our team, please call us on ";
  const phoneNumber = '0800 169 9661';

  return (
    <div className="max-w-6xl mx-auto mt-2 text-black font-sans">
      {/* Title line with responsive flexbox behavior */}
      <div className="flex flex-col md:flex-row justify-between md:items-baseline">
        <h1 className="text-2xl font-bold">{titleLeft}</h1>
        <a 
          href="#" 
          target="_blank" 
          rel="noopener noreferrer" 
          className="text-sm md:text-right md:mt-0 mt-2 font-bold"
        >
          {titleRightText}
          <span className="ml-1 text-secondary-pink">{'>'}</span>
        </a>
      </div>

      {/* Middle font text below the title */}
      <div className="mt-2">
        <p className="text-base">
          {descriptionPart1}
          <span className="text-secondary-pink font-bold">{phoneNumber}</span>.
        </p>
      </div>
    </div>
  );
}

export default InfoCard;
