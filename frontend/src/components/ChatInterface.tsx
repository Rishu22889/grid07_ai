import { useEffect, useRef, useState } from "react";

interface Bot {
  id: string;
  avatar: string;
  name: string;
  role: string;
}

interface Message {
  id: string;
  role: "user" | "bot";
  content: string;
  timestamp: Date;
}

interface ChatInterfaceProps {
  bot: Bot;
  onBack: () => void;
}

const API_URL = "http://localhost:5001";

export default function ChatInterface({
  bot,
  onBack,
}: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, isTyping]);

  const sendMessage = async () => {
    const text = input.trim();

    if (!text || isTyping) return;

    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: text,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsTyping(true);

    try {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          bot_id: bot.id,
          message: text,
          parent_post: "",
          comment_history: messages.map((msg) => ({
            role: msg.role,
            content: msg.content,
          })),
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();

      const botMessage: Message = {
        id: crypto.randomUUID(),
        role: "bot",
        content: data.reply,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: "bot",
          content: "Something went wrong. Please try again.",
          timestamp: new Date(),
        },
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  const formatTime = (date: Date) =>
    date.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });

  return (
    <div className="chat-page">

      {/* HEADER */}
      <header className="chat-header">

        <button
          className="back-button"
          onClick={onBack}
        >
          ←
        </button>

        <div className="chat-bot-avatar">
          {bot.avatar}
        </div>

        <div className="chat-bot-details">
          <h1>{bot.name}</h1>

          <div className="bot-status">
            <span className="status-dot" />
            <span>{bot.role}</span>
          </div>
        </div>

        <div className="header-online">
          <span className="status-dot" />
          Online
        </div>
      </header>


      {/* CHAT */}
      <main className="chat-messages">

        {messages.length === 0 && (
          <div className="chat-welcome">

            <div className="welcome-avatar">
              {bot.avatar}
            </div>

            <h2>Chat with {bot.name}</h2>

            <p>
              {bot.role}
            </p>

            <span>
              Start a conversation with this agent.
            </span>

          </div>
        )}

        {messages.map((message) => {
          const isUser = message.role === "user";

          return (
            <div
              key={message.id}
              className={`message-row ${
                isUser ? "user-row" : "bot-row"
              }`}
            >

              {!isUser && (
                <div className="message-avatar">
                  {bot.avatar}
                </div>
              )}

              <div className="message-wrapper">

                <div
                  className={`message-bubble ${
                    isUser
                      ? "user-message"
                      : "bot-message"
                  }`}
                >
                  {message.content}
                </div>

                <div className="message-time">
                  {formatTime(message.timestamp)}
                </div>

              </div>

            </div>
          );
        })}


        {/* TYPING */}
        {isTyping && (
          <div className="message-row bot-row">

            <div className="message-avatar">
              {bot.avatar}
            </div>

            <div className="typing-indicator">
              <span />
              <span />
              <span />
            </div>

          </div>
        )}

        <div ref={messagesEndRef} />

      </main>


      {/* INPUT */}
      <footer className="chat-input-container">

        <div className="chat-input-wrapper">

          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                sendMessage();
              }
            }}
            placeholder={`Message ${bot.name}...`}
            disabled={isTyping}
          />

          <button
            className="send-button"
            onClick={sendMessage}
            disabled={!input.trim() || isTyping}
          >
            ↑
          </button>

        </div>

        <div className="input-hint">
          Press Enter to send
        </div>

      </footer>

    </div>
  );
}