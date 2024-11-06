import React, { useState } from 'react';
import Terms from './Terms';
import ThankYou from './ThankYou';
import TermsCardWrapper from './TermsCardWrapper';
import * as Sentry from "@sentry/react";

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
      const completeData = {
        ...responseData,
        ...additionalData,
      };

      const response = await submitResponseData(completeData);

      if (response.ok) {
        setSubmissionStatus('success');
      } else {
        setSubmissionStatus(response);
        Sentry.captureMessage("Response submission returned a non-OK status");
      }
    } catch (error) {
      setSubmissionStatus(error);
      Sentry.captureException(error); // This logs the error to Sentry
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
