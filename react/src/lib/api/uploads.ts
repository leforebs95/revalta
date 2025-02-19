import { uploadsClient } from './client';

export const documentsAPI = {
  getUploads: async (userId: string) => {
    // const session = await authAPI.getSession()
    const response = await uploadsClient.get(`/${userId}`);
    return response.data;
  },

  uploadFile: async (userId: string, file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    // const session = await authAPI.getSession()
    formData.append('userId', userId); // This should come from auth context

    const response = await uploadsClient.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  },

  deleteUpload: async (fileId: string) => {
    const response = await uploadsClient.delete(`/${fileId}`);
    return response.data;
  }
};