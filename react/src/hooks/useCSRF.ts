import { useState, useEffect } from 'react';
import { authClient, uploadsClient, ocrClient, chatClient } from '../lib/api/client';

interface CSRFState {
  csrfToken: string | null;
  isLoading: boolean;
  error: Error | null;
}

// Singleton to prevent multiple token fetches
let tokenPromise: Promise<string> | null = null;

export const useCSRF = () => {
  const [csrfState, setCsrfState] = useState<CSRFState>({
    csrfToken: null,
    isLoading: true,
    error: null
  });

  useEffect(() => {
    const fetchToken = async () => {
      try {
        // If there's already a token fetch in progress, wait for it
        if (tokenPromise) {
          const token = await tokenPromise;
          setCsrfState({ csrfToken: token, isLoading: false, error: null });
          return;
        }

        // Start a new token fetch
        tokenPromise = (async () => {
          const response = await authClient.get('/getcsrf');
          const token = response.headers['x-csrftoken'];
          
          if (!token) {
            throw new Error('No CSRF token found in response');
          }
          
          // Update headers for all API clients
          const clients = [authClient, uploadsClient, ocrClient, chatClient];
          clients.forEach(client => {
            client.defaults.headers.common['X-CSRFToken'] = token;
          });
          
          return token;
        })();

        const token = await tokenPromise;
        setCsrfState({ csrfToken: token, isLoading: false, error: null });
      } catch (error) {
        console.error('Failed to fetch CSRF token:', error);
        setCsrfState({
          csrfToken: null,
          isLoading: false,
          error: error instanceof Error ? error : new Error('Failed to fetch CSRF token')
        });
      } finally {
        // Clear the promise after it's done (success or failure)
        tokenPromise = null;
      }
    };

    fetchToken();
  }, []);

  return csrfState;
}; 