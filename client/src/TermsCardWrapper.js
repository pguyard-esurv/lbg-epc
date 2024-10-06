import React from 'react';

function TermsCardWrapper({ children, handleSubmit, submissionStatus }) {
  return (
    <>
      <div className="flex flex-col items-center justify-center min-h-screen p-4">
        <div className="max-w-2xl w-full">
          <div className="bg-white rounded-lg p-8">
            {children}
            <div className="flex justify-end">
              <button
                type="button"
                onClick={handleSubmit}
                className="bg-secondary-pink text-white px-6 py-1 rounded-full mt-4"
              >
                Submit
              </button>
            </div>
          </div>
        </div>
      </div>
      {submissionStatus === 'pending' && <p>Submitting...</p>}
      {submissionStatus === 'error' && (
        <p className="text-red-500">Submission failed. Please try again.</p>
      )}
    </>
  );
}

export default TermsCardWrapper;
