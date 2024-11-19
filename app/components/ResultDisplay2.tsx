"use client";

import { useState, useEffect } from "react";

interface ChatMessage {
  id: number;
  message: string;
}

export default function ResultDisplay() {
  const [chatRecord, setChatRecord] = useState<ChatMessage[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [conversationId, setConversationId] = useState<number>(0); // To track new conversations

  useEffect(() => {
    async function fetchResults(): Promise<void> {
      try {
        const res = await fetch("http://localhost:8000/results/", {
          method: "GET",
        });

        if (!res.ok) {
          throw new Error(`Failed to fetch results: ${res.status} ${res.statusText}`);
        }

        const data: { results: string } = await res.json();

        // Add the new message to the chat record
        setChatRecord((prevChatRecord) => [
          ...prevChatRecord,
          { id: prevChatRecord.length + 1, message: data.results },
        ]);
      } catch (error: unknown) {
        const message = error instanceof Error ? error.message : "Unknown error occurred";
        setError(message);
      }
    }

    // Fetch results when component mounts or conversation ID changes
    fetchResults();
  }, [conversationId]); // Trigger fetch when conversation ID changes

  const startNewConversation = () => {
    // Clear chat record and set a new conversation ID
    setChatRecord([]);
    setConversationId((prevId) => prevId + 1);
  };

  return (
    <section className="result-display">
      <h2>Chat History</h2>
      {error && <p className="error" style={{ color: "red" }}>{error}</p>}

      <div className="chat-record">
        {chatRecord.length > 0 ? (
          chatRecord.map((chat) => (
            <div key={chat.id} className="chat-message">
              <strong>Message {chat.id}:</strong> {chat.message}
            </div>
          ))
        ) : (
          <p>No messages in this conversation.</p>
        )}
      </div>

      <button onClick={startNewConversation} className="new-conversation-button">
        Start New Conversation
      </button>
    </section>
  );
}
