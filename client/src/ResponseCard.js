import React, { useState } from 'react';
import ScotlandTerms from './ScotlandTerms';
import NotScotlandTerms from './NotScotlandTerms';
import ThankYou from './ThankYou';
import TermsCardWrapper from './TermsCardWrapper';

// Function to submit response data
async function submitResponseData(responseData) {
  const backendUrl = process.env.REACT_APP_BACKEND_URL + '/api/submit-form';

  const response = await fetch(backendUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(responseData),
  });

  return response;
}

function ResponseCard({ responseData }) {
  const [submissionResult] = useState(responseData[1]);
  const [submissionStatus, setSubmissionStatus] = useState(null); // null, 'pending', 'success', or 'error'

  const handleSubmit = async () => {
    setSubmissionStatus('pending');
    try {
      const response = await submitResponseData(responseData);

      if (response.ok) {
        setSubmissionStatus('success');
      } else {
        setSubmissionStatus('error');
      }
    } catch (error) {
      setSubmissionStatus('error');
    }
  };


  if (submissionStatus === 'success') {
    return <ThankYou />;
  }

  if (responseData.region) {
    if (responseData.region === 'Scotland') {
      return (
        <TermsCardWrapper handleSubmit={handleSubmit} submissionStatus={submissionStatus}>
          <ScotlandTerms />
        </TermsCardWrapper>
      );
    }

    if (responseData.region && responseData.region !== 'Scotland') {
      return (
        <TermsCardWrapper handleSubmit={handleSubmit} submissionStatus={submissionStatus}>
          <NotScotlandTerms />
        </TermsCardWrapper>
      );
    }
  } else {
    return (
      <div className="response-card-container">
        <div className="max-w-6xl mx-auto mt-2 text-black font-sans text-center">
          <h1 className="text-2xl font-bold">{responseData[0]}</h1>
        </div>
      </div>
    );
  }
}

export default ResponseCard;
