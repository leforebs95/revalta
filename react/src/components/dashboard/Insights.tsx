import React from 'react';
import { ChatInterface } from '../chat/ChatInterface';

const Insights: React.FC = () => {
  return (
    <div className="h-[calc(100vh-4rem)]">
      <h1 className="text-2xl font-semibold mb-6">AI Insights</h1>
      <div className="bg-white rounded-lg shadow-sm border h-full">
        <ChatInterface />
      </div>
    </div>
  );
};

export default Insights; 