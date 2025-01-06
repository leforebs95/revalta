import React, { useState } from 'react';

function Footer() {

    const [waitlistEmail, setWaitlistEmail] = useState('');

    const handleWaitlistSubmit = (e) => {
        e.preventDefault();
        console.log('Waitlist email:', waitlistEmail);
      };

    return (
        <footer id="waitlist" className="bg-gray-900 mt-auto" aria-labelledby="footer-heading">
        <h2 id="footer-heading" className="sr-only">Footer</h2>
        <div className="mx-auto max-w-7xl px-6 pb-8 pt-8 sm:pt-24 lg:px-8 lg:pt-8">
          <div className="mt-8 border-t border-white/10 pt-4 pb-4 sm:mt-20 lg:mt-6 lg:flex lg:items-center lg:justify-between">
            <div>
              <h3 className="text-sm font-semibold leading-6 text-white">Sign up today</h3>
              <p className="mt-2 text-sm leading-6 text-gray-300">
                Join our waitlist to be the first to hear about new features and updates. We promise not to send any junk.
              </p>
            </div>
            <form onSubmit={handleWaitlistSubmit} className="mt-6 sm:flex sm:max-w-md lg:mt-0">
              <label htmlFor="email-address" className="sr-only">Email address</label>
              <input
                type="email"
                name="email-address"
                id="email-address"
                value={waitlistEmail}
                onChange={(e) => setWaitlistEmail(e.target.value)}
                className="w-full min-w-0 appearance-none rounded-md border-0 bg-white/5 px-3 py-1.5 text-base text-white shadow-sm ring-1 ring-inset ring-white/10 placeholder:text-gray-500 focus:ring-2 focus:ring-inset focus:ring-blue-500 sm:w-56 sm:text-sm sm:leading-6"
                placeholder="Enter your email"
              />
              <div className="mt-4 sm:ml-4 sm:mt-0 sm:flex-shrink-0">
                <button
                  type="submit"
                  className="flex w-full items-center justify-center rounded-3xl bg-blue-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500"
                >
                  Wait List
                </button>
              </div>
            </form>
          </div>
          <div className="border-t border-white/10 pt-4 md:flex md:items-center md:justify-between">
            <p className="text-xs leading-5 text-gray-400 md:order-1 md:mt-0">
              &copy; 2024 Nivalta, Inc. All rights reserved.
            </p>
          </div>
        </div>
      </footer>

  );
};

export default Footer;