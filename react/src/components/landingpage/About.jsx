import { React } from 'react';

function About() {
    return (
<div id="about" className="relative bg-white">
        <div className="mx-auto max-w-7xl lg:flex lg:justify-between lg:px-8">
          <div className="lg:flex lg:w-1/2 lg:shrink lg:grow-0">
            <div className="relative h-80 lg:-ml-8 lg:h-auto lg:w-full lg:grow">
              <img
                className="absolute inset-0 h-full w-full bg-gray-50 object-cover"
                // src="/api/placeholder/800/600" Need the actual image path
                alt="Team collaboration"
              />
            </div>
          </div>
          <div className="px-6 lg:contents">
            <div className="mx-auto max-w-2xl pb-24 pt-16 sm:pb-32 sm:pt-20 lg:ml-8 lg:mr-0 lg:w-full lg:max-w-lg lg:flex-none lg:pt-32">
              <h1 className="mt-2 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
                Pioneering the future of personalized health management.
              </h1>
              <p className="mt-6 text-xl leading-8 text-gray-700">
                We transform complex health information into clear, actionable insights tailored to your individual health profile.
              </p>
              <div className="mt-10 max-w-xl text-base leading-7 text-gray-700">
                <p>
                  We aim to empower individuals with tools and information readily accessible about their individual health.
                  Our tools work for you to assist you with getting to the bottom of your health care issues, have powerful
                  analysis tools such as artificial intelligence and visual graphs.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
};

export default About;