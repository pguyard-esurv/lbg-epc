import React, { useState } from 'react';
import Terms from './Terms';
import ThankYou from './ThankYou';
import TermsCardWrapper from './TermsCardWrapper';

async function submitResponseData(responseData) {
  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'https://lbg-epc.esurv.co.uk/';

  const backendApiUrl = backendUrl + 'api/submit-form' 

  const response = await fetch(backendApiUrl, {
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

  // handleSubmit now accepts full submission data from TermsCardWrapper
  const handleSubmit = async (additionalData) => {
    setSubmissionStatus('pending');
    try {
      // Merge responseData with additionalData from TermsCardWrapper
      const completeData = {
        ...responseData,
        ...additionalData, // Data from TermsCardWrapper passed up through onSubmit
      };

      const response = await submitResponseData(completeData);

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

  return (
    <TermsCardWrapper onSubmit={handleSubmit} submissionStatus={submissionStatus}>
      <Terms />
    </TermsCardWrapper>
  );
}

export default ResponseCard;
