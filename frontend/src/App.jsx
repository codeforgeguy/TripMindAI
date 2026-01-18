import { useEffect, useRef, useState } from "react";
import "./fonts.css";

function App() {
  useEffect(() => {
    document.title = "TripMind AI";
  }, []);
  const API_URL = import.meta.env.VITE_API_URL;
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([
    { role: "bot", text: "👋 Hi! Where would you like to travel?" }
  ]);
  const [loading, setLoading] = useState(false);

  const chatEndRef = useRef(null);
  const streamRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  /* ================= SAFE STREAMING ================= */

  function streamText(fullText) {
    if (!fullText || typeof fullText !== "string") {
      setMessages(prev => [
        ...prev,
        { role: "bot", text: "⚠️ I had trouble responding. Please retry." }
      ]);
      setLoading(false);
      return;
    }

    if (streamRef.current) {
      clearInterval(streamRef.current);
      streamRef.current = null;
    }

    let index = 0;
    setMessages(prev => [...prev, { role: "bot", text: "" }]);

    streamRef.current = setInterval(() => {
      index++;

      setMessages(prev => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          ...updated[updated.length - 1],
          text: fullText.slice(0, index)
        };
        return updated;
      });

      if (index >= fullText.length) {
        clearInterval(streamRef.current);
        streamRef.current = null;
        setLoading(false);
      }
    }, 18);
  }

  /* ================= SEND MESSAGE ================= */

  async function sendMessage() {
    if (!input.trim() || loading) return;

    const userMsg = { role: "user", text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("https://tripmindai.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMsg.text })
      });

      const data = await res.json();
      streamText(data.reply);
    } catch {
      streamText("❌ Server error. Please try again.");
    }
  }

  return (
    <div style={styles.page}>
      <div style={styles.card}>

        {/* Header */}
        <div style={styles.header}>
          🌈 TripMind AI
        </div>

        {/* Chat */}
        <div style={styles.chat}>
          {messages.map((m, i) => (
            <div
              key={i}
              style={{
                ...styles.message,
                whiteSpace: "pre-line",
                ...(m.role === "user"
                  ? styles.user
                  : styles.bot)
              }}
            >
              {m.text}
            </div>
          ))}

          {loading && (
            <div style={{ ...styles.message, ...styles.bot }}>
              ✨ Planning...
            </div>
          )}

          <div ref={chatEndRef} />
        </div>

        {/* Input */}
        <div style={styles.inputBar}>
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === "Enter" && sendMessage()}
            placeholder="Ask about your trip..."
            style={styles.input}
          />
          <button onClick={sendMessage} disabled={loading} style={styles.button}>
            Send
          </button>
        </div>

      </div>
    </div>
  );
}

/* ================= STYLES ================= */

const styles = {
  page: {
    height: "100vh",
    width: "100vw",
    background: `
      linear-gradient(rgba(0,0,0,0.25), rgba(0,0,0,0.25)),
      url("/img.jpg")
    `,
    backgroundSize: "cover",
    backgroundPosition: "center",
    display: "flex",
    alignItems: "center",
    justifyContent: "center"
  },
  card: {
    width: "100%",
    maxWidth: 650,
    height: "100%",
    maxHeight: 605,
    borderRadius: 20,
    display: "flex",
    flexDirection: "column",
    backdropFilter: "blur(16px)",
    boxShadow: "0 30px 80px rgba(0,0,0,0.35)",
    overflow: "hidden"
  },
  header: {
    padding: "16px 20px",
    fontSize: 20,
    fontWeight: "bold",
    color: "#111"
  },
  chat: {
    flex: 1,
    padding: 20,
    overflowY: "auto",
    display: "flex",
    flexDirection: "column",
    gap: 12,
    scrollbarWidth: "thin"
  },
  message: {
    maxWidth: "70%",
    padding: "14px 18px",
    borderRadius: 18,
    fontSize: 15,
    lineHeight: 1.6,
    boxShadow: "0 6px 20px rgba(0,0,0,0.08)",
    animation: "fadeIn 0.3s ease-in-out"
  },
  user: {
    alignSelf: "flex-end",
    borderBottomRightRadius: 4,
    background: "#667eea",
    color: "#fff"
  },
  bot: {
    alignSelf: "flex-start",
    borderBottomLeftRadius: 4,
    background: "#e4e7f2",
    color: "#111"
  },
  inputBar: {
    display: "flex",
    padding: 12,
    gap: 10
  },
  input: {
    flex: 1,
    padding: "12px 14px",
    fontSize: 15,
    borderRadius: 10,
    outline: "none",
    border: "1px solid #ccc",
    background: "#fff",
    color: "#111"
  },
  button: {
    padding: "0 20px",
    borderRadius: 10,
    border: "none",
    /*background: "#6366f1",*/
    background: "black",
    color: "#fff",
    cursor: "pointer"
  }
};

export default App;
