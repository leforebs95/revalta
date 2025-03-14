import React from 'react';
import { useAuth } from '../hooks/useAuth';

const DashboardPage = () => {
  const { user } = useAuth();

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-2xl font-bold text-gray-900">
          Welcome back, {user?.name || 'User'}
        </h1>
        <p className="mt-1 text-gray-500">
          Here's an overview of your health data
        </p>
      </header>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {/* Symptom Summary Card */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="font-semibold text-gray-900">Recent Symptoms</h2>
          <p className="mt-2 text-sm text-gray-500">
            Track and monitor your symptoms over time
          </p>
        </div>

        {/* Lab Results Card */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="font-semibold text-gray-900">Lab Results</h2>
          <p className="mt-2 text-sm text-gray-500">
            View and manage your lab results
          </p>
        </div>

        {/* Family History Card */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="font-semibold text-gray-900">Family History</h2>
          <p className="mt-2 text-sm text-gray-500">
            Track your family health history
          </p>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;