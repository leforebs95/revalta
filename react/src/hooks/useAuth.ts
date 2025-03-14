import { useState, useEffect } from 'react';
import { authClient } from '../lib/api/client';

interface User {
  userId: string;
  firstName: string;
  lastName: string;
  userEmail: string;
  isEmailVerified: boolean;
  createdAt: string;
  lastLogin: string;
}

interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  isLoading: boolean;
  error: string | null;
}

export const useAuth = () => {
  const [authState, setAuthState] = useState<AuthState>({
    isAuthenticated: false,
    user: null,
    isLoading: true,
    error: null
  });

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await authClient.get('/getsession');
        setAuthState({
          isAuthenticated: response.data.login,
          user: response.data.user || null,
          isLoading: false,
          error: null
        });
      } catch (error) {
        setAuthState({
          isAuthenticated: false,
          user: null,
          isLoading: false,
          error: 'Failed to check authentication status'
        });
      }
    };

    checkAuth();
  }, []);

  const login = async (userEmail: string, password: string) => {
    try {
      const response = await authClient.post('/login', {
        userEmail,
        password
      });
      
      setAuthState({
        isAuthenticated: true,
        user: response.data.user,
        isLoading: false,
        error: null
      });
      
      return { success: true };
    } catch (error: any) {
      setAuthState(prev => ({
        ...prev,
        error: error.response?.data?.error || 'Login failed'
      }));
      return {
        success: false,
        error: error.response?.data?.error || 'Login failed',
      };
    }
  };

  const logout = async () => {
    try {
      await authClient.post('/logout');
      setAuthState({
        isAuthenticated: false,
        user: null,
        isLoading: false,
        error: null
      });
      return { success: true };
    } catch (error: any) {
      setAuthState(prev => ({
        ...prev,
        error: error.response?.data?.error || 'Logout failed'
      }));
      return {
        success: false,
        error: error.response?.data?.error || 'Logout failed',
      };
    }
  };

  const oauthLogin = async (provider: string) => {
    try {
      const response = await authClient.get('/oauth2/authorize/' + provider);
      // Redirect to provider's authorization URL
      window.location.href = response.data.authorizationUrl;
      return { success: true };
    } catch (error: any) {
      setAuthState(prev => ({
        ...prev,
        error: error.response?.data?.error || 'OAuth login failed'
      }));
      return {
        success: false,
        error: error.response?.data?.error || 'OAuth login failed'
      };
    }
  };

  const signup = async (credentials: { 
    userEmail: string; 
    password: string; 
    firstName: string;
    lastName: string;
  }) => {
    try {
      const response = await authClient.post('/signup', {
        userEmail: credentials.userEmail,
        password: credentials.password,
        firstName: credentials.firstName,
        lastName: credentials.lastName
      });
      
      setAuthState({
        isAuthenticated: true,
        user: response.data,
        isLoading: false,
        error: null
      });
      
      return { success: true };
    } catch (error: any) {
      setAuthState(prev => ({
        ...prev,
        error: error.response?.data?.error || 'Signup failed'
      }));
      return {
        success: false,
        error: error.response?.data?.error || 'Signup failed'
      };
    }
  };

  return {
    ...authState,
    login,
    logout,
    oauthLogin,
    signup
  };
}; 