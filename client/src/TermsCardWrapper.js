import React, { useRef } from 'react';
import SignatureCanvas from "react-signature-canvas";

function TermsCardWrapper({ children, handleSubmit, submissionStatus }) {
  // Ref for SignatureCanvas
  const sigCanvasRef = useRef(null);

  // Function to clear the signature
  const clearSignature = () => {
    sigCanvasRef.current.clear();
  };

  return (
    <>
      <div className="flex flex-col items-center justify-center min-h-screen p-4">
        <div className="max-w-2xl w-full">
          <div className="bg-white rounded-lg p-8">
            {children}
            <div className="flex justify-end items-start gap-4 mt-4">
              {/* Signature Canvas with border */}
              <div className="border-2 border-gray-300 rounded p-2">
                <SignatureCanvas
                  ref={sigCanvasRef}
                  penColor="blue"
                  canvasProps={{ width: 500, height: 200 }}
                />
              </div>
              
              {/* Button Section */}
              <div className="flex flex-col gap-2">
                <button
                  type="button"
                  onClick={handleSubmit}
                  className="bg-secondary-pink text-white px-6 py-2 rounded-full"
                >
                  Submit
                </button>
                <button
                  type="button"
                  onClick={clearSignature}
                  className="bg-gray-300 text-black px-6 py-2 rounded-full"
                >
                  Clear
                </button>
              </div>
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
