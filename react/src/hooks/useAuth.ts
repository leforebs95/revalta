import { useState, useEffect } from 'react';
import { authAPI } from '../lib/api/auth';

interface User {
  id: string;
  email: string;
  name?: string;
}

interface AuthState {
  user: User | null;
  isLoading: boolean;
  error: string | null;
}

export const useAuth = () => {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    isLoading: true,
    error: null
  });

  const login = async (credentials: { email: string; password: string }) => {
    try {
      setAuthState(prev => ({ ...prev, isLoading: true, error: null }));
      const response = await authAPI.login(credentials);
      setAuthState({ user: response.user, isLoading: false, error: null });
      return response;
    } catch (error) {
      setAuthState({
        user: null,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Login failed'
      });
      throw error;
    }
  };

  const logout = async () => {
    try {
      setAuthState(prev => ({ ...prev, isLoading: true, error: null }));
      await authAPI.logout();
      setAuthState({ user: null, isLoading: false, error: null });
    } catch (error) {
      setAuthState({
        user: null,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Logout failed'
      });
      throw error;
    }
  };

  const oauthLogin = async (provider: string) => {
    try {
      setAuthState(prev => ({ ...prev, isLoading: true, error: null }));
      const response = await authAPI.oauthLogin(provider);
      return response;
    } catch (error) {
      setAuthState({
        user: null,
        isLoading: false,
        error: error instanceof Error ? error.message : 'OAuth login failed'
      });
      throw error;
    }
  };

  const signup = async (credentials: { email: string; password: string; name?: string }) => {
    try {
      setAuthState(prev => ({ ...prev, isLoading: true, error: null }));
      const response = await authAPI.signUp(credentials);
      setAuthState({ user: response.user, isLoading: false, error: null });
      return response;
    } catch (error) {
      setAuthState({
        user: null,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Signup failed'
      });
      throw error;
    }
  };

  // Check auth status on mount
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await authAPI.getSession();
        setAuthState({ user: response.user, isLoading: false, error: null });
      } catch (error) {
        setAuthState({
          user: null,
          isLoading: false,
          error: error instanceof Error ? error.message : 'Authentication failed'
        });
      }
    };

    checkAuth();
  }, []);

  return {
    ...authState,
    login,
    logout,
    oauthLogin,
    signup
  };
}; 