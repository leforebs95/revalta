import apiClient from './client';

export const authAPI = {
  login: async (credentials) => {
    const response = await apiClient.post('/login', credentials);
    return response.data;
  },

  logout: async () => {
    const response = await apiClient.post('/logout');
    return response.data;
  },

  oauthLogin: async (provider) => {
    const response = await apiClient.get('/oauth2/authorize/' + provider);
    return response.data;
  },

  getSession: async () => {
    const response = await apiClient.get('/getsession');
    return response.data;
  },

  getCsrfToken: async () => {
    const response = await apiClient.get('/getcsrf');
    return response.headers['x-csrftoken'];
  },
};