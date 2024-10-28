// frontend/app/components/Chatbot.tsx
"use client";  // Add this directive at the top

import { useState } from 'react';

export default function Chatbot() {
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState('');

  const handlePromptChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPrompt(event.target.value);
  };

  const handleSend = async () => {
    const res = await fetch('http://localhost:8000/chatbot/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt }),
    });
    const data = await res.json();
    setResponse(data.response);
  };

  return (
    <section className="chatbot">
      <h2>AI Chatbot</h2>
      <input
        type="text"
        value={prompt}
        onChange={handlePromptChange}
        placeholder="Ask the AI anything..."
      />
      <button onClick={handleSend}>Send</button>
      <p>{response}</p>
    </section>
  );
}
