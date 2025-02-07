import axios from 'axios';

const AUTH_API_BASE_URL = 'http://localhost/api/auth';
const FILE_API_BASE_URL = 'http://localhost/api/files';
const OCR_API_BASE_URL = 'http://localhost/api/ocr';

export const authClient = axios.create({
  baseURL: AUTH_API_BASE_URL,
  withCredentials: true, // Important for handling cookies/sessions
  headers: {
    'Content-Type': 'application/json',
  },
});

export const filesClient = axios.create({
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

filesClient.interceptors.response.use(
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