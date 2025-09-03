// src/App.js
import React, { useState, useRef, useEffect } from "react";
import axios from "axios";

function App() {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "👷 Hi — I'm your construction assistant. Ask me anything about construction." }
  ]);
  const [input, setInput] = useState("");
  const [typing, setTyping] = useState(false);
  const scrollRef = useRef(null);

  // auto-scroll to bottom when messages change
  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, typing]);

  const sendMessage = async () => {
    const text = input.trim();
    if (!text) return;

    // Add user message immediately
    const userMsg = { sender: "user", text };
    setMessages(prev => [...prev, userMsg]);
    setInput("");
    setTyping(true);

    try {
      // ✅ Updated backend URL (Render deployment)
      const res = await axios.post(
  "https://construction-chatbot-fh4v.onrender.com/chat",
  { query: text },
  { timeout: 60000 }
);


      const botText = (res.data && res.data.answer) ? res.data.answer : "⚠️ No answer returned";
      setMessages(prev => [...prev, { sender: "bot", text: botText }]);
    } catch (err) {
      console.error("Chat error:", err);
      setMessages(prev => [...prev, { sender: "bot", text: "⚠️ Error: Could not reach server." }]);
    } finally {
      setTyping(false);
    }
  };

  // handle Enter key
  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div style={{
      minHeight: "100vh",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      background: "#f3f4f6",
      padding: "20px"
    }}>
      <div style={{
        width: "100%",
        maxWidth: "720px",
        height: "80vh",
        display: "flex",
        flexDirection: "column",
        background: "#ffffff",
        borderRadius: "12px",
        boxShadow: "0 6px 20px rgba(0,0,0,0.08)",
        overflow: "hidden"
      }}>
        <header style={{
          padding: "14px 20px",
          borderBottom: "1px solid #e6e6e6",
          background: "#004d99", // ✅ Blue theme header
          color: "#fff"
        }}>
          <h2 style={{ margin: 0 }}>🏗️ Construction Assistant</h2>
          <div style={{ fontSize: "12px", opacity: 0.85 }}>Construction-only answers • Example: “What is curing?”</div>
        </header>

        <main style={{ flex: 1, overflowY: "auto", padding: "18px" }}>
          {messages.map((msg, i) => (
            <div key={i} style={{
              display: "flex",
              justifyContent: msg.sender === "user" ? "flex-end" : "flex-start",
              margin: "8px 0"
            }}>
              <div style={{
                maxWidth: "78%",
                padding: "10px 14px",
                borderRadius: "12px",
                background: msg.sender === "user" ? "#004d99" : "#f3f4f6",
                color: msg.sender === "user" ? "#fff" : "#0f172a",
                boxShadow: "0 1px 0 rgba(0,0,0,0.03)",
                lineHeight: "1.4",
                whiteSpace: "pre-wrap",
                wordBreak: "break-word"
              }}>
                <div style={{ fontSize: "13px", marginBottom: "6px", opacity: 0.9 }}>
                  <strong>{msg.sender === "user" ? "You" : "Bot"}</strong>
                </div>
                <div style={{ fontSize: "15px" }}>{msg.text}</div>
              </div>
            </div>
          ))}

          {typing && (
            <div style={{ display: "flex", justifyContent: "flex-start", marginTop: 6 }}>
              <div style={{
                padding: "8px 12px",
                borderRadius: "12px",
                background: "#f3f4f6",
                color: "#0f172a"
              }}>
                <em>⏳ Bot is typing...</em>
              </div>
            </div>
          )}

          <div ref={scrollRef} />
        </main>

        <div style={{
          padding: "12px 16px",
          borderTop: "1px solid #e6e6e6",
          display: "flex",
          gap: "8px",
          alignItems: "center",
          background: "#fff"
        }}>
          <input
            aria-label="Type your question"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about construction (cement, BOQ, curing...)"
            style={{
              flex: 1,
              padding: "10px 12px",
              borderRadius: "10px",
              border: "1px solid #e6e6e6",
              outline: "none",
              fontSize: "15px"
            }}
          />
          <button
            onClick={sendMessage}
            style={{
              padding: "10px 14px",
              borderRadius: "10px",
              border: "none",
              background: "#004d99", // ✅ Blue theme button
              color: "#fff",
              fontWeight: 600,
              cursor: "pointer"
            }}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
