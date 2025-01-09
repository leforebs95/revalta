import React from 'react';
import { useAuth } from '../providers/AuthProvider';

function DashboardPage() {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold tracking-tight text-gray-900">
            Welcome back, {user?.name || 'User'}
          </h1>
        </div>
      </header>
      <main>
        <div className="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8">
          {/* Add your dashboard content here */}
          <div className="px-4 py-6 sm:px-0">
            <div className="rounded-lg border-4 border-dashed border-gray-200 p-4">
              <p>Your dashboard content goes here</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default DashboardPage;