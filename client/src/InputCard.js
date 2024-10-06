import React, { useState } from 'react';
import InfoCard from './InfoCard.js';
import FormCard from './FormCard.js';
import ResponseCard from './ResponseCard.js';

function checkPostcode() {
  //API call to go here
  const type = 'not scotland'
  return type
}

function InputCard() {
  const [submissionResult, setSubmissionResult] = useState(null); 

  function handleFormSubmit(result) {
    setSubmissionResult(result);
  };

  let termType = null;  
  termType = checkPostcode();

  if (submissionResult) {
    submissionResult.termType = checkPostcode();
  }

  let responseData;

  if (submissionResult === 'failure') {
    responseData = ["Something Has Gone Wrong. Please try again.", submissionResult]
  } else {
    responseData = ["success", submissionResult]
  }

  return (
    <div className="input-card-container">
      {submissionResult === null ? (
        <>
          <InfoCard />
          <FormCard onFormSubmit={handleFormSubmit} />
        </>
      ) : 
        <ResponseCard responseData={responseData} />
      }
    </div>
  );
}

export default InputCard;
