"""手写 ReAct Agent — Day39 企业增强版"""
from __future__ import annotations
import json
import re
from typing import Any, Callable, Dict, List, Optional


class ReActAgent:
    """Thought -> Action -> Observation 循环"""

    def __init__(self, llm_call: Callable[[str], str], tools: Dict[str, Callable[..., str]], max_steps: int = 10) -> None:
        self.llm_call = llm_call
        self.tools = tools
        self.max_steps = max_steps

    def _build_prompt(self, question: str, history: str) -> str:
        tool_desc = "\n".join(f"- {name}: 可调用" for name in self.tools)
        return f"""你是一个 ReAct 助手。按以下格式回答：
Thought: 思考
Action: 工具名
Action Input: JSON 参数
Observation: （系统填入）
... 重复直到能给出 Final Answer

可用工具：
{tool_desc}

历史：
{history}

问题：{question}
"""

    def run(self, question: str) -> str:
        history = ""
        for _ in range(self.max_steps):
            out = self.llm_call(self._build_prompt(question, history))
            history += out + "\n"
            if "Final Answer:" in out:
                return out.split("Final Answer:")[-1].strip()
            m = re.search(r"Action:\s*(\w+)\s*\nAction Input:\s*(.+)", out, re.DOTALL)
            if m:
                tool_name, raw_input = m.group(1), m.group(2).strip()
                if tool_name in self.tools:
                    try:
                        params = json.loads(raw_input)
                        obs = self.tools[tool_name](**params) if isinstance(params, dict) else self.tools[tool_name](params)
                    except Exception as e:
                        obs = f"工具执行错误: {e}"
                    history += f"Observation: {obs}\n"
        return "未能在最大步数内完成"
