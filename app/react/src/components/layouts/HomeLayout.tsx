import { Outlet } from 'react-router-dom';
import Overlay from '../Overlay';
import { useState } from 'react';
import React from 'react';

function Layout() {
  const [isOverlayOpen, setIsOverlayOpen] = useState(false);

  return (
    <>
      <header>
        {isOverlayOpen && (
          <Overlay onClose={() => setIsOverlayOpen(false)}>
            <div className="bg-whisper sm:rounded-lg">
              <div className="px-4 py-5 sm:p-6">
                <h3 className="text-base font-semibold leading-6 text-gray-900">
                  Provide the email associated with your account
                </h3>
                <form className="mt-5 sm:flex sm:items-center z-0">
                  <div className="w-full sm:max-w-xs">
                    <label htmlFor="email" className="sr-only">Email</label>
                    <input
                      type="email"
                      name="email"
                      id="email"
                      className="block w-full rounded-md border-0 py-1.5 px-1 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                      placeholder="email@example.com"
                      required
                    />
                  </div>
                  <button
                    type="submit"
                    className="mt-3 inline-flex w-full items-center justify-center rounded-md bg-nivaltaBlue px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 sm:ml-3 sm:mt-0 sm:w-auto"
                  >
                    Submit
                  </button>
                </form>
              </div>
            </div>
          </Overlay>
        )}
      </header>
      <Outlet />
    </>
  );
}