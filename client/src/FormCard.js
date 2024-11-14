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
    agreeToPrivacy: false,
  });

  const [postcode, setPostcode] = useState('');
  const [addresses, setAddresses] = useState([]);
  const [manualAddress, setManualAddress] = useState({
    building_name_number: '',
    street: '',
    town: '',
    postcode: '',
    region: ''
  });

  const [country, setCountry] = useState('');
  const [postcodeError, setPostcodeError] = useState(false);
  const [formErrors, setFormErrors] = useState({});

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

  // Separate function to handle country selection and error clearing
  function handleCountryChange(e) {
    const selectedCountry = e.target.value;
    setCountry(selectedCountry);
    setFormErrors((prevErrors) => ({
      ...prevErrors,
      country: selectedCountry ? '' : prevErrors.country, // Clear the error if a country is selected
    }));
  }

  function formatPostcode(pc) {
    pc = pc.toUpperCase().replace(/\s+/g, '');
    return pc.length > 3 ? `${pc.slice(0, -3)} ${pc.slice(-3)}` : pc;
  }

  function validateForm() {
    const errors = {};
    if (!formData.fullName.trim()) {
      errors.fullName = 'Full Name is required.';
    }

    const phoneRegex = /^[\d\s+\-().]+$/;
    const digitCount = formData.telephone.replace(/[^\d]/g, '').length;
    
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

    const rollNumberRegex = /^\d{12}$/;
    if (!formData.customerRoll.trim()) {
      errors.customerRoll = 'Customer Roll Number is required.';
    } else if (!rollNumberRegex.test(formData.customerRoll)) {
      errors.customerRoll = 'Customer Roll Number must be exactly 12 digits.';
    }
    if (!manualAddress.building_name_number?.trim() || !manualAddress.street?.trim()) {
      errors.selectedAddress = 'You must enter an address.';
    }
    if (!formData.agreeToPrivacy) {
      errors.agreeToPrivacy = 'You need to accept the privacy terms.';
    }
    if (!country) {
      errors.country = 'Country selection is required.';
    }
    if (!isValid(postcode)) {
      errors.postcode = 'Please enter a valid postcode.';
      setPostcodeError(true);
    } else {
      setPostcodeError(false);
    }

    return errors;
  }

  function handleSubmit(e) {
    e.preventDefault();
    const errors = validateForm();
    if (Object.keys(errors).length > 0) {
      setFormErrors(errors);
      return;
    }
    onFormSubmit({
      ...formData,
      selectedAddress: {
        ...manualAddress,
        postcode: formatPostcode(postcode), // Format postcode before submitting
        region: country
      }
    });
  }

  return (
    <div className="bg-primary-dark text-white p-7 rounded-lg max-w-6xl mx-auto mt-2 m-2">
      <form onSubmit={handleSubmit}>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <h2 className="text-xl font-semibold mb-4">Personal Information</h2>
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
                This will be a 12-digit number
              </p>
            </div>
          </div>

          <div>
            <h2 className="text-xl font-semibold mb-4">Property Information</h2>
            <div className="mb-4">
              <label className="block text-sm font-medium mb-2">Postcode</label>
              <input
                type="text"
                name="postcode"
                value={postcode}
                onChange={(e) => setPostcode(e.target.value)}
                autoComplete="off"
                className={`w-full p-2 rounded ${
                  postcodeError ? 'input-border-error' : 'input-border'
                } bg-primary-dark text-white placeholder-gray-400`}
              />
              {postcodeError && (
                <p className="text-red-500 mt-2">Invalid postcode. Please enter a valid postcode.</p>
              )}
            </div>
            <div className="mt-3 mb-4">
              <label className="block text-sm font-medium mb-2">Address</label>
              <div className="flex space-x-2">
                <input
                  type="text"
                  value={manualAddress.building_name_number || ""}
                  onChange={(e) =>
                    setManualAddress({ ...manualAddress, building_name_number: e.target.value })
                  }
                  className="w-1/3 p-2 rounded border border-white bg-primary-dark text-white placeholder-gray-400"
                  placeholder="Building Name/Number"
                />
                <input
                  type="text"
                  value={manualAddress.street || ""}
                  onChange={(e) =>
                    setManualAddress({ ...manualAddress, street: e.target.value })
                  }
                  className="w-1/3 p-2 rounded border border-white bg-primary-dark text-white placeholder-gray-400"
                  placeholder="Street"
                />
                <input
                  type="text"
                  value={manualAddress.town || ""}
                  onChange={(e) =>
                    setManualAddress({ ...manualAddress, town: e.target.value })
                  }
                  className="w-1/3 p-2 rounded border border-white bg-primary-dark text-white placeholder-gray-400"
                  placeholder="Town"
                />
              </div>
              {formErrors.selectedAddress && (!manualAddress.building_name_number?.trim() || !manualAddress.street?.trim()) && (
                <p className="text-red-500 text-sm mt-2">{formErrors.selectedAddress}</p>
              )}
            </div>

            <div className="mb-4">
              <label className="block text-sm font-medium mb-2">Country</label>
              <select
                value={country}
                onChange={handleCountryChange}
                className={`w-full p-2 rounded border ${
                  formErrors.country ? 'border-red-500' : 'border-white'
                } bg-primary-dark text-white placeholder-gray-400`}
              >
                <option value="">Select a country</option>
                <option value="England">England</option>
                <option value="Scotland">Scotland</option>
                <option value="Wales">Wales</option>
                <option value="Northern Ireland">Northern Ireland</option>
              </select>
              {formErrors.country && (
                <p className="text-red-500 text-sm mt-2">{formErrors.country}</p>
              )}
            </div>

            <div className="mt-4 flex items-center">
              <input
                type="checkbox"
                name="agreeToPrivacy"
                id="agreeToPrivacy"
                checked={formData.agreeToPrivacy}
                onChange={handleChange}
                className="hidden"
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
