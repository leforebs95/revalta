import { chatClient } from './client';

export interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  createdAt: string;
  conversationId: string;
}

export interface Conversation {
  id: string;
  title: string;
  createdAt: string;
  updatedAt: string;
  messages: Message[];
}

export interface CreateConversationRequest {
  title: string;
}

export interface CreateMessageRequest {
  content: string;
  conversationId: string;
}

class ChatAPI {
  async getConversations(): Promise<Conversation[]> {
    const response = await chatClient.get('/conversations');
    return response.data;
  }

  async createConversation(request: CreateConversationRequest): Promise<Conversation> {
    const response = await chatClient.post('/conversations', request);
    return response.data;
  }

  async getConversation(id: string): Promise<Conversation> {
    const response = await chatClient.get(`/conversations/${id}`);
    return response.data;
  }

  async createMessage(request: CreateMessageRequest): Promise<Message> {
    const response = await chatClient.post('/messages', request);
    return response.data;
  }
}

export const chatApi = new ChatAPI();