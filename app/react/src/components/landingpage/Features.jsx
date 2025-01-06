// components/Features.jsx
import React from 'react';
import { ScreenCog, CloudIcon, GlassIcon } from './Icons';

function Features() {
  return (
    <div id="features" className="w-full bg-white py-24 sm:py-32">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl lg:max-w-none">
          <h2 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
            Your Complete Health Management Tool Kit
          </h2>
        </div>
        <div className="mt-16 sm:mt-20">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-x-8 gap-y-8">
            <FeatureCard
              Icon={ScreenCog}
              title="Upload & Integrate"
              description="Upload and consolidate health data from various sources into one secure profile."
            />
            <FeatureCard
              Icon={ScreenCog}
              title="Track Your Symptoms"
              description="Log symptoms, identify problems, and generate reports for healthcare providers."
            />
            <FeatureCard
              Icon={CloudIcon}
              title="Map Family Health"
              description="Create your family health tree to better understand genetic predispositions and risks."
            />
            <FeatureCard
              Icon={GlassIcon}
              title="Discover Health Insights"
              description="Get tailored analysis and actionable recommendations for your wellness."
            />
          </div>
        </div>
      </div>
    </div>
  );
}

function FeatureCard({ Icon, title, description }) {
  return (
    <div className="flex flex-col h-full">
      <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
        <div className="h-14 w-12 mb-4">
          <Icon />
        </div>
        <div>
          <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
          <p className="mt-3 text-gray-600">{description}</p>
        </div>
      </div>
    </div>
  );
}

export default Features;