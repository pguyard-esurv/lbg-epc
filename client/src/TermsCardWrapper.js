import React, { useRef, useState, useEffect } from 'react';
import SignatureCanvas from "react-signature-canvas";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

function TermsCardWrapper({ children, handleSubmit, submissionStatus }) {
  const sigCanvasRef = useRef(null);
  const contentRef = useRef(null);
  const [startDate, setStartDate] = useState(new Date());

  // State variables for checkboxes and scrolling
  const [checkboxes, setCheckboxes] = useState({
    acceptTerms: false,
    commenceWork: false,
    paymentAcceptance: false,
    dataProcessing: false,
  });
  const [hasScrolledToBottom, setHasScrolledToBottom] = useState(false);

  const clearSignature = () => {
    sigCanvasRef.current.clear();
  };

  const handleCheckboxChange = (e) => {
    const { name, checked } = e.target;
    setCheckboxes((prevState) => ({
      ...prevState,
      [name]: checked,
    }));
  };

  const handleSubmission = () => {
    if (sigCanvasRef.current.isEmpty()) {
      alert("Please sign in the signature block and accept all terms before submitting.");
      return;
    }
    const allChecked = Object.values(checkboxes).every(Boolean);
    if (!allChecked) {
      alert("Please accept all terms by checking all the boxes before submitting.");
      return;
    }
    if (!hasScrolledToBottom) {
      alert("Please scroll to the bottom of the terms to confirm that you've read them.");
      return;
    }
    handleSubmit();
  };

  const handleScroll = () => {
    const { scrollTop, scrollHeight, clientHeight } = contentRef.current;
    if (scrollTop + clientHeight >= scrollHeight) {
      setHasScrolledToBottom(true);
    }
  };

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => setHasScrolledToBottom(entry.isIntersecting),
      { root: contentRef.current, threshold: 1.0 }
    );
    observer.observe(contentRef.current.lastChild);
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    if (submissionStatus === 'error') {
      alert("There was an error processing your request, please try again.");
      window.location.href = '/';
    }
  }, [submissionStatus]);

  return (
    <>
      <div className="flex flex-col items-center justify-center min-h-screen p-4">
        <div className="max-w-8xl w-full"> {/* Increased width */}
          <div className="bg-white rounded-lg p-8">
            
            {/* Scrollable Content Section with increased height */}
            <div
              ref={contentRef}
              className="overflow-y-auto max-h-96 border p-4" // Increased max-height
              onScroll={handleScroll}
            >
              {children}
            </div>

            {/* Confirmation Section */}
            <h2 className="text-xl font-bold mt-6">Confirmation of Instruction</h2>
            <p className="mt-2">
              Please click the checkboxes and sign below to confirm acceptance and understanding of the Terms and Conditions.
            </p>

            <div className="mt-4 space-y-4">
              <div className="flex items-start">
                <input
                  type="checkbox"
                  name="acceptTerms"
                  checked={checkboxes.acceptTerms}
                  onChange={handleCheckboxChange}
                  className="mt-1"
                />
                <label htmlFor="acceptTerms" className="ml-2">
                  I have read, understand, and accept the "Description of Service" and the contract terms and confirm that the Property to be assessed is the residential property at the address stated in the e.surv Limited web page to which these Terms and Conditions are linked.
                </label>
              </div>
              <div className="flex items-start">
                <input
                  type="checkbox"
                  name="commenceWork"
                  checked={checkboxes.commenceWork}
                  onChange={handleCheckboxChange}
                  className="mt-1"
                />
                <label htmlFor="commenceWork" className="ml-2">
                  I authorise e.surv Limited (including its subcontractors) to immediately commence work on arranging the EPC, and I accept that once the EPC has been provided to me, I will lose my right to cancel during the 14-day "cooling off" period (as provided by the Consumer Contracts (Information, Cancellation and Additional Charges) Regulations 2013).
                </label>
              </div>
              <div className="flex items-start">
                <input
                  type="checkbox"
                  name="paymentAcceptance"
                  checked={checkboxes.paymentAcceptance}
                  onChange={handleCheckboxChange}
                  className="mt-1"
                />
                <label htmlFor="paymentAcceptance" className="ml-2">
                  I accept that e.surv Limited will be paid by Lloyds Bank Plc in connection with this transaction.
                </label>
              </div>
              <div className="flex items-start">
                <input
                  type="checkbox"
                  name="dataProcessing"
                  checked={checkboxes.dataProcessing}
                  onChange={handleCheckboxChange}
                  className="mt-1"
                />
                <label htmlFor="dataProcessing" className="ml-2">
                  I authorise e.surv Limited to process my personal data in accordance with these terms.
                </label>
              </div>
            </div>

            {/* Signature and Buttons */}
            <div className="flex flex-col lg:flex-row justify-end items-start gap-4 mt-6">
              {/* Signature Canvas with responsive width */}
              <div className="border-2 border-gray-300 rounded p-2 w-full lg:w-[500px]">
                <SignatureCanvas
                  ref={sigCanvasRef}
                  penColor="blue"
                  canvasProps={{ width: 500, height: 114 }}
                />
              </div>

              {/* Button Section */}
              <div className="flex flex-col gap-2 mt-4 lg:mt-0"> {/* Stack on mobile, row on large screens */}
                <button
                  type="button"
                  onClick={handleSubmission}
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
                <div className="border-2 border-gray-300 rounded p-1">
                  <DatePicker selected={startDate} onChange={(date) => setStartDate(date)} />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      {submissionStatus === 'pending' && <p>Submitting...</p>}
    </>
  );
}

export default TermsCardWrapper;
