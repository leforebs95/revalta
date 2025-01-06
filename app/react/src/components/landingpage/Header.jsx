import React, { useState } from 'react';

function Header() {
  const handleAnchorClick = (event, anchorId) => {
    event.preventDefault();
    const anchor = document.getElementById(anchorId);
    window.scrollTo({
      top: anchor?.offsetTop,
      behavior: 'smooth'
    });
  };

  return (
    <header className="sticky top-0 z-10 shadow-sm bg-white bg-opacity-60 bg-clip-padding blur-backdrop-filter">
      <nav className="mx-auto flex items-center justify-between gap-x-6 p-6 lg:px-8" aria-label="Global">
        <div className="flex lg:flex-1">
          <a href="/" className="-m-1.5 p-1.5 text-nivaltaBlue font-bold text-3xl">
            Nivalta
          </a>
        </div>
        <div className="hidden lg:flex lg:gap-x-12">
          <a
            href="#home"
            onClick={(e) => handleAnchorClick(e, 'home')}
            className="text-md font-semibold leading-6 text-gray-900 hover:text-nivaltaBlue"
          >
            Home
          </a>
          <a
            href="#features"
            onClick={(e) => handleAnchorClick(e, 'features')}
            className="text-md font-semibold leading-6 text-gray-900 hover:text-nivaltaBlue"
          >
            Features
          </a>
          <a
            href="#about"
            onClick={(e) => handleAnchorClick(e, 'about')}
            className="text-md font-semibold leading-6 text-gray-900 hover:text-nivaltaBlue"
          >
            About Us
          </a>
          <a
            href="#contact"
            onClick={(e) => handleAnchorClick(e, 'contact')}
            className="text-md font-semibold leading-6 text-gray-900 hover:text-nivaltaBlue"
          >
            Contact
          </a>
        </div>
        <div className="flex flex-1 items-center justify-end gap-x-6">
          <a
            href="#waitlist"
            onClick={(e) => handleAnchorClick(e, 'waitlist')}
            className="rounded-3xl bg-nivaltaBlue px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
          >
            Wait List
          </a>
        </div>
        <div className="flex lg:hidden">
          <button
            type="button"
            className="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-gray-700"
          >
            <span className="sr-only">Open main menu</span>
            <svg
              className="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth="1.5"
              stroke="currentColor"
              aria-hidden="true"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"
              />
            </svg>
          </button>
        </div>
      </nav>
    </header>
  );
}

export default Header;