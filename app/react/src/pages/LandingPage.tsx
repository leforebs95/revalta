import React, { useState } from 'react';
import * as yup from 'yup';
import Header from '../components/landingpage/Header';
import Hero from '../components/landingpage/Hero';
import Features from '../components/landingpage/Features';
import About from '../components/landingpage/About';
import Contact from '../components/landingpage/Contact';
import Footer from '../components/landingpage/Footer';

function LandingPage() {
  return (
    <div className="min-h-screen bg-white">
      <Header />
      <main className="w-full">
        <Hero />
        <Features />
        <About />
        <Contact />
      </main>
      <Footer /> 
    </div>
  );
}

export default LandingPage;