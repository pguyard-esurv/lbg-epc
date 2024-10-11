import React, { useState } from 'react';
import InfoCard from './InfoCard.js';
import FormCard from './FormCard.js';
import ResponseCard from './ResponseCard.js';

function InputCard() {
  const [submissionResult, setSubmissionResult] = useState(null); 

  function handleFormSubmit(result) {
    setSubmissionResult(result);
  };

  return (
    <div className="input-card-container">
      {submissionResult === null ? (
        <>
          <InfoCard />
          <FormCard onFormSubmit={handleFormSubmit} />
        </>
      ) : 
        <ResponseCard responseData={submissionResult} />
      }
    </div>
  );
}

export default InputCard;
