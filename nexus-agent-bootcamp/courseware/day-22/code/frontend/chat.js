/**
 * Day 22 — 静态聊天前端（MOCK 模式）
 * Day 23+ 将把 API_BASE 指向 FastAPI 后端。
 */
const API_BASE = window.NEXUS_API_BASE || "";

const chatWindow = document.getElementById("chat-window");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

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

function mockReply(text) {
  if (text.includes("天气")) return "【MOCK】北京晴，26°C。";
  if (/[\d+\-*/]/.test(text)) return "【MOCK】计算功能将在后端接入。";
  if (text.includes("Nexus") || text.includes("平台"))
    return "【MOCK】NexusAgent 是智链科技的企业级智能体协作平台。";
  return `【MOCK】收到：「${text}」。Day 23 将对接真实 API。`;
}

async function fetchReply(text) {
  if (!API_BASE) return mockReply(text);
  const resp = await fetch(`${API_BASE}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text }),
  });
  if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
  const data = await resp.json();
  return data.reply || data.content || "（空回复）";
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
    const reply = await fetchReply(text);
    botBubble.classList.remove("typing");
    botBubble.textContent = reply;
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
