import { filesClient } from './client';

export const documentsAPI = {
  getFiles: async (userId: string) => {
    // const session = await authAPI.getSession()
    const response = await filesClient.get(`/${userId}`);
    return response.data;
  },

  uploadFile: async (userId: string, file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    // const session = await authAPI.getSession()
    formData.append('userId', userId); // This should come from auth context

    const response = await filesClient.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  },

  deleteFile: async (fileId: string) => {
    const response = await filesClient.delete(`/${fileId}`);
    return response.data;
  }
};