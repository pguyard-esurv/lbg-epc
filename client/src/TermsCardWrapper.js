import React, { useRef, useState, useEffect } from 'react';
import SignatureCanvas from "react-signature-canvas";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

function TermsCardWrapper({ children, onSubmit, submissionStatus }) {
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

  // Clear the signature canvas
  const clearSignature = () => {
    sigCanvasRef.current.clear();
  };

  // Handle checkbox changes
  const handleCheckboxChange = (e) => {
    const { name, checked } = e.target;
    setCheckboxes((prevState) => ({
      ...prevState,
      [name]: checked,
    }));
  };

  // Collect and submit form data
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

    // Extract the signature data URL
    const signatureDataURL = sigCanvasRef.current.toDataURL('image/png');
    const cleanedSignatureData = signatureDataURL.replace(/^data:image\/png;base64,/, "");

    // Collect all form data
    const submissionData = {
      signature: cleanedSignatureData,
      date: startDate,
      checkboxes: checkboxes,
    };

    // Call the onSubmit prop function with the collected data
    onSubmit(submissionData);
  };

  // Scroll handling for the content section
  const handleScroll = () => {
    const { scrollTop, scrollHeight, clientHeight } = contentRef.current;
    if (scrollTop + clientHeight >= scrollHeight) {
      setHasScrolledToBottom(true);
    }
  };

  // Set up IntersectionObserver to track scrolling to the bottom
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => setHasScrolledToBottom(entry.isIntersecting),
      { root: contentRef.current, threshold: 1.0 }
    );
    observer.observe(contentRef.current.lastChild);
    return () => observer.disconnect();
  }, []);

  // Display an error if submission fails
  useEffect(() => {
    if (submissionStatus && submissionStatus === 'error') {
      alert(`There was an error processing your request: ${submissionStatus}`);
      window.location.reload();
    }
  }, [submissionStatus]);

  return (
    <>
      <div className="flex flex-col items-center justify-center min-h-screen p-4 relative">
        <div className="max-w-8xl w-full">
          <div className="bg-white rounded-lg p-8">
            
            {/* Scrollable Content Section */}
            <div
              ref={contentRef}
              className="overflow-y-auto max-h-96 border p-4"
              onScroll={handleScroll}
            >
              {children}
            </div>

            {/* Confirmation Section */}
            <h2 className="text-xl font-bold mt-6">Confirmation of Instruction</h2>
            <p className="mt-2">
              Please click the checkboxes and sign below to confirm acceptance and understanding of the Terms and Conditions.
            </p>

            {/* Checkbox Section */}
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
                  I have read, understand and accept the contract terms and conditions and confirm that the Property to be assessed is the residential property at the address stated in the e.surv Limited web page to which these Terms and Conditions are linked.
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
                  I authorise e.surv Limited (including its subcontractors) to immediately commence work on arranging the EPC, and I accept that once the EPC has been provided to me, I will lose my right to cancel during the 14 day "cooling off" period (as provided by the Consumer Contracts (Information, Cancellation and Additional Charges) Regulations 2013).
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
                  I accept that e.surv Limited will be paid by Lloyds Banking Group in connection with this transaction. 
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

              <p>Please e-sign and date this document:</p>

            </div>

            {/* Signature and Button Section */}
            <div className="flex flex-col lg:flex-row justify-end items-start gap-4 mt-6">
              {/* Signature Canvas */}
              <div className="border-2 border-gray-300 rounded p-2 w-full lg:w-[500px]">
                <SignatureCanvas
                  ref={sigCanvasRef}
                  penColor="blue"
                  canvasProps={{ width: 500, height: 114 }}
                />
              </div>

              {/* Button Section */}
              <div className="flex flex-col gap-2 mt-4 lg:mt-0">
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
                  <DatePicker 
                    selected={startDate}
                    onChange={(date) => setStartDate(date)}
                    dateFormat="dd/MM/yyyy"  
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Loading Spinner Overlay */}
        {submissionStatus === 'pending' && (
          <div className="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-75 z-50">
            <div className="w-16 h-16 border-4 border-secondary-pink border-t-transparent border-solid rounded-full animate-spin"></div>
          </div>
        )}
      </div>
    </>
  );
}

export default TermsCardWrapper;
