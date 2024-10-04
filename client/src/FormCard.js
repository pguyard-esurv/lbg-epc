import React, { useState } from 'react';
import './index.css';  // Ensure your Tailwind styles are being imported
import {isValid} from 'postcode';

function FormCard() {
  const [formData, setFormData] = useState({
    fullName: '',
    telephone: '',
    email: '',
    customerRoll: '',
    address: '',
    agreeToPrivacy: false,
  });

  function handleChange(e) {
    const { name, value, type, checked } = e.target;
    setFormData(function (prevData) {
      return {
        ...prevData,
        [name]: type === 'checkbox' ? checked : value,
      };
    });
  }

  function handleSubmit(e) {
    e.preventDefault();
    console.log(formData);  // Process form data here
  }

  function searchAddress() {
    // console.log(parse(formData.address))
    const valid = isValid(formData.address);
    console.log(valid);

    if(!valid){
      console.log('invalid address/postcode; unable to parse')
    }
  }

  return (
    <div className="bg-primary-dark text-white p-7 rounded-lg max-w-6xl mx-auto mt-6 m-2">
      <form onSubmit={handleSubmit}>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Personal Information Column */}
          <div>
            <h2 className="text-xl font-semibold mb-4">Personal Information</h2>
            <div className="mb-4">
              <label className="block text-sm font-medium mb-2">Full Name</label>
              <input
                type="text"
                name="fullName"
                value={formData.fullName}
                onChange={handleChange}
                className="w-full p-2 rounded border border-white bg-primary-dark text-white placeholder-gray-400"
              />
            </div>
            <div className="mb-4">
              <label className="block text-sm font-medium mb-2">Telephone Number</label>
              <input
                type="tel"
                name="telephone"
                value={formData.telephone}
                onChange={handleChange}
                className="w-full p-2 rounded border border-white bg-primary-dark text-white placeholder-gray-400"
              />
            </div>
            <div className="mb-4">
              <label className="block text-sm font-medium mb-2">Email Address</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className="w-full p-2 rounded border border-white bg-primary-dark text-white placeholder-gray-400"
              />
            </div>
            <div className="mb-4">
              <label className="block text-sm font-medium mb-2">Customer Roll Number</label>
              <input
                type="text"
                name="customerRoll"
                value={formData.customerRoll}
                onChange={handleChange}
                className="w-full p-2 rounded border border-white bg-primary-dark text-white placeholder-gray-400"
                placeholder="Enter customer roll number"
              />
              <p className="text-xs text-gray-400 mt-1">This will be a 12-digit number, starting with either 1 for Halifax and 4 for Lloyds</p>
            </div>
          </div>

          {/* Property Information Column */}
          <div>
            <h2 className="text-xl font-semibold mb-4">Property Information</h2>
            <div className="mb-4">
              <label className="block text-sm font-medium mb-2">Address</label>
              <div className="flex">
                <input
                  type="text"
                  name="address"
                  value={formData.address}
                  onChange={handleChange}
                  className="w-full p-2 rounded-l border border-white bg-primary-dark text-white placeholder-gray-400"
                />
                <button
                  type="button"
                  className="bg-white text-primary-dark p-2 rounded-r border border-white"
                  onClick={searchAddress}
                  disabled={formData.address==''}
                >
                  Search
                </button>
              </div>
            </div>
            <div className="mb-4 flex items-center">
              <input
                type="checkbox"
                name="agreeToPrivacy"
                id="agreeToPrivacy"
                checked={formData.agreeToPrivacy}
                onChange={handleChange}
                className="hidden" // Hide the default checkbox
              />
              <label
                htmlFor="agreeToPrivacy"
                className={`w-5 h-5 rounded-full border-2 border-gray-300 cursor-pointer flex items-center justify-center
                  ${formData.agreeToPrivacy ? '' : 'bg-white'}`}
              >
                {formData.agreeToPrivacy && <div className="w-2 h-2 rounded-full bg-white"></div>}
              </label>
              <label className="ml-2 text-sm font-medium">I agree to the <a href='' className="underline">Privacy Notice</a></label>
            </div>
          </div>
        </div>

        {/* Submit Button */}
        <div className="text-right ">
          <button
            type="submit"
            className="bg-secondary-pink text-white px-6 py-1 rounded-full"
          >
            Next
          </button>
        </div>
      </form>
    </div>
  );
}

export default FormCard;

