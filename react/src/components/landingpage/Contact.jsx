import React, { useState } from 'react';
import * as yup from 'yup';

const schema = yup.object({
  name: yup.string().required('Name is required'),
  email: yup.string().email('Invalid email address').required('Email is required'),
  message: yup.string().required('Message cannot be empty')
});

function Contact() {
    
    const [formValues, setFormValues] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Form submitted:', formValues);
  };

  return (
    <div id="contact" className="relative isolate px-6 py-24 sm:py-32 lg:px-8">
        <div className="mx-auto max-w-xl lg:max-w-4xl">
          <h2 className="text-4xl font-bold tracking-tight text-gray-900">Looking for more information?</h2>
          <p className="mt-2 text-lg leading-8 text-gray-600">
            We are here to help in any way. Simply fill out our form below and we will have someone contact you promptly.
          </p>
          <div className="mt-16 flex flex-col gap-16 sm:gap-y-20 lg:flex-row">
            <form onSubmit={handleSubmit} className="lg:flex-auto">
              <div className="grid grid-cols-1 gap-x-8 gap-y-6 sm:grid-cols-2">
                <div>
                  <label htmlFor="name" className="block text-sm font-semibold leading-6 text-gray-900">
                    Name
                  </label>
                  <input
                    type="text"
                    id="name"
                    value={formValues.name}
                    onChange={(e) => setFormValues({...formValues, name: e.target.value})}
                    className="block w-full rounded-md border-0 px-3.5 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm"
                  />
                </div>
                <div>
                  <label htmlFor="email" className="block text-sm font-semibold leading-6 text-gray-900">
                    Email
                  </label>
                  <input
                    type="email"
                    id="email"
                    value={formValues.email}
                    onChange={(e) => setFormValues({...formValues, email: e.target.value})}
                    className="block w-full rounded-md border-0 px-3.5 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm"
                  />
                </div>
                <div className="sm:col-span-2">
                  <label htmlFor="message" className="block text-sm font-semibold leading-6 text-gray-900">
                    Message
                  </label>
                  <textarea
                    id="message"
                    rows={4}
                    value={formValues.message}
                    onChange={(e) => setFormValues({...formValues, message: e.target.value})}
                    className="block w-full rounded-md border-0 px-3.5 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm"
                  />
                </div>
              </div>
              <div className="mt-10">
                <button
                  type="submit"
                  className="block w-full rounded-md bg-blue-600 px-3.5 py-2.5 text-center text-sm font-semibold text-white shadow-sm hover:bg-blue-500"
                >
                  Let's talk
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
  );
};

export default Contact;