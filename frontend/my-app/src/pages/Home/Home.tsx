import React, { useState } from "react";
import "./Home.css";

const Home: React.FC = () => {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState<{ sender: string; text: string }[]>([]);
  const [showHistory, setShowHistory] = useState(false); // Controlează afișarea istoricului

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Adaugă mesajul utilizatorului în chat
    setChatHistory((prev) => [...prev, { sender: "You", text: message }]);

    try {
      const res = await fetch("http://localhost:8000/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ user_input: message }),
      });

      const data = await res.json();

      setChatHistory((prev) => [...prev, { sender: "Bot", text: data.response }]);
    } catch (error) {
      console.error("Error sending message:", error);
      setChatHistory((prev) => [...prev, { sender: "Bot", text: "An error occurred. Please try again." }]);
    }

    setMessage(""); 
  };

  return (
    <div className="home-container">
      <button className="history-toggle" onClick={() => setShowHistory(!showHistory)}>
        {showHistory ? "Hide History" : "Show History"}
      </button>
      {showHistory && (
        <div className="history-panel">
          <h3>History</h3>
          <ul>
            {chatHistory.map((chat, index) => (
              <li key={index}>
                <strong>{chat.sender}:</strong> {chat.text}
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="chat-box">
        <div className="chat-history">
          {chatHistory.map((chat, index) => (
            <div
              key={index}
              className={`chat-message ${chat.sender === "You" ? "user-message" : "bot-message"}`}
            >
              <div className="message-content">
                <strong>{chat.sender}:</strong> {chat.text}
              </div>
            </div>
          ))}
        </div>
        <form onSubmit={handleSubmit} className="chat-form">
          <input
            type="text"
            placeholder="Write your simptoms..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            required
          />
          <button type="submit">Send</button>
        </form>
      </div>
      <div className="photo-container">
        <img src="src/assets/background.webp"/>

      </div>
    </div>
  );
};

export default Home;