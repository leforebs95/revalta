import { apiClient } from "./client";

interface Symptom {
    id: string;
    name: string;
    description: string;
    severity: number;
    date: string;
  }
  
  export const symptomsAPI = {
    getAll: () => apiClient.get<Symptom[]>('/symptoms'),
  
    create: (symptom: Omit<Symptom, 'id'>) =>
      apiClient.post<Symptom>('/symptoms', symptom),
  
    update: (id: string, symptom: Partial<Symptom>) =>
      apiClient.put<Symptom>(`/symptoms/${id}`, symptom),
  
    delete: (id: string) => apiClient.delete<void>(`/symptoms/${id}`),
  };