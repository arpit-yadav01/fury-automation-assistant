import { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./App.css";

const API = "http://localhost:8000";

const QUICK_CMDS = [
  { label: "▶ Lofi", cmd: "visual play lofi on youtube" },
  { label: "🧩 Two Sum", cmd: "leetcode two sum" },
  { label: "💬 WhatsApp", cmd: "check whatsapp" },
  { label: "🔍 React Jobs", cmd: "search jobs react developer naukri" },
  { label: "👤 Profile", cmd: "profile" },
  { label: "🗂 Tabs", cmd: "tabs" },
  { label: "📋 History", cmd: "visual history" },
  { label: "❓ Help", cmd: "fury help" },
];

function formatOutput(text) {
  if (!text) return "";
  return text
    .replace(/✅/g, "✅ ")
    .replace(/❌/g, "❌ ")
    .replace(/🔥/g, "🔥 ")
    .trim();
}

export default function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: "fury",
      text: "🔥 Fury AI ready.\n\nTry: visual play lofi on youtube\nOr: leetcode two sum\nOr: search jobs react developer naukri\nOr: fury help",
      time: new Date().toLocaleTimeString(),
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [connected, setConnected] = useState(false);
  const [status, setStatus] = useState({});
  const messagesEnd = useRef(null);
  const inputRef = useRef(null);

  // ping backend
  useEffect(() => {
    const ping = async () => {
      try {
        const r = await axios.get(`${API}/status`, { timeout: 2000 });
        setConnected(true);
        setStatus(r.data.context || {});
      } catch {
        setConnected(false);
      }
    };
    ping();
    const iv = setInterval(ping, 4000);
    return () => clearInterval(iv);
  }, []);

  useEffect(() => {
    messagesEnd.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const addMsg = (role, text) => {
    setMessages((prev) => [
      ...prev,
      {
        id: Date.now(),
        role,
        text: formatOutput(text),
        time: new Date().toLocaleTimeString(),
      },
    ]);
  };

  const send = async (cmd) => {
    const command = (cmd || input).trim();
    if (!command || loading) return;
    setInput("");
    addMsg("user", command);
    setLoading(true);

    try {
      const r = await axios.post(
        `${API}/chat`,
        { command },
        { timeout: 120000 }
      );
      addMsg("fury", r.data.output || "✅ Done");
    } catch (e) {
      if (e.code === "ECONNABORTED") {
        addMsg("fury", "⏱ Task is running... check terminal for live progress");
      } else if (e.response?.status === 404) {
        // fallback to queue endpoint
        try {
          await axios.post(`${API}/command`, { command });
          addMsg("fury", "✅ Command queued — check terminal for output");
        } catch {
          addMsg("fury", "❌ Cannot connect to Fury backend\nRun: python dashboard_api.py");
        }
      } else {
        addMsg("fury", `❌ Error: ${e.message}`);
      }
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  };

  return (
    <div className="app">
      {/* SIDEBAR */}
      <aside className="sidebar">
        <div className="logo">
          <span className="logo-fire">🔥</span>
          <span className="logo-text">FURY</span>
          <span className="logo-sub">AI AGENT</span>
        </div>

        <div className="conn-badge" data-connected={connected}>
          <span className="conn-dot" />
          {connected ? "Connected" : "Offline"}
        </div>

        {connected && (
          <div className="ctx-panel">
            <div className="ctx-title">CONTEXT</div>
            {Object.entries(status).map(([k, v]) =>
              v ? (
                <div className="ctx-row" key={k}>
                  <span className="ctx-key">{k}</span>
                  <span className="ctx-val">{String(v).slice(0, 20)}</span>
                </div>
              ) : null
            )}
          </div>
        )}

        <div className="quick-title">QUICK</div>
        <div className="quick-list">
          {QUICK_CMDS.map((q) => (
            <button
              key={q.cmd}
              className="quick-item"
              onClick={() => send(q.cmd)}
              disabled={loading}
            >
              {q.label}
            </button>
          ))}
        </div>

        <div className="sidebar-footer">
          v1.0 · Phase 10
        </div>
      </aside>

      {/* MAIN */}
      <main className="main">
        {/* HEADER */}
        <header className="topbar">
          <div className="topbar-title">Chat</div>
          <div className="topbar-hint">
            Press <kbd>Enter</kbd> to send · <kbd>Shift+Enter</kbd> for newline
          </div>
        </header>

        {/* MESSAGES */}
        <div className="messages">
          {messages.map((m) => (
            <div key={m.id} className={`msg msg-${m.role}`}>
              {m.role === "fury" && (
                <div className="msg-avatar">F</div>
              )}
              <div className="msg-bubble">
                <pre className="msg-text">{m.text}</pre>
                <div className="msg-time">{m.time}</div>
              </div>
            </div>
          ))}

          {loading && (
            <div className="msg msg-fury">
              <div className="msg-avatar">F</div>
              <div className="msg-bubble">
                <div className="typing">
                  <span /><span /><span />
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEnd} />
        </div>

        {/* INPUT */}
        <div className="input-bar">
          <textarea
            ref={inputRef}
            className="input-field"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKey}
            placeholder="Type a command..."
            rows={1}
            disabled={loading}
          />
          <button
            className="send-btn"
            onClick={() => send()}
            disabled={loading || !input.trim()}
          >
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M2 21l21-9L2 3v7l15 2-15 2z" />
            </svg>
          </button>
        </div>
      </main>
    </div>
  );
}