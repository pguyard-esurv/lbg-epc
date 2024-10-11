import React, { useState } from 'react';
import './index.css';
import './FormCard.css';
import { isValid } from 'postcode';

function FormCard({ onFormSubmit }) {
  const [formData, setFormData] = useState({
    fullName: '',
    telephone: '',
    email: '',
    customerRoll: '',
    selectedAddress: '',
    region: '',
    agreeToPrivacy: false,
  });

  const [postcode, setPostcode] = useState('');
  const [region, setRegion] = useState('');
  const [addresses, setAddresses] = useState([]);
  const [postcodeError, setPostcodeError] = useState(false);
  const [formErrors, setFormErrors] = useState({});

  // Handle input changes
  function handleChange(e) {
    const { name, value, type, checked } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: type === 'checkbox' ? checked : value,
    }));
    setFormErrors((prevErrors) => ({
      ...prevErrors,
      [name]: '',
    }));
  }

  // Form validation
  function validateForm() {
    const errors = {};
    if (!formData.fullName.trim()) {
      errors.fullName = 'Full Name is required.';
    }
    // Telephone validation (must be at least 9 digits, can contain numbers, spaces, +, -, parentheses, and full stops)
    const phoneRegex = /^[\d\s+\-().]+$/; // Allows digits, spaces, +, -, parentheses (), and full stops .
    const digitCount = formData.telephone.replace(/[^\d]/g, '').length; // Counts only digits
    
    if (!formData.telephone.trim()) {
      errors.telephone = 'Telephone Number is required.';
    } else if (!phoneRegex.test(formData.telephone)) {
      errors.telephone = 'Telephone Number can only contain numbers, spaces, +, -, parentheses (), and full stops.';
    } else if (digitCount < 9) {
      errors.telephone = 'Telephone Number must contain at least 9 digits.';
    }
    if (!formData.email.trim()) {
      errors.email = 'Email Address is required.';
    }
    // Customer Roll Number validation (must be 12 digits)
    const rollNumberRegex = /^\d{12}$/; // Regex for exactly 12 digits
    if (!formData.customerRoll.trim()) {
      errors.customerRoll = 'Customer Roll Number is required.';
    } else if (!rollNumberRegex.test(formData.customerRoll)) {
      errors.customerRoll = 'Customer Roll Number must be exactly 12 digits.';
    }
    if (!formData.selectedAddress.trim()) {
      errors.selectedAddress = 'You must select an address.';
    }
    if (!formData.agreeToPrivacy) {
      errors.agreeToPrivacy = 'You need to accept the privacy terms.';
    }
    return errors;
  }

  // Handle form submission
  function handleSubmit(e) {
    e.preventDefault();
    const errors = validateForm();
    if (Object.keys(errors).length > 0) {
      setFormErrors(errors);
      return;
    }
    onFormSubmit(formData); // Include region in the submitted form data
  }

  // Handle postcode search and address lookup
  function searchAddress() {
    const valid = isValid(postcode);

    if (!valid) {
      setPostcodeError(true);
      return;
    }

    setPostcodeError(false); // Reset error if valid postcode

    const requestData = {
      postcode: postcode,
      token: '12345', // Replace with your actual token
    };

    fetch(`${process.env.REACT_APP_BACKEND_URL}/api/get-addresses`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => {
        setAddresses(data.addresses);
        setRegion(data.region);
      })

      .catch((error) => {
        console.error('Error fetching addresses:', error);
      });
  }

  // Select address from fetched addresses and save region
  function selectAddress(address) {
    setFormData((prevData) => ({
      ...prevData,
      selectedAddress: address, // Store selected address
      region: region, // Store region
    }));

    // Clear the selectedAddress error when an address is selected
    setFormErrors((prevErrors) => ({
      ...prevErrors,
      selectedAddress: '',
    }));
  }

  return (
    <div className="bg-primary-dark text-white p-7 rounded-lg max-w-6xl mx-auto mt-2 m-2">
      <form onSubmit={handleSubmit}>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Personal Information Column */}
          <div>
            <h2 className="text-xl font-semibold mb-4">Personal Information</h2>

            {/* Full Name Input */}
            <div className="mb-4">
              <label className="block text-sm font-medium mb-2">Full Name</label>
              <input
                type="text"
                name="fullName"
                value={formData.fullName}
                onChange={handleChange}
                className={`w-full p-2 rounded border ${
                  formErrors.fullName ? 'border-red-500' : 'border-white'
                } bg-primary-dark text-white placeholder-gray-400`}
              />
              {formErrors.fullName && (
                <p className="text-red-500 text-sm">{formErrors.fullName}</p>
              )}
            </div>

            {/* Telephone Number Input */}
            <div className="mb-4">
              <label className="block text-sm font-medium mb-2">Telephone Number</label>
              <input
                type="tel"
                name="telephone"
                value={formData.telephone}
                onChange={handleChange}
                className={`w-full p-2 rounded border ${
                  formErrors.telephone ? 'border-red-500' : 'border-white'
                } bg-primary-dark text-white placeholder-gray-400`}
              />
              {formErrors.telephone && (
                <p className="text-red-500 text-sm">{formErrors.telephone}</p>
              )}
            </div>

            {/* Email Address Input */}
            <div className="mb-4">
              <label className="block text-sm font-medium mb-2">Email Address</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className={`w-full p-2 rounded border ${
                  formErrors.email ? 'border-red-500' : 'border-white'
                } bg-primary-dark text-white placeholder-gray-400`}
              />
              {formErrors.email && (
                <p className="text-red-500 text-sm">{formErrors.email}</p>
              )}
            </div>

            {/* Customer Roll Number Input */}
            <div className="mb-4">
              <label className="block text-sm font-medium mb-2">Customer Roll Number</label>
              <input
                type="text"
                name="customerRoll"
                value={formData.customerRoll}
                onChange={handleChange}
                className={`w-full p-2 rounded border ${
                  formErrors.customerRoll ? 'border-red-500' : 'border-white'
                } bg-primary-dark text-white placeholder-gray-400`}
                placeholder="Enter customer roll number"
              />
              {formErrors.customerRoll && (
                <p className="text-red-500 text-sm">{formErrors.customerRoll}</p>
              )}
              <p className="text-xs text-gray-400 mt-1">
                This will be a 12-digit number, starting with either 1 for Halifax and 4 for Lloyds
              </p>
            </div>
          </div>

          {/* Property Information Column */}
          <div>
            <h2 className="text-xl font-semibold mb-4">Property Information</h2>

            {/* Postcode Search */}
            <div className="mb-4">
              <label className="block text-sm font-medium mb-2">Postcode</label>
              <div className="flex">
                <input
                  type="text"
                  name="postcode"
                  value={postcode}
                  onChange={(e) => setPostcode(e.target.value)}
                  className={`w-full p-2 rounded-l ${
                    postcodeError ? 'input-border-error' : 'input-border'
                  } bg-primary-dark text-white placeholder-gray-400`}
                />
                <button
                  type="button"
                  className="bg-white text-primary-dark p-2 rounded-r border border-white"
                  onClick={searchAddress}
                  disabled={postcode === ''}
                >
                  Search
                </button>
              </div>
              {postcodeError && (
                <p className="text-red-500 mt-2">Invalid postcode. Please enter a valid postcode.</p>
              )}

              {/* Show the error under the postcode search if no address is selected and no addresses have been fetched */}
              {formErrors.selectedAddress && addresses.length === 0 && (
                <p className="text-red-500 text-sm mt-2">{formErrors.selectedAddress}</p>
              )}
            </div>

            {/* Display list of addresses */}
            {addresses.length > 0 && (
              <div className="bg-gray-100 text-black p-4 rounded mt-2 max-h-40 overflow-y-auto">
                {addresses.map((address, index) => (
                  <button
                    key={index}
                    type="button"
                    onClick={() => selectAddress(address)}
                    className={`block w-full text-left p-2 mb-2 border ${
                      formData.selectedAddress === address
                        ? 'border-blue-500'
                        : 'border-gray-300'
                    } rounded hover:bg-gray-200`}
                  >
                    {address}
                  </button>
                ))}
              </div>
            )}

            {/* Show the error below the addresses if there are addresses but none selected */}
            {formErrors.selectedAddress && addresses.length > 0 && (
              <p className="text-red-500 text-sm mt-2">{formErrors.selectedAddress}</p>
            )}

            {/* Privacy Checkbox */}
            <div className="mt-4 flex items-center">
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
                className={`w-5 h-5 rounded-full border-2 border-gray-300 cursor-pointer flex items-center justify-center ${
                  formData.agreeToPrivacy ? '' : 'bg-white'
                }`}
              >
                {formData.agreeToPrivacy && (
                  <div className="w-2 h-2 rounded-full bg-white"></div>
                )}
              </label>
              <label className="ml-2 text-sm font-medium">
                I agree to the{' '}
                <a
                  href="https://www.esurv.co.uk/privacy-notice/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="underline"
                >
                  Privacy Notice
                </a>
              </label>
            </div>

            {formErrors.agreeToPrivacy && (
              <p className="text-red-500 text-sm">{formErrors.agreeToPrivacy}</p>
            )}
          </div>
        </div>

        {/* Submit Button */}
        <div className="text-right mt-4">
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
