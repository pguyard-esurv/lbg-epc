import React from 'react';

function ThankYou() {
  return (
    <div className="flex items-center justify-center min-h-[80vh]">
      <div className="max-w-lg w-full p-6 bg-primary-dark shadow-md text-center">
        <h1 className="text-4xl text-secondary-pink mb-4">Thank you.</h1>
        <p className="text-white text-lg">We have received your instruction. You will shortly receive an email from ehouse to book your EPC.</p>
      </div>
    </div>
  );
}

export default ThankYou;
