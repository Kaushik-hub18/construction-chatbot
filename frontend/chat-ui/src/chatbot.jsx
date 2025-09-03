import React, { useState, useRef, useEffect } from "react";

export default function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const chatEndRef = useRef(null);

  // Scroll to bottom whenever a new message is added
  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  // Handle sending user message
  const handleSend = () => {
    if (!input.trim()) return;

    // Add user message with timestamp
    setMessages((prev) => [
      ...prev,
      { text: input, isBot: false, time: new Date().toLocaleTimeString() },
    ]);

    // Call backend
    fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: input }),
    })
      .then((res) => res.json())
      .then((data) => {
        setMessages((prev) => [
          ...prev,
          { text: data.answer, isBot: true, time: new Date().toLocaleTimeString() },
        ]);
      })
      .catch(() => {
        setMessages((prev) => [
          ...prev,
          {
            text: "⚠️ Error: Could not reach server.",
            isBot: true,
            time: new Date().toLocaleTimeString(),
          },
        ]);
      });

    setInput("");
  };

  // Handle suggestion button click
  const handleSuggestionClick = (suggestedTopic) => {
    setMessages((prev) => [
      ...prev,
      { text: suggestedTopic, isBot: false, time: new Date().toLocaleTimeString() },
    ]);

    fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: suggestedTopic }),
    })
      .then((res) => res.json())
      .then((data) => {
        setMessages((prev) => [
          ...prev,
          { text: data.answer, isBot: true, time: new Date().toLocaleTimeString() },
        ]);
      })
      .catch(() => {
        setMessages((prev) => [
          ...prev,
          {
            text: "⚠️ Error: Could not reach server.",
            isBot: true,
            time: new Date().toLocaleTimeString(),
          },
        ]);
      });
  };

  // Render message with timestamp and optional suggestion button
  const renderMessage = (msg, isBot) => {
    const timeStyle = "text-xs text-gray-500 mt-1";

    if (!isBot) {
      return (
        <div className="text-right bg-gray-200 p-2 rounded-lg mb-2 inline-block">
          <div>{msg.text}</div>
          <div className={timeStyle}>{msg.time}</div>
        </div>
      );
    }

    // Check for suggestion pattern
    const suggestionMatch = msg.text.match(/\*\*(.*?)\*\*/);
    if (suggestionMatch) {
      const suggestion = suggestionMatch[1];
      return (
        <div className="text-left bg-blue-100 p-2 rounded-lg mb-2 inline-block">
          <p
            dangerouslySetInnerHTML={{
              __html: msg.text.replace(/\*\*(.*?)\*\*/, `<b>${suggestion}</b>`),
            }}
          ></p>
          <button
            onClick={() => handleSuggestionClick(suggestion)}
            className="mt-2 px-3 py-1 bg-[#004d99] text-white rounded-lg hover:bg-blue-700"
          >
            Ask about {suggestion}
          </button>
          <div className={timeStyle}>{msg.time}</div>
        </div>
      );
    }

    // Normal bot message
    return (
      <div className="text-left bg-blue-100 p-2 rounded-lg mb-2 inline-block">
        <div>{msg.text}</div>
        <div className={timeStyle}>{msg.time}</div>
      </div>
    );
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-[#004d99] text-white text-lg font-bold p-4 shadow-md rounded-b-lg">
        Construction Chatbot
      </header>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4">
        {messages.map((msg, idx) => (
          <div key={idx}>{renderMessage(msg, msg.isBot)}</div>
        ))}
        <div ref={chatEndRef}></div>
      </div>

      {/* Input Area */}
      <div className="p-4 flex gap-2 bg-white border-t">
        <input
          className="flex-1 border rounded-lg px-3 py-2"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <button
          onClick={handleSend}
          className="bg-[#004d99] text-white px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          Send
        </button>
      </div>
    </div>
  );
}
