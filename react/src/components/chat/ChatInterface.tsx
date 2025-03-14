import React, { useState, useEffect, useRef } from 'react';
import { chatApi, Conversation, Message } from '../../lib/api/chat';
import { useAuth } from '../../hooks/useAuth';

export const ChatInterface: React.FC = () => {
  const { user, isLoading } = useAuth();
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [currentConversation, setCurrentConversation] = useState<Conversation | null>(null);
  const [messageInput, setMessageInput] = useState('');
  const [isLoadingMessages, setIsLoadingMessages] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [currentConversation?.messages]);

  useEffect(() => {
    const loadConversations = async () => {
      if (!user || isLoading) return;
      
      try {
        const userConversations = await chatApi.getConversations(user.id);
        setConversations(userConversations);
      } catch (error) {
        console.error('Failed to load conversations:', error);
      }
    };

    loadConversations();
  }, [user, isLoading]);

  const handleCreateConversation = async () => {
    if (!user || isLoading) return;
    
    try {
      const conversation = await chatApi.createConversation({
        userId: user.id,
        title: 'New Conversation'
      });
      setConversations([...conversations, conversation]);
      setCurrentConversation(conversation);
    } catch (error) {
      console.error('Failed to create conversation:', error);
    }
  };

  const handleSendMessage = async () => {
    if (!currentConversation || !user || !messageInput.trim() || isLoading) return;

    setIsLoadingMessages(true);
    try {
      const response = await chatApi.sendMessage(currentConversation.id, {
        userId: user.id,
        content: messageInput.trim()
      });

      const updatedConversation = {
        ...currentConversation,
        messages: [
          ...(currentConversation.messages || []),
          response.user_message,
          response.assistant_message
        ]
      };

      setCurrentConversation(updatedConversation);
      setMessageInput('');
    } catch (error) {
      console.error('Failed to send message:', error);
    } finally {
      setIsLoadingMessages(false);
    }
  };

  return (
    <div className="flex h-full">
      {/* Sidebar */}
      <div className="w-64 bg-gray-100 p-4 border-r">
        <button
          onClick={handleCreateConversation}
          className="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 mb-4"
        >
          New Conversation
        </button>
        <div className="space-y-2">
          {conversations.map((conv) => (
            <button
              key={conv.id}
              onClick={() => setCurrentConversation(conv)}
              className={`w-full text-left p-2 rounded ${
                currentConversation?.id === conv.id
                  ? 'bg-blue-100 text-blue-800'
                  : 'hover:bg-gray-200'
              }`}
            >
              {conv.title}
            </button>
          ))}
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 flex flex-col">
        {currentConversation ? (
          <>
            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {currentConversation.messages?.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${
                    message.role === 'user' ? 'justify-end' : 'justify-start'
                  }`}
                >
                  <div
                    className={`max-w-[70%] rounded-lg p-3 ${
                      message.role === 'user'
                        ? 'bg-blue-500 text-white'
                        : 'bg-gray-100 text-gray-800'
                    }`}
                  >
                    {message.content}
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="border-t p-4">
              <div className="flex space-x-2">
                <input
                  type="text"
                  value={messageInput}
                  onChange={(e) => setMessageInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                  placeholder="Type your message..."
                  className="flex-1 border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  disabled={isLoadingMessages}
                />
                <button
                  onClick={handleSendMessage}
                  disabled={isLoadingMessages || !messageInput.trim()}
                  className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isLoadingMessages ? 'Sending...' : 'Send'}
                </button>
              </div>
            </div>
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center text-gray-500">
            Select a conversation or create a new one
          </div>
        )}
      </div>
    </div>
  );
}; 