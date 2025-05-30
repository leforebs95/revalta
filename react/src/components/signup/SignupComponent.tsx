import React, { useState, ChangeEvent, FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';

interface FormData {
  firstName: string;
  lastName: string;
  userEmail: string;
  password: string;
  confirmPassword: string;
}

interface FormErrors {
  password: string;
  fields: string;
}

const SignupComponent = () => {
  const navigate = useNavigate();
  const { signup, login } = useAuth();
  
  const [formData, setFormData] = useState<FormData>({
    firstName: '',
    lastName: '',
    userEmail: '',
    password: '',
    confirmPassword: ''
  });

  const [formErrors, setFormErrors] = useState<FormErrors>({
    password: '',
    fields: ''
  });

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const validateForm = () => {
    let isValid = true;
    const errors: FormErrors = {
      password: '',
      fields: ''
    };

    // Check if any field is empty
    if (!formData.firstName || !formData.lastName || !formData.userEmail || 
        !formData.password || !formData.confirmPassword) {
      errors.fields = 'Please fill in all fields';
      isValid = false;
    }

    // Check if passwords match
    if (formData.password !== formData.confirmPassword) {
      errors.password = 'Passwords do not match';
      isValid = false;
    }

    setFormErrors(errors);
    return isValid;
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    try {
      // Signup request
      await signup({
        email: formData.userEmail,
        password: formData.password,
        name: `${formData.firstName} ${formData.lastName}`
      });

      // Login after successful signup
      await login({
        email: formData.userEmail,
        password: formData.password
      });

      navigate('/dashboard');
    } catch (error) {
      console.error('Error during signup:', error);
      setFormErrors(prev => ({
        ...prev,
        fields: 'Failed to create account. Please try again.'
      }));
    }
  };

  return (
    <div className="flex h-screen w-screen justify-center items-center">
      <div className="flex bg-whisper h-[600px] w-[400px] rounded-xl items-center justify-center">
        <form onSubmit={handleSubmit} className="w-full px-8">
          <div className="flex items-center mb-6">
            <h1 className="text-nivaltaBlue font-bold text-xl">Sign Up</h1>
          </div>

          {formErrors.fields && (
            <div className="mb-4 text-red-500 text-sm">
              {formErrors.fields}
            </div>
          )}

          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label htmlFor="firstName" className="block text-sm font-medium text-white-900">
                  First name
                </label>
                <input
                  type="text"
                  name="firstName"
                  id="firstName"
                  value={formData.firstName}
                  onChange={handleChange}
                  className="block w-full rounded-md border-0 py-1.5 px-2 text-white-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm"
                />
              </div>

              <div>
                <label htmlFor="lastName" className="block text-sm font-medium text-white-900">
                  Last name
                </label>
                <input
                  type="text"
                  name="lastName"
                  id="lastName"
                  value={formData.lastName}
                  onChange={handleChange}
                  className="block w-full rounded-md border-0 py-1.5 px-2 text-white-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm"
                />
              </div>
            </div>

            <div>
              <label htmlFor="userEmail" className="block text-sm font-medium text-white-900">
                Email address
              </label>
              <input
                type="email"
                name="userEmail"
                id="userEmail"
                value={formData.userEmail}
                onChange={handleChange}
                className="block w-full rounded-md border-0 py-1.5 px-2 text-white-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-white-900">
                Password
              </label>
              <input
                type="password"
                name="password"
                id="password"
                value={formData.password}
                onChange={handleChange}
                className="block w-full rounded-md border-0 py-1.5 px-2 text-white-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm"
              />
            </div>

            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-white-900">
                Confirm Password
              </label>
              <input
                type="password"
                name="confirmPassword"
                id="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                className="block w-full rounded-md border-0 py-1.5 px-2 text-white-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm"
              />
              {formErrors.password && (
                <p className="mt-1 text-sm text-red-500">{formErrors.password}</p>
              )}
            </div>
          </div>

          <div className="mt-6 flex items-center justify-end gap-x-6">
            <button
              type="button"
              onClick={() => navigate('/login')}
              className="text-sm font-semibold leading-6 text-white-900"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="rounded-md bg-nivaltaBlue px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
            >
              Sign up
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SignupComponent;