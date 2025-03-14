import { uploadsClient } from './client';

export const documentsAPI = {
  getUploads: async () => {
    const response = await uploadsClient.get('/');
    return response.data;
  },

  uploadFile: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    
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