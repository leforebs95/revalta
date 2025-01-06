import axios, { AxiosError, AxiosInstance, AxiosResponse } from 'axios';

interface APIError {
  message: string;
  errors?: Record<string, string[]>;
  status: number;
}

class APIClient {
  private client: AxiosInstance;
  private csrfToken: string | null = null;

  constructor() {
    this.client = axios.create({
      baseURL: '/api',
      headers: {
        'Content-Type': 'application/json',
      },
      withCredentials: true, // Important for CSRF token cookies
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor
    this.client.interceptors.request.use(
      async (config) => {
        // Fetch CSRF token if we don't have it
        if (!this.csrfToken) {
          try {
            const response = await axios.get('/api/getcsrf');
            this.csrfToken = response.headers['x-csrf-token'];
          } catch (error) {
            console.error('Failed to fetch CSRF token:', error);
          }
        }

        // Add CSRF token to headers
        if (this.csrfToken) {
          config.headers['X-CSRF-Token'] = this.csrfToken;
        }

        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        const apiError: APIError = {
          message: 'An unexpected error occurred',
          status: error.response?.status || 500,
        };

        if (error.response?.data) {
          apiError.message = error.response.data.message || apiError.message;
          apiError.errors = error.response.data.errors;
        }

        // Handle authentication errors
        if (error.response?.status === 401) {
          // Redirect to login or handle auth error
          window.location.href = '/login';
        }

        return Promise.reject(apiError);
      }
    );
  }

  // Generic request method with type safety
  private async request<T>(
    method: string,
    url: string,
    data?: unknown
  ): Promise<T> {
    try {
      const response: AxiosResponse<T> = await this.client.request({
        method,
        url,
        data,
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  // Convenience methods
  public async get<T>(url: string): Promise<T> {
    return this.request<T>('GET', url);
  }

  public async post<T>(url: string, data?: unknown): Promise<T> {
    return this.request<T>('POST', url, data);
  }

  public async put<T>(url: string, data?: unknown): Promise<T> {
    return this.request<T>('PUT', url, data);
  }

  public async delete<T>(url: string): Promise<T> {
    return this.request<T>('DELETE', url);
  }
}

export const apiClient = new APIClient();