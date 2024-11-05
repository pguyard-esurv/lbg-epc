import React, { useState } from 'react';
import Terms from './Terms';
import ThankYou from './ThankYou';
import TermsCardWrapper from './TermsCardWrapper';

async function submitResponseData(responseData) {

  const backendUrl = 'https://wa-lbgepc-prd.azurewebsites.net//api/submit-form';

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





  return (
    <TermsCardWrapper handleSubmit={handleSubmit} submissionStatus={submissionStatus}>
      <Terms />
    </TermsCardWrapper>
  );


}

export default ResponseCard;
