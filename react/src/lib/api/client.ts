import axios from 'axios';

// Create API clients for different services
export const authClient = axios.create({
  baseURL: 'http://localhost:5000/api/auth',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const uploadsClient = axios.create({
  baseURL: 'http://localhost:5001/api/uploads',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const ocrClient = axios.create({
  baseURL: 'http://localhost:5002/api/ocr',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const chatClient = axios.create({
  baseURL: 'http://localhost:5004/api/chat',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add response interceptor to handle unauthorized access
const handleUnauthorized = (error: any) => {
  if (error.response && error.response.status === 401) {
    // Redirect to login page
    window.location.href = '/login';
  }
  return Promise.reject(error);
};

authClient.interceptors.response.use((response) => response, handleUnauthorized);
uploadsClient.interceptors.response.use((response) => response, handleUnauthorized);
ocrClient.interceptors.response.use((response) => response, handleUnauthorized);
chatClient.interceptors.response.use((response) => response, handleUnauthorized);
