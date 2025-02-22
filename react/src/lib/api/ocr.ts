import { ocrClient } from "./client";

export const ocrAPI = {

    extractDocument: async (fileId: string) => {
      const response = await ocrClient.post(`/document/${fileId}/extract`);
      return response
    },

    processDocument: async (fileId: string) => {
      const response = await ocrClient.post(`/document/${fileId}/process`);
      return response.data;
    },

    getDocument: async (fileId: string) => {
      const response = await ocrClient.get(`/document/${fileId}`);
      return response.data;
    },

    getPage: async (pageId: string) => {
      const response = await ocrClient.get(`/page/${pageId}`);
      return response.data;
    },

    getPageImage: async (pageId: string) => {
      const response = await ocrClient.get(`/page/${pageId}/image`, {
        responseType: "arraybuffer",
      });
      return response.data;
    },
  
    getStatus: async (fileId: string) => {
      const response = await ocrClient.get(`/document/${fileId}/status`);
      return response.data;
    },

    deleteDocument: async (fileId: string) => {
      const response = await ocrClient.delete(`/document/${fileId}`);
      return response.data;
    },
  };