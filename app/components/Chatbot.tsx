"use client";

import { useState } from 'react';

export default function Chatbot() {
  const [prompt, setPrompt] = useState<string>('');
  const [response, setResponse] = useState<string>('');
  const [error, setError] = useState<string | null>(null);

  const handlePromptChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPrompt(event.target.value);
  };

  const handleSend = async () => {
    setError(null);
    setResponse('');

    if (!prompt.trim()) {
      setError('Prompt cannot be empty.');
      return;
    }

    try {
      const res = await fetch('http://localhost:8000/chatbot/', {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });

      if (!res.ok) {
        throw new Error(`Failed to send prompt: ${res.status} ${res.statusText}`);
      }

      const data: { response: string } = await res.json();
      setResponse(data.response);
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : 'Unknown error occurred';
      setError(message);
    }
  };

  return (
    <section className="chatbot">
      <h2>AI Chatbot</h2>
      <input
        type="text"
        value={prompt}
        onChange={handlePromptChange}
        placeholder="Ask the AI anything..."
        className="chatbot-input"
      />
      <button onClick={handleSend} className="chatbot-button">
        Send
      </button>
      {error && <p className="error" style={{ color: 'red' }}>{error}</p>}
      {response && <p className="response">{response}</p>}
    </section>
  );
}
