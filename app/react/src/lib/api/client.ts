import axios from 'axios';

const API_BASE_URL = 'http://localhost/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true, // Important for handling cookies/sessions
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response interceptor for handling unauthorized access
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;