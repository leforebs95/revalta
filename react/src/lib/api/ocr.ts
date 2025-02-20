import { ocrClient } from "./client";

export const ocrAPI = {

    createPages: async (fileId: string) => {
      const response = await ocrClient.post(`/pages/${fileId}`);
      return response
    },

    processPages: async (fileId: string) => {
      const response = await ocrClient.post(`/pages/${fileId}/process`);
      return response.data;
    },

    getPages: async (fileId: string) => {
      const response = await ocrClient.get(`/pages/${fileId}`);
      return response.data;
    },

    getPage: async (fileId: string, pageNumber: number) => {
      const response = await ocrClient.get(`/pages/${fileId}/${pageNumber}`);
      return response.data;
    },
  
    getStatus: async (fileId: string) => {
      const response = await ocrClient.get(`/status/${fileId}`);
      return response.data;
    },
  
    retryPage: async (fileId: string, pageNumber: number) => {
      const response = await ocrClient.post(`/pages/${fileId}/${pageNumber}/retry`);
      return response.data;
    },
  
    retryFailedPages: async (fileId: string) => {
      const response = await ocrClient.post(`/pages/${fileId}/retry`);
      return response.data;
    },

    deletePages: async (fileId: string) => {
      const response = await ocrClient.delete(`/pages/${fileId}`);
      return response.data;
    },

    deletePage: async (fileId: string, pageNumber: number) => {
      const response = await ocrClient.delete(`/pages/${fileId}/${pageNumber}`);
      return response.data;
    },
  };