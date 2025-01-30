import { authClient } from './client';

export const authAPI = {
  login: async (credentials) => {
    const response = await authClient.post('/login', credentials);
    return response.data;
  },

  logout: async () => {
    const response = await authClient.post('/logout');
    return response.data;
  },

  oauthLogin: async (provider) => {
    const response = await authClient.get('/oauth2/authorize/' + provider);
    return response.data;
  },

  getSession: async () => {
    const response = await authClient.get('/getsession');
    return response.data;
  },

  getCsrfToken: async () => {
    const response = await authClient.get('/getcsrf');
    console.log(response.headers['x-csrftoken']);
    return response.headers['x-csrftoken'];
  },
};