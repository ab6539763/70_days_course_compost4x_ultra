/**
 * 聊天面板组件 30 — Day22+ 前端模块
 */
import React, { useState } from 'react';

export function ChatPanel30() {
  const [messages, setMessages] = useState<{role: string; content: string}[]>([]);
  const [input, setInput] = useState('');

  const send = async () => {
    const res = await fetch('/api/v1/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: input, session_id: 'panel30' }),
    });
    const data = await res.json();
    setMessages((m) => [...m, { role: 'user', content: input }, { role: 'assistant', content: data.reply }]);
    setInput('');
  };

  return (
    <div className="chat-panel-30">
      <div className="messages">{messages.map((m, idx) => <div key={idx}>{m.role}: {m.content}</div>)}</div>
      <input value={input} onChange={(e) => setInput(e.target.value)} />
      <button onClick={send}>发送</button>
    </div>
  );
}
