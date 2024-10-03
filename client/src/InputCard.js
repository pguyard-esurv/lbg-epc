import React, { useState } from 'react';
import InfoCard from './InfoCard.js';
import FormCard from './FormCard.js';
import ResponseCard from './ResponseCard.js';

function InputCard() {
  const [isFormSubmitted, setIsFormSubmitted] = useState(false);

  const handleFormSubmit = () => {
    setIsFormSubmitted(true);
  };

  return (
    <div className="input-card-container">
      {isFormSubmitted ? (
        <ResponseCard />
      ) : (
        <>
          <InfoCard />
          <FormCard onFormSubmit={handleFormSubmit} />
        </>
      )}
    </div>
  );
}

export default InputCard;
