import apiClient from './client';

export const documentsAPI = {
  getDocuments: async () => {
    const response = await apiClient.get('/documents');
    return response.data;
  },

  uploadDocument: async (file: File) => {
    // Get presigned URL
    const response = await apiClient.post('/documents/presign', {
      filename: file.name,
      contentType: file.type,
    });
    
    // Upload directly to S3
    await fetch(response.data.uploadUrl, {
      method: 'PUT',
      body: file,
      headers: {
        'Content-Type': file.type,
      }
    });

    // Notify backend of completed upload
    const completeResponse = await apiClient.post('/documents/complete', {
      s3_key: response.data.s3_key,
      filename: file.name,
      contentType: file.type
    });
    
    return completeResponse.data;
  },

  deleteDocument: async (documentId: string) => {
    const response = await apiClient.delete(`/documents/${documentId}`);
    return response.data;
  }
};