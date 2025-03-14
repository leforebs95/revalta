import apiClient from './client';

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
}

export interface Conversation {
  id: string;
  title: string;
  user_id: string;
  created_at: string;
  updated_at: string;
  messages?: Message[];
}

export interface CreateConversationRequest {
  userId: string;
  title: string;
}

export interface SendMessageRequest {
  userId: string;
  content: string;
}

export interface SendMessageResponse {
  user_message: Message;
  assistant_message: Message;
}

class ChatApi {
  private baseUrl = 'http://localhost/api/chat';

  async createConversation(data: CreateConversationRequest): Promise<Conversation> {
    const response = await apiClient.post(`${this.baseUrl}/conversations`, data);
    return response.data;
  }

  async getConversations(userId: string): Promise<Conversation[]> {
    const response = await apiClient.get(`${this.baseUrl}/conversations`, {
      params: { user_id: userId }
    });
    return response.data;
  }

  async getConversation(conversationId: string): Promise<Conversation> {
    const response = await apiClient.get(`${this.baseUrl}/conversations/${conversationId}`);
    return response.data;
  }

  async sendMessage(conversationId: string, data: SendMessageRequest): Promise<SendMessageResponse> {
    const response = await apiClient.post(
      `${this.baseUrl}/conversations/${conversationId}/messages`,
      data
    );
    return response.data;
  }

  async deleteConversation(conversationId: string): Promise<void> {
    await apiClient.delete(`${this.baseUrl}/conversations/${conversationId}`);
  }
}

export const chatApi = new ChatApi();