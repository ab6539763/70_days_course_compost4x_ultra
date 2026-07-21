/**
 * Day 24 — 对接 SSE 流式 API 的前端增强版
 */
const API_BASE = window.NEXUS_API_BASE || "";
const chatWindow = document.getElementById("chat-window");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
let sessionId = localStorage.getItem("nexus_session_id") || null;

function appendMessage(role, text) {
  const div = document.createElement("div");
  div.className = `message ${role}`;
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;
  div.appendChild(bubble);
  chatWindow.appendChild(div);
  chatWindow.scrollTop = chatWindow.scrollHeight;
  return bubble;
}

async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;
  userInput.value = "";
  sendBtn.disabled = true;
  appendMessage("user", text);
  const botBubble = appendMessage("bot", "");
  botBubble.classList.add("typing");
  try {
    const resp = await fetch(`${API_BASE}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, session_id: sessionId, stream: true }),
    });
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const reader = resp.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    botBubble.textContent = "";
    botBubble.classList.remove("typing");
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop() || "";
      for (const line of lines) {
        if (!line.startsWith("data: ")) continue;
        const data = JSON.parse(line.slice(6));
        if (data.token) {
          botBubble.textContent += data.token;
          chatWindow.scrollTop = chatWindow.scrollHeight;
        }
        if (data.session_id) {
          sessionId = data.session_id;
          localStorage.setItem("nexus_session_id", sessionId);
        }
      }
    }
  } catch (err) {
    botBubble.classList.remove("typing");
    botBubble.textContent = `请求失败: ${err.message}`;
  } finally {
    sendBtn.disabled = false;
    userInput.focus();
  }
}

sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendMessage(); }
});
userInput.focus();
