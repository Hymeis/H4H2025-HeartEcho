// app/chat/page.tsx
'use client';

import { useState } from 'react';
import NavBar from '../homepage/_components/NavBar';

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    // 1. Add the user's message to the conversation immediately
    const userMsg: ChatMessage = { role: 'user', content: input.trim() };
    setMessages((prev) => [...prev, userMsg]);

    // 2. Clear the input field
    setInput('');
    setIsLoading(true);

    try {
      // 3. Post to the specialized ChatGPT endpoint
      const res = await fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMsg.content }),
      });

      if (!res.ok) {
        throw new Error(`Error from server: ${res.status} ${res.statusText}`);
      }

      const data = await res.json();
      const assistantMsg: ChatMessage = {
        role: 'assistant',
        content: data.response || 'No response found',
      };

      // 4. Append the assistant's message
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      console.error(err);
      // Optionally show an error message in the chat
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'Error: failed to get response.' },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  // Pressing Enter in the input
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="bg-black min-h-screen text-white flex flex-col">
        <NavBar />
      <div className="flex-1 max-w-3xl w-full mx-auto p-4 overflow-y-auto">
        <h1 className="text-3xl font-bold mb-4">Heart Echo Chat</h1>

        {/* Chat Messages */}
        <div className="space-y-4">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${
                msg.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              <div
                className={`rounded-md px-3 py-2 max-w-xs break-words ${
                  msg.role === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-800 text-white'
                }`}
              >
                {msg.content}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Chat Input */}
      <div className="border-t border-gray-700 p-4">
        <div className="flex items-center gap-2 max-w-3xl mx-auto">
          <input
            type="text"
            className="flex-1 rounded bg-gray-800 text-white px-3 py-2 focus:outline-none"
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isLoading}
          />
          <button
            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
            onClick={handleSendMessage}
            disabled={isLoading}
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </div>
      </div>
    </div>
  );
}
