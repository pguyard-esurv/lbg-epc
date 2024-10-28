import React, { useState } from 'react';
import ScotlandTerms from './ScotlandTerms';
import NotScotlandTerms from './NotScotlandTerms';
import ThankYou from './ThankYou';
import TermsCardWrapper from './TermsCardWrapper';

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

  if (responseData.selectedAddress.region) {
    if (responseData.selectedAddress.region === 'Scotland') {
      return (
        <TermsCardWrapper handleSubmit={handleSubmit} submissionStatus={submissionStatus}>
          <ScotlandTerms />
        </TermsCardWrapper>
      );
    }

    if (responseData.selectedAddress.region !== 'Scotland') {

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
