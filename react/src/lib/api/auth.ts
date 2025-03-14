import { authClient } from './client';

interface LoginCredentials {
  userEmail: string;
  password: string;
}

interface SignUpCredentials extends LoginCredentials {
  firstName?: string;
  lastName?: string;
}

export const authAPI = {
  login: async (credentials: LoginCredentials) => {
    const response = await authClient.post('/login', credentials);
    return response.data;
  },

  logout: async () => {
    const response = await authClient.post('/logout');
    return response.data;
  },

  oauthLogin: async (provider: string) => {
    const response = await authClient.get('/oauth2/authorize/' + provider);
    return response.data;
  },

  signup: async (credentials: SignUpCredentials) => {
    const response = await authClient.post('/signup', credentials);
    return response.data;
  },

  getSession: async () => {
    const response = await authClient.get('/getsession');
    return response.data;
  },

  getCsrfToken: async () => {
    const response = await authClient.get('/getcsrf');
    const token = response.headers['x-csrftoken'];
    if (!token) {
      console.error('No CSRF token found in response headers:', response.headers);
      throw new Error('No CSRF token found in response');
    }
    return token;
  },
};