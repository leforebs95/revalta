import React, { createContext, useContext, useState, useEffect } from 'react';
import { authClient, uploadsClient } from '../lib/api/client';
import { authAPI } from '../lib/api/auth';

const CSRFContext = createContext(null);

const useCSRFProvider = () => {
  const [csrfToken, setCsrfToken] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    console.log('CSRFProvider effect triggered');
    const fetchToken = async () => {
      try {
        const token = await authAPI.getCsrfToken();
        setCsrfToken(token);
        authClient.defaults.headers.common['x-csrftoken'] = token;
        uploadsClient.defaults.headers.common['x-csrftoken'] = token;
      } catch (err) {
        console.error('Failed to fetch CSRF token:', err);
        setError(err);
      } finally {
        setLoading(false);
      }
    };
    fetchToken();
  }, []);

  return {
    csrfToken,
    loading,
    error
  };
};

export function CSRFProvider({ children }) {
  const csrf = useCSRFProvider();

  return (
    <CSRFContext.Provider value={csrf}>
      {children}
    </CSRFContext.Provider>
  );
}

export function useCSRF() {
  const context = useContext(CSRFContext);
  if (!context) {
    throw new Error('useCSRF must be used within a CSRFProvider');
  }
  return context;
}