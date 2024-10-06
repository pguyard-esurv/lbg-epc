import React, { useState } from 'react';
import ScotlandTerms from './ScotlandTerms';
import NotScotlandTerms from './NotScotlandTerms';
import ThankYou from './ThankYou.js'
import TermsCardWrapper from './TermsCardWrapper';


async function submitResponseData(submissionResult) {
  return {
    ok: true
  }
  const response = await fetch('https://api.example.com/submit', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(submissionResult),
  });

  return response;
}

function ResponseCard({ responseData }) {
  const [submissionResult] = useState(responseData[1]);
  const [submissionStatus, setSubmissionStatus] = useState(null); // null, 'pending', 'success', or 'error'

  const handleSubmit = async () => {
    setSubmissionStatus('pending');
    try {
      const response = await submitResponseData(submissionResult);

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

  if (submissionResult.termType) {
    if (submissionResult.termType === 'scotland') {
      return (
        <TermsCardWrapper handleSubmit={handleSubmit} submissionStatus={submissionStatus}>
          <ScotlandTerms />
        </TermsCardWrapper>
      );
    }

    if (submissionResult.termType === 'not scotland') {
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

