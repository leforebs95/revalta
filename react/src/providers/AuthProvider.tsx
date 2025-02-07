import React, { createContext, useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { authAPI } from '../lib/api/auth';

const AuthContext = createContext(null);

interface User {
  userId: string;
  email: string;
  role: string;
}

const useAuthProvider = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  // Only check auth once when the provider mounts
  useEffect(() => {
    console.log('AuthProvider effect triggered');
    const checkAuth = async () => {
      try {
        const session = await authAPI.getSession();
        setUser(session.user);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []); // Empty dependency array

  const login = async (credentials) => {
    try {
      setLoading(true);
      const response = await authAPI.login(credentials);
      setUser(response.user);
      navigate('/dashboard');
      return response;
    } catch (err) {
      setError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  
  const oauthLogin = async (provider) => {
    try {
      setLoading(true);
      const response = await authAPI.oauthLogin(provider);
      setUser(response.user);
      window.location.href = response.authorizationUrl;
      return response;
    } catch (err) {
      setError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  }

  const logout = async () => {
    try {
      setLoading(true);
      await authAPI.logout();
      setUser(null);
      navigate('/login');
    } catch (err) {
      setError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    user,
    loading,
    error,
    login,
    oauthLogin,
    logout
  };
};

export function AuthProvider({ children }) {
  const auth = useAuthProvider();
  
  return (
    <AuthContext.Provider value={auth}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}