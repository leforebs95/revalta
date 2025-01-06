import { apiClient } from "./client";

interface LoginCredentials {
    email: string;
    password: string;
  }
  
  interface LoginResponse {
    user: User;
    token: string;
  }
  
  interface User {
    id: string;
    email: string;
    name: string;
  }
  
  export const authAPI = {
    login: (credentials: LoginCredentials) =>
      apiClient.post<LoginResponse>('/login', credentials),
  
    logout: () => apiClient.post('/logout'),
  
    getSession: () => apiClient.get<{ user: User | null }>('/getsession'),
  
    signup: (data: LoginCredentials & { name: string }) =>
      apiClient.post<{ user: User }>('/signup', data),
  };