import apiClient from './client';

export const documentsAPI = {
  getDocuments: async () => {
    const response = await apiClient.get('/api/documents');
    return response.data;
  },

  uploadDocuments: async (files: File[]) => {
    const formData = new FormData();
    files.forEach(file => {
      formData.append('files', file);
    });

    const response = await apiClient.post('/api/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      }
    });
    return response.data;
  },

  deleteDocument: async (documentId: string) => {
    const response = await apiClient.delete(`/api/documents/${documentId}`);
    return response.data;
  }
};