import axios from 'axios';

const AUTH_API_BASE_URL = 'http://localhost/api/auth';
const FILE_API_BASE_URL = 'http://localhost/api/uploads';
const OCR_API_BASE_URL = 'http://localhost/api/ocr';
const CHAT_API_BASE_URL = 'http://localhost/api/chat';

// Create API clients
export const authClient = axios.create({
  baseURL: AUTH_API_BASE_URL,
  withCredentials: true, // Important for handling cookies/sessions
  headers: {
    'Content-Type': 'application/json',
  },
});

export const uploadsClient = axios.create({
  baseURL: FILE_API_BASE_URL,
  withCredentials: true, // Important for handling cookies/sessions
  headers: {
    'Content-Type': 'application/json',
  },
});

export const ocrClient = axios.create({
  baseURL: OCR_API_BASE_URL,
  withCredentials: true, // Important for handling cookies/sessions
  headers: {
    'Content-Type': 'application/json',
  },
});

export const chatClient = axios.create({
  baseURL: CHAT_API_BASE_URL,
  withCredentials: true, // Important for handling cookies/sessions
  headers: {
    'Content-Type': 'application/json',
  },
});

// List of all API clients for bulk operations
const apiClients = [authClient, uploadsClient, ocrClient, chatClient];

// Function to update user ID in all API clients
export const updateUserIdInClients = (userId: string | null) => {
  apiClients.forEach(client => {
    // Add userId to query params for GET requests
    client.interceptors.request.use(config => {
      if (userId && config.method === 'get') {
        config.params = { ...config.params, userId };
      }
      
      // Add userId to body for POST/PUT requests
      if (userId && (config.method === 'post' || config.method === 'put')) {
        if (config.data instanceof FormData) {
          config.data.append('userId', userId);
        } else {
          config.data = { ...config.data, userId };
        }
      }
      
      return config;
    });
  });
};

// Response interceptor for handling unauthorized access
authClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

uploadsClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

ocrClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

chatClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
