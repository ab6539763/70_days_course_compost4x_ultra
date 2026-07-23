"""
NexusAgent 训练营 — 第二周（Day 8-14）课件定义
主题：面向对象、模块包、文件 IO、网络 API、装饰器异步、阶段项目 CLI 助手
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class DayPlan:
    """单日课件计划，与 generate_courseware.DayPlan 字段保持一致。"""

    day: int
    title: str
    phase: str
    epic: str
    jira_stories: list[str]
    morning: list[str]
    afternoon: list[str]
    evening: list[str]
    code_files: dict[str, str]
    homework_desc: str
    homework_answer_hint: str
    architecture_mermaid: str
    narration: str
    key_concepts: list[str]
    platform_touches: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Day 8 — OOP 上：ChatMessage 类
# ---------------------------------------------------------------------------

_DAY08_CHAT_MESSAGE = '''#!/usr/bin/env python3
"""
Day 8 示例：ChatMessage 类 —— 对话消息的领域模型

在企业级大模型应用中，每一条用户/助手消息都需要被结构化存储，
以便后续做历史记录、Token 统计、审计日志等。本模块定义最基础的消息实体。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class MessageRole(str, Enum):
    """消息角色枚举，与 OpenAI Chat Completions API 的 role 字段对齐。"""

    SYSTEM = "system"      # 系统提示词，设定 AI 行为
    USER = "user"          # 终端用户输入
    ASSISTANT = "assistant"  # 模型回复
    TOOL = "tool"          # 工具调用结果（Day 40+ 会用到）


@dataclass
class ChatMessage:
    """
    单条聊天消息的领域对象。

    属性:
        role: 消息角色（system/user/assistant/tool）
        content: 消息正文，纯文本
        timestamp: 消息创建时间，默认取当前时间
        metadata: 扩展字段，如 token 数、模型名称、trace_id 等
    """

    role: MessageRole
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """构造后校验：确保 role 为枚举类型、content 非空。"""
        # 允许传入字符串形式的 role，自动转换为枚举
        if isinstance(self.role, str):
            self.role = MessageRole(self.role)
        if not self.content or not self.content.strip():
            raise ValueError("消息内容 content 不能为空")

    def to_dict(self) -> dict[str, Any]:
        """序列化为字典，便于 JSON 存储或 API 传输。"""
        return {
            "role": self.role.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ChatMessage:
        """从字典反序列化，用于读取历史记录文件。"""
        ts = data.get("timestamp")
        if isinstance(ts, str):
            timestamp = datetime.fromisoformat(ts)
        else:
            timestamp = datetime.now()
        return cls(
            role=MessageRole(data["role"]),
            content=data["content"],
            timestamp=timestamp,
            metadata=data.get("metadata", {}),
        )

    def word_count(self) -> int:
        """粗略统计字数（中文按字符、英文按空格分词）。"""
        # 简单实现：去除首尾空白后按空白切分
        return len(self.content.split())

    def preview(self, max_len: int = 50) -> str:
        """生成消息预览，用于 CLI 历史列表展示。"""
        text = self.content.replace("\\n", " ")
        if len(text) <= max_len:
            return text
        return text[: max_len - 3] + "..."

    def __repr__(self) -> str:
        return (
            f"ChatMessage(role={self.role.value!r}, "
            f"content={self.preview(30)!r}, "
            f"timestamp={self.timestamp:%Y-%m-%d %H:%M})"
        )


def demo() -> None:
    """演示 ChatMessage 的基本用法。"""
    # 1. 创建用户消息
    user_msg = ChatMessage(role=MessageRole.USER, content="你好，请介绍一下 NexusAgent 平台。")
    print("用户消息:", user_msg)
    print("字数:", user_msg.word_count())

    # 2. 创建助手回复，附带 metadata
    assistant_msg = ChatMessage(
        role=MessageRole.ASSISTANT,
        content="NexusAgent 是智链科技的企业级智能体协作平台，支持多轮对话与知识库问答。",
        metadata={"model": "qwen-plus", "tokens": 42},
    )
    print("助手消息:", assistant_msg)

    # 3. 序列化与反序列化
    payload = user_msg.to_dict()
    restored = ChatMessage.from_dict(payload)
    print("反序列化成功:", restored.role == user_msg.role)

    # 4. 批量消息列表（后续 Day 14 会用于对话历史）
    history: list[ChatMessage] = [user_msg, assistant_msg]
    print(f"\\n对话历史共 {len(history)} 条:")
    for i, msg in enumerate(history, 1):
        print(f"  [{i}] {msg.role.value}: {msg.preview()}")


if __name__ == "__main__":
    demo()
'''

DAY_08 = DayPlan(
    day=8,
    title="OOP 上：类与对象 — ChatMessage 领域模型",
    phase="第一阶段:Python编程基础",
    epic="NEXUS-E1",
    jira_stories=["NEXUS-801", "NEXUS-802", "NEXUS-803"],
    morning=[
        "09:00 站会：回顾 Day 7 函数与数据结构，引出「消息对象」需求",
        "09:30 理论：类、对象、属性、方法、`__init__` 与 `self`",
        "10:30 理论：`@dataclass`、枚举 Enum、类型注解入门",
        "11:00 跟敲 chat_message.py：定义 MessageRole 与 ChatMessage",
    ],
    afternoon=[
        "14:00 实现 to_dict / from_dict 序列化方法",
        "15:00 添加 word_count、preview 等业务方法",
        "16:00 单元测试思维：构造合法/非法消息，观察异常",
        "17:00 Code Review：命名规范、docstring 完整性检查",
    ],
    evening=[
        "19:00 作业：扩展 ChatMessage 支持 `is_empty()` 与 `merge()`",
        "20:00 预习 Day 9 继承与多态，阅读 OpenAI API 消息格式文档",
    ],
    code_files={"chat_message.py": _DAY08_CHAT_MESSAGE},
    homework_desc="""\
在 `homework/chat_message_ext.py` 中扩展 ChatMessage：

1. 实现 `is_empty()`：判断 content 是否仅含空白字符
2. 实现 `merge(other: ChatMessage) -> ChatMessage`：合并两条同 role 消息（content 用换行拼接）
3. 实现 `format_for_api() -> dict`：仅返回 `{"role": ..., "content": ...}`，供 LLM API 调用
4. 编写 `if __name__ == "__main__"` 演示上述三个方法
""",
    homework_answer_hint="""\
```python
# homework/chat_message_ext.py 参考答案
from chat_message import ChatMessage, MessageRole

class ChatMessageExt(ChatMessage):
    def is_empty(self) -> bool:
        return not self.content.strip()

    def merge(self, other: ChatMessage) -> ChatMessage:
        if self.role != other.role:
            raise ValueError("只能合并相同 role 的消息")
        return ChatMessage(
            role=self.role,
            content=self.content + "\\n" + other.content,
            metadata={**self.metadata, **other.metadata},
        )

    def format_for_api(self) -> dict:
        return {"role": self.role.value, "content": self.content}

if __name__ == "__main__":
    m1 = ChatMessage(MessageRole.USER, "你好")
    m2 = ChatMessage(MessageRole.USER, "请继续")
    merged = m1.merge(m2)
    print(merged.format_for_api())
    print("is_empty:", ChatMessage(MessageRole.USER, "   ").is_empty())
```
""",
    architecture_mermaid="""\
flowchart LR
    USER[用户输入] --> CM[ChatMessage]
    CM --> DICT[to_dict]
    DICT --> JSON[(JSON 文件)]
    JSON --> FROM[from_dict]
    FROM --> CM
    CM --> API[format_for_api]
    API --> LLM[LLM API Day12+]
""",
    narration="""\
**林悦（产品经理）**：陈工，昨天我们把对话历史用列表存了，但每条消息还是裸字典，字段名经常写错。今天能不能定义一个「消息类」？

**陈工（Tech Lead）**：可以。我们引入 `ChatMessage` 领域模型，把 role、content、timestamp 封装起来。这是面向对象的第一步——用类表达业务概念，而不是到处传 dict。

**小王（后端）**：跟 OpenAI 的 messages 数组格式对齐吗？

**陈工**：对。`format_for_api()` 只输出 API 需要的字段，内部 metadata 自己留着做审计。今天先把类写好，Day 14 阶段项目会直接复用。

**测试小李**：空 content 要抛异常，避免脏数据进历史。

**陈工**：`__post_init__` 里做校验，企业代码不能信任外部输入。下午大家跟敲，17:00 我逐行 Review。
""",
    key_concepts=[
        "类与对象：用 class 封装数据与行为",
        "__init__ 构造方法与 self",
        "@dataclass 减少样板代码",
        "Enum 枚举类型约束取值",
        "__post_init__ 构造后校验",
        "实例方法 vs 类方法 from_dict",
        "序列化 to_dict / 反序列化",
        "__repr__ 调试友好输出",
        "领域模型 Domain Model 思想",
    ],
    platform_touches=[
        "NexusAgent 对话服务底层消息实体，对应 platform/nexus_agent/schemas/message.py 雏形",
        "为 Day 14 CLI 助手的历史持久化打基础",
        "与 OpenAI Chat Completions messages 格式对齐",
    ],
)


# ---------------------------------------------------------------------------
# Day 9 — OOP 下：模型继承体系
# ---------------------------------------------------------------------------

_DAY09_BASE_MODEL = '''#!/usr/bin/env python3
"""
Day 9 示例：BaseModel 抽象基类 —— 统一大模型调用接口

企业里往往对接多家模型供应商（OpenAI、通义千问、DeepSeek 等），
通过继承抽象出统一接口，上层业务代码无需关心具体厂商实现。
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ModelResponse:
    """模型调用的统一响应结构。"""

    content: str
    model_name: str
    usage: dict[str, int] = field(default_factory=dict)  # prompt_tokens, completion_tokens 等
    raw: dict[str, Any] = field(default_factory=dict)    # 原始 API 响应，调试用


class BaseModel(ABC):
    """
    大语言模型抽象基类。

    子类必须实现 chat() 方法。基类提供公共属性与工具方法。
    """

    def __init__(self, model_name: str, api_key: str = "", **kwargs: Any) -> None:
        self.model_name = model_name
        self.api_key = api_key
        self.extra_config = kwargs

    @abstractmethod
    def chat(self, messages: list[dict[str, str]], **kwargs: Any) -> ModelResponse:
        """
        发送多轮对话请求。

        Args:
            messages: [{"role": "user", "content": "..."}, ...]
        Returns:
            ModelResponse 统一响应对象
        """
        ...

    def validate_messages(self, messages: list[dict[str, str]]) -> None:
        """校验消息列表格式，子类可在 chat 开头调用。"""
        if not messages:
            raise ValueError("messages 不能为空")
        for msg in messages:
            if "role" not in msg or "content" not in msg:
                raise ValueError(f"消息缺少 role 或 content: {msg}")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(model={self.model_name!r})"
'''

_DAY09_OPENAI_MODEL = '''#!/usr/bin/env python3
"""
Day 9 示例：OpenAIModel —— 继承 BaseModel，模拟 OpenAI 兼容接口

实际项目中可替换为真实 requests 调用；本日侧重继承与多态演示。
"""
from __future__ import annotations

from typing import Any

from base_model import BaseModel, ModelResponse


class OpenAIModel(BaseModel):
    """OpenAI 及兼容 API（如 DeepSeek）的模型实现。"""

    def __init__(
        self,
        model_name: str = "gpt-4o-mini",
        api_key: str = "",
        base_url: str = "https://api.openai.com/v1",
        **kwargs: Any,
    ) -> None:
        super().__init__(model_name, api_key, **kwargs)
        self.base_url = base_url

    def chat(self, messages: list[dict[str, str]], **kwargs: Any) -> ModelResponse:
        """模拟调用 OpenAI Chat Completions API。"""
        self.validate_messages(messages)

        # 模拟 API 响应（Day 12 会改为真实 HTTP 请求）
        last_user = next(
            (m["content"] for m in reversed(messages) if m["role"] == "user"),
            "",
        )
        fake_reply = f"[OpenAI/{self.model_name}] 收到: {last_user[:50]}"

        return ModelResponse(
            content=fake_reply,
            model_name=self.model_name,
            usage={"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
            raw={"id": "chatcmpl-mock-openai", "object": "chat.completion"},
        )


if __name__ == "__main__":
    model = OpenAIModel(model_name="gpt-4o-mini", api_key="sk-mock")
    resp = model.chat([{"role": "user", "content": "你好"}])
    print(resp.content)
    print("usage:", resp.usage)
'''

_DAY09_QWEN_MODEL = '''#!/usr/bin/env python3
"""
Day 9 示例：QwenModel —— 通义千问模型实现，演示多态

与 OpenAIModel 继承同一基类，上层可用 BaseModel 类型统一调度。
"""
from __future__ import annotations

from typing import Any

from base_model import BaseModel, ModelResponse


class QwenModel(BaseModel):
    """阿里云通义千问 DashScope API 模型实现。"""

    def __init__(
        self,
        model_name: str = "qwen-plus",
        api_key: str = "",
        **kwargs: Any,
    ) -> None:
        super().__init__(model_name, api_key, **kwargs)

    def chat(self, messages: list[dict[str, str]], **kwargs: Any) -> ModelResponse:
        """模拟调用通义千问 API。"""
        self.validate_messages(messages)

        last_user = next(
            (m["content"] for m in reversed(messages) if m["role"] == "user"),
            "",
        )
        # 通义千问风格的模拟回复
        fake_reply = f"[通义千问/{self.model_name}] 您好！关于「{last_user[:30]}」，我来为您解答。"

        return ModelResponse(
            content=fake_reply,
            model_name=self.model_name,
            usage={"input_tokens": 15, "output_tokens": 25},
            raw={"request_id": "mock-qwen-req-001"},
        )


def demo_polymorphism() -> None:
    """多态演示：同一函数处理不同子类。"""
    from openai_model import OpenAIModel

    models: list[BaseModel] = [
        OpenAIModel("gpt-4o-mini"),
        QwenModel("qwen-plus"),
    ]
    messages = [{"role": "user", "content": "什么是 RAG？"}]

    print("=== 多态调用 demo ===")
    for m in models:
        resp = m.chat(messages)
        print(f"{m} -> {resp.content}")


if __name__ == "__main__":
    demo_polymorphism()
'''

_DAY09_DEMO = '''#!/usr/bin/env python3
"""Day 9 综合演示：模型工厂与多态调度。"""
from __future__ import annotations

from base_model import BaseModel
from openai_model import OpenAIModel
from qwen_model import QwenModel


def create_model(provider: str, **kwargs) -> BaseModel:
    """
    简单工厂：根据 provider 字符串创建对应模型实例。

    企业实践中可扩展为注册表模式（Day 39 Agent 工具注册同理）。
    """
    registry: dict[str, type[BaseModel]] = {
        "openai": OpenAIModel,
        "qwen": QwenModel,
    }
    cls = registry.get(provider.lower())
    if cls is None:
        raise ValueError(f"未知 provider: {provider}，可选: {list(registry)}")
    return cls(**kwargs)


if __name__ == "__main__":
    for provider in ("openai", "qwen"):
        model = create_model(provider, model_name="default")
        r = model.chat([{"role": "user", "content": "讲个笑话"}])
        print(r.content)
'''

DAY_09 = DayPlan(
    day=9,
    title="OOP 下：继承、抽象类与多态 — 模型适配层",
    phase="第一阶段:Python编程基础",
    epic="NEXUS-E1",
    jira_stories=["NEXUS-901", "NEXUS-902", "NEXUS-903"],
    morning=[
        "09:00 站会：演示昨日 ChatMessage MR，今日目标「多模型统一接口」",
        "09:30 理论：继承、super()、方法重写 override",
        "10:30 理论：ABC 抽象基类、@abstractmethod",
        "11:00 跟敲 base_model.py 与 openai_model.py",
    ],
    afternoon=[
        "14:00 实现 qwen_model.py，对比两家 API 差异",
        "15:00 多态 demo：list[BaseModel] 统一遍历调用",
        "16:00 简单工厂 create_model(provider)",
        "17:00 Review：里氏替换原则 LSP，子类能否替换父类",
    ],
    evening=[
        "19:00 作业：新增 DeepSeekModel 子类",
        "20:00 阅读通义千问 DashScope 官方文档 API 章节",
    ],
    code_files={
        "base_model.py": _DAY09_BASE_MODEL,
        "openai_model.py": _DAY09_OPENAI_MODEL,
        "qwen_model.py": _DAY09_QWEN_MODEL,
        "model_factory_demo.py": _DAY09_DEMO,
    },
    homework_desc="""\
新增 `homework/deepseek_model.py`：

1. 继承 `BaseModel`，实现 `chat()` 方法
2. 模拟回复格式：`[DeepSeek/{model}] ...`
3. 在 `model_factory_demo.py` 中注册 `deepseek` provider
4. 写测试：传入非法 messages 应抛出 ValueError
""",
    homework_answer_hint="""\
```python
# homework/deepseek_model.py
from base_model import BaseModel, ModelResponse

class DeepSeekModel(BaseModel):
    def chat(self, messages, **kwargs):
        self.validate_messages(messages)
        last = next(m["content"] for m in reversed(messages) if m["role"] == "user")
        return ModelResponse(
            content=f"[DeepSeek/{self.model_name}] {last}",
            model_name=self.model_name,
            usage={"total_tokens": 50},
        )
```
""",
    architecture_mermaid="""\
classDiagram
    class BaseModel {
        <<abstract>>
        +model_name: str
        +api_key: str
        +chat(messages)* ModelResponse
        +validate_messages(messages)
    }
    class OpenAIModel {
        +base_url: str
        +chat(messages) ModelResponse
    }
    class QwenModel {
        +chat(messages) ModelResponse
    }
    BaseModel <|-- OpenAIModel
    BaseModel <|-- QwenModel
    BaseModel --> ModelResponse
""",
    narration="""\
**林悦**：产品要支持「模型切换」——客户 A 用通义，客户 B 用 OpenAI。不能每换一个模型就改一遍业务代码吧？

**陈工**：今天用继承搞定。`BaseModel` 定义统一 `chat()` 接口，`OpenAIModel`、`QwenModel` 各自实现。上层只认 `BaseModel` 类型，这就是依赖倒置。

**小王**：抽象类 ABC 和普通父类有啥区别？

**陈工**：ABC 强制子类实现 `chat()`，漏写就实例化报错。企业里接口契约要硬，不能靠自觉。

**架构老张**：这个适配层以后放 `platform/nexus_agent/llm/`，今天先在课件里练手。下午加工厂方法，字符串配置就能切模型。

**测试小李**：我会测子类能不能当父类用——多态对不对，LSP 原则。
""",
    key_concepts=[
        "继承 extends 与 super() 调用父类",
        "方法重写 override",
        "ABC 抽象基类与 @abstractmethod",
        "多态：父类引用指向子类对象",
        "里氏替换原则 LSP",
        "简单工厂模式 create_model",
        "ModelResponse 统一响应 DTO",
        "validate_messages 公共校验逻辑",
        "依赖倒置：业务依赖抽象不依赖具体",
    ],
    platform_touches=[
        "platform/nexus_agent/llm/base.py 适配层原型",
        "配置化模型切换，为 Day 12 真实 API 调用铺路",
        "多租户场景下按客户选择不同 LLM Provider",
    ],
)


# ---------------------------------------------------------------------------
# Day 10 — 模块、包与异常
# ---------------------------------------------------------------------------

_DAY10_INIT = '''"""
nexus_cli — 智链科技 Nexus 命令行工具包（Day 10 教学示例）

包结构说明:
    nexus_cli/
    ├── __init__.py      # 包入口，导出公共 API
    ├── __main__.py      # python -m nexus_cli 入口
    ├── commands.py      # 子命令实现
    ├── utils.py         # 工具函数
    └── exceptions.py    # 自定义异常层次
"""
from nexus_cli.commands import run_greet, run_version
from nexus_cli.exceptions import NexusCLIError

__version__ = "0.1.0"
__all__ = ["run_greet", "run_version", "NexusCLIError", "__version__"]
'''

_DAY10_MAIN = '''#!/usr/bin/env python3
"""
包模块入口：python -m nexus_cli

Python 通过 __main__.py 支持将包作为脚本运行。
"""
from __future__ import annotations

import sys

from nexus_cli.commands import dispatch
from nexus_cli.exceptions import NexusCLIError


def main(argv: list[str] | None = None) -> int:
    """CLI 主函数，返回进程退出码（0=成功，非0=失败）。"""
    argv = argv if argv is not None else sys.argv[1:]
    try:
        return dispatch(argv)
    except NexusCLIError as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\\n已取消", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
'''

_DAY10_COMMANDS = '''"""nexus_cli 子命令实现模块。"""
from __future__ import annotations

import argparse

from nexus_cli import __version__
from nexus_cli.exceptions import CommandNotFoundError
from nexus_cli.utils import banner, validate_name


def run_greet(name: str) -> None:
    """greet 子命令：向指定用户问好。"""
    validate_name(name)
    print(banner())
    print(f"你好，{name}！欢迎使用 Nexus CLI v{__version__}")


def run_version() -> None:
    """version 子命令：打印版本号。"""
    print(f"nexus_cli/{__version__}")


def build_parser() -> argparse.ArgumentParser:
    """构建 argparse 解析器，定义子命令。"""
    parser = argparse.ArgumentParser(prog="nexus_cli", description="Nexus 命令行工具")
    sub = parser.add_subparsers(dest="command", required=True)

    greet_p = sub.add_parser("greet", help="问候用户")
    greet_p.add_argument("name", help="用户名")

    sub.add_parser("version", help="显示版本")

    return parser


def dispatch(argv: list[str]) -> int:
    """根据 argv 分发到对应子命令处理函数。"""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "greet":
        run_greet(args.name)
    elif args.command == "version":
        run_version()
    else:
        raise CommandNotFoundError(args.command)
    return 0
'''

_DAY10_UTILS = '''"""nexus_cli 工具函数。"""
from __future__ import annotations

from nexus_cli.exceptions import ValidationError


def banner() -> str:
    """返回 ASCII 品牌横幅。"""
    return """
╔══════════════════════════════════╗
║     NexusAgent CLI  v0.1         ║
║     智链科技 SmartLink Tech      ║
╚══════════════════════════════════╝
""".strip()


def validate_name(name: str) -> None:
    """校验用户名：非空、长度 2-20、仅字母数字下划线中文。"""
    if not name or not name.strip():
        raise ValidationError("用户名不能为空")
    if len(name) > 20:
        raise ValidationError("用户名不能超过 20 个字符")
'''

_DAY10_EXCEPTIONS = '''"""nexus_cli 自定义异常层次。

企业代码应使用语义化异常，便于上层统一捕获与日志分类。
"""
from __future__ import annotations


class NexusCLIError(Exception):
    """所有 Nexus CLI 异常的基类。"""

    def __init__(self, message: str, code: str = "NEXUS_CLI_ERROR") -> None:
        super().__init__(message)
        self.message = message
        self.code = code


class ValidationError(NexusCLIError):
    """输入校验失败。"""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="VALIDATION_ERROR")


class CommandNotFoundError(NexusCLIError):
    """未知子命令。"""

    def __init__(self, command: str) -> None:
        super().__init__(f"未知命令: {command}", code="COMMAND_NOT_FOUND")
        self.command = command
'''

_DAY10_DEMO = '''#!/usr/bin/env python3
"""
Day 10 演示：以包方式运行 nexus_cli

在 code/ 目录下执行:
    python -m nexus_cli greet 张三
    python -m nexus_cli version
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent


def run(cmd: list[str]) -> None:
    print(f"$ {' '.join(cmd)}")
    subprocess.run(cmd, cwd=CODE_DIR, check=False)
    print()


if __name__ == "__main__":
    py = sys.executable
    run([py, "-m", "nexus_cli", "greet", "林悦"])
    run([py, "-m", "nexus_cli", "version"])
    # 触发 ValidationError
    run([py, "-m", "nexus_cli", "greet", ""])
'''

DAY_10 = DayPlan(
    day=10,
    title="模块、包与异常 — nexus_cli 包结构",
    phase="第一阶段:Python编程基础",
    epic="NEXUS-E1",
    jira_stories=["NEXUS-1001", "NEXUS-1002", "NEXUS-1003"],
    morning=[
        "09:00 站会：昨日模型适配层合并 develop，今日打包成可安装 CLI",
        "09:30 理论：import 机制、模块搜索路径 sys.path",
        "10:30 理论：包 package、`__init__.py`、`__all__`",
        "11:00 跟敲 nexus_cli 目录结构与 exceptions 层次",
    ],
    afternoon=[
        "14:00 实现 commands.py 与 argparse 子命令",
        "14:30 实现 __main__.py，掌握 python -m 运行方式",
        "16:00 异常处理：自定义异常 vs 裸 except",
        "17:00 演示：故意触发 ValidationError 观察退出码",
    ],
    evening=[
        "19:00 作业：新增 `echo` 子命令",
        "20:00 阅读 PEP 8 导入顺序规范",
    ],
    code_files={
        "nexus_cli/__init__.py": _DAY10_INIT,
        "nexus_cli/__main__.py": _DAY10_MAIN,
        "nexus_cli/commands.py": _DAY10_COMMANDS,
        "nexus_cli/utils.py": _DAY10_UTILS,
        "nexus_cli/exceptions.py": _DAY10_EXCEPTIONS,
        "run_package_demo.py": _DAY10_DEMO,
    },
    homework_desc="""\
扩展 nexus_cli 包：

1. 新增 `echo` 子命令：`python -m nexus_cli echo hello world` 原样输出
2. 在 exceptions.py 新增 `ConfigError`，用于配置文件缺失场景
3. 编写 `try/except` 演示捕获 `NexusCLIError` 及其子类
""",
    homework_answer_hint="""\
```python
# commands.py 中添加
def run_echo(text: str) -> None:
    print(text)

# build_parser 中
echo_p = sub.add_parser("echo")
echo_p.add_argument("text", nargs="+")

# dispatch 中
elif args.command == "echo":
    run_echo(" ".join(args.text))
```
""",
    architecture_mermaid="""\
flowchart TB
    MAIN[python -m nexus_cli] --> DISPATCH[dispatch]
    DISPATCH --> GREET[greet]
    DISPATCH --> VER[version]
    GREET --> UTILS[utils.validate_name]
    UTILS -->|失败| VAL_ERR[ValidationError]
    DISPATCH -->|未知命令| CMD_ERR[CommandNotFoundError]
    VAL_ERR --> EXIT[退出码 1]
""",
    narration="""\
**陈工**：昨天模型类散在三个文件里，import 路径乱七八糟。今天把它们组织成标准 Python 包 `nexus_cli`。

**小王**：`__init__.py` 一定要写吗？Python 3.3 不是有 namespace package？

**陈工**：教学项目和平台代码我们统一显式 `__init__.py`，导出 `__all__`，IDE 自动补全才好用。`python -m nexus_cli` 是以后平台 CLI 的标准启动方式。

**林悦**：用户输错命令时别抛一屏 Traceback，要友好提示。

**陈工**：自定义异常层次：`NexusCLIError` 基类，子类 `ValidationError`、`CommandNotFoundError`。`__main__.py` 里统一 catch，打印中文错误，退出码 1。

**运维老周**：退出码规范很重要，CI 脚本靠这个判断成功失败。KeyboardInterrupt 返回 130 是 Unix 惯例。
""",
    key_concepts=[
        "模块 module 与包 package 区别",
        "__init__.py 包初始化与 __all__",
        "相对导入 vs 绝对导入",
        "python -m package 运行机制",
        "__main__.py 包入口",
        "argparse 子命令 subparsers",
        "自定义异常继承 Exception",
        "异常层次与语义化错误码",
        "进程退出码 exit code 约定",
    ],
    platform_touches=[
        "platform/nexus_agent/cli/ 包结构原型",
        "platform 将以 python -m nexus_agent 启动",
        "异常体系对齐平台 NexusAgentError 设计",
    ],
)


# ---------------------------------------------------------------------------
# Day 11 — 文件操作与正则
# ---------------------------------------------------------------------------

_DAY11_DOC_KEYWORD = '''#!/usr/bin/env python3
"""
Day 11 示例：文档关键词统计器 —— 文件 IO + 正则表达式

场景：企业知识库上传前，自动扫描文档中的敏感词、高频技术术语，
      为 RAG 索引质量评估提供基础数据（Day 25+ 会扩展为完整管道）。
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path


# 默认关注的技术关键词（可扩展为从配置文件加载）
DEFAULT_KEYWORDS: list[str] = [
    "Python", "API", "Agent", "RAG", "向量", "嵌入",
    "大模型", "LLM", "微调", "Docker", "FastAPI",
]

# 编译正则：整词匹配，忽略大小写（中文无边界，直接子串匹配）
def build_pattern(keywords: list[str]) -> re.Pattern[str]:
    """将关键词列表编译为单一正则表达式。"""
    escaped = [re.escape(kw) for kw in keywords]
    # 英文用词边界 \\b，中文直接匹配
    parts = []
    for kw, esc in zip(keywords, escaped):
        if re.match(r"^[A-Za-z0-9]+$", kw):
            parts.append(rf"\\b{esc}\\b")
        else:
            parts.append(esc)
    return re.compile("|".join(parts), re.IGNORECASE)


def read_text_file(path: Path, encoding: str = "utf-8") -> str:
    """
    安全读取文本文件，自动处理常见编码问题。

    Raises:
        FileNotFoundError: 文件不存在
        UnicodeDecodeError: 编码无法解码（会尝试 gbk 回退）
    """
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {path}")
    if not path.is_file():
        raise IsADirectoryError(f"路径是目录而非文件: {path}")

    try:
        return path.read_text(encoding=encoding)
    except UnicodeDecodeError:
        # Windows 用户可能用 GBK 保存的文档
        return path.read_text(encoding="gbk", errors="replace")


def count_keywords(text: str, pattern: re.Pattern[str]) -> Counter[str]:
    """统计文本中各关键词出现次数。"""
    counter: Counter[str] = Counter()
    for match in pattern.finditer(text):
        counter[match.group().lower() if match.group().isascii() else match.group()] += 1
    return counter


def scan_file(path: Path, keywords: list[str] | None = None) -> dict:
    """
    扫描单个文件，返回统计报告字典。

    Returns:
        {
            "file": str,
            "total_chars": int,
            "total_lines": int,
            "keyword_hits": dict[str, int],
            "top_keywords": list[tuple[str, int]],
        }
    """
    keywords = keywords or DEFAULT_KEYWORDS
    pattern = build_pattern(keywords)
    text = read_text_file(path)

    lines = text.splitlines()
    hits = count_keywords(text, pattern)

    return {
        "file": str(path),
        "total_chars": len(text),
        "total_lines": len(lines),
        "keyword_hits": dict(hits),
        "top_keywords": hits.most_common(5),
    }


def scan_directory(dir_path: Path, glob_pattern: str = "*.md") -> list[dict]:
    """批量扫描目录下匹配的文档。"""
    reports = []
    for fp in sorted(dir_path.glob(glob_pattern)):
        if fp.is_file():
            reports.append(scan_file(fp))
    return reports


def print_report(report: dict) -> None:
    """格式化打印单文件报告。"""
    print(f"\\n{'='*50}")
    print(f"文件: {report['file']}")
    print(f"字符数: {report['total_chars']}  |  行数: {report['total_lines']}")
    print("关键词命中:")
    if report["top_keywords"]:
        for kw, cnt in report["top_keywords"]:
            print(f"  - {kw}: {cnt}")
    else:
        print("  (无匹配)")


def main() -> None:
    """命令行入口：python doc_keyword_counter.py <文件或目录>"""
    if len(sys.argv) < 2:
        # 无参数时扫描内置示例文档
        sample = Path(__file__).parent / "sample_docs" / "intro.md"
        sample.parent.mkdir(parents=True, exist_ok=True)
        if not sample.exists():
            sample.write_text(
                """# NexusAgent 简介

NexusAgent 是智链科技的企业级 Agent 平台，基于 Python 与 FastAPI 构建。
支持 RAG 检索增强、多 Agent 协作与大模型 API 接入。

## 技术栈
- Python 3.10+
- 向量数据库
- LLM API（通义千问、DeepSeek）
""",
                encoding="utf-8",
            )
        target = sample
    else:
        target = Path(sys.argv[1])

    if target.is_dir():
        reports = scan_directory(target)
    else:
        reports = [scan_file(target)]

    for r in reports:
        print_report(r)

    total_hits = sum(sum(r["keyword_hits"].values()) for r in reports)
    print(f"\\n{'='*50}")
    print(f"共扫描 {len(reports)} 个文件，关键词总命中 {total_hits} 次")


if __name__ == "__main__":
    main()
'''

DAY_11 = DayPlan(
    day=11,
    title="文件操作与正则 — 文档关键词统计器",
    phase="第一阶段:Python编程基础",
    epic="NEXUS-E1",
    jira_stories=["NEXUS-1101", "NEXUS-1102", "NEXUS-1103"],
    morning=[
        "09:00 站会：nexus_cli 包已合并，今日做知识库文档预检工具",
        "09:30 理论：Path 对象、读写文本、with 语句与上下文管理器",
        "10:30 理论：正则 re 模块、compile、finditer、转义",
        "11:00 跟敲 doc_keyword_counter.py 文件读取部分",
    ],
    afternoon=[
        "14:00 实现 build_pattern 与 count_keywords",
        "15:00 目录批量扫描 scan_directory",
        "16:00 编码处理：UTF-8 与 GBK 回退策略",
        "17:00 用 sample_docs 跑通端到端演示",
    ],
    evening=[
        "19:00 作业：支持从 JSON 配置文件加载关键词列表",
        "20:00 预习 requests 库，准备 Day 12 API 调用",
    ],
    code_files={"doc_keyword_counter.py": _DAY11_DOC_KEYWORD},
    homework_desc="""\
扩展 doc_keyword_counter.py：

1. 支持 `--config keywords.json` 从外部文件加载关键词
2. 输出 CSV 报告 `report.csv`（列：file, keyword, count）
3. 新增敏感词检测：命中敏感词时 print 警告（敏感词列表可硬编码 3 个示例词）
""",
    homework_answer_hint="""\
```python
import json, csv

def load_keywords(config_path: Path) -> list[str]:
    data = json.loads(config_path.read_text(encoding="utf-8"))
    return data["keywords"]

# 写 CSV
with open("report.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["file", "keyword", "count"])
    for r in reports:
        for kw, cnt in r["keyword_hits"].items():
            writer.writerow([r["file"], kw, cnt])
```
""",
    architecture_mermaid="""\
flowchart LR
    DOC[(.md 文档)] --> READ[read_text_file]
    READ --> TEXT[文本内容]
    KW[keywords.json] --> PATTERN[build_pattern]
    PATTERN --> COUNT[count_keywords]
    TEXT --> COUNT
    COUNT --> REPORT[统计报告]
    REPORT --> CSV[(report.csv)]
""",
    narration="""\
**林悦**：客户上传知识库文档前，我们想自动统计里面有多少「Agent」「RAG」这类词，评估文档质量。能做个脚本吗？

**陈工**：今天练文件 IO 和正则。`Path.read_text()` 读文件，`re.compile` 做关键词匹配。注意 Windows 上 GBK 编码的坑，要 try UTF-8 再 fallback。

**小王**：英文要整词匹配，「API」不能匹配到「CAPITAL」吧？

**陈工**：用 `\\b` 词边界。中文没有这个词边界概念，直接子串匹配。下午加目录批量扫描，为 Day 25 RAG 文档管道热身。

**架构老张**：这个计数器以后会进 ingestion pipeline 的质量门禁——关键词密度太低的文档可能不值得索引。

**测试小李**：我会准备空文件、二进制文件、超大文件，看异常处理是否得体。
""",
    key_concepts=[
        "pathlib.Path 面向对象路径操作",
        "read_text / write_text 文本读写",
        "UTF-8 与 GBK 编码处理",
        "正则表达式 re.compile / finditer",
        "re.escape 转义特殊字符",
        "词边界 \\b 整词匹配",
        "collections.Counter 计数",
        "glob 批量文件遍历",
        "命令行参数 sys.argv 解析",
    ],
    platform_touches=[
        "RAG 文档入库前的质量扫描原型",
        "platform/nexus_agent/rag/ingestion/scanner.py 前身",
        "关键词统计结果将用于知识库 Dashboard（Day 30+）",
    ],
)


# ---------------------------------------------------------------------------
# Day 12 — 网络请求与 API
# ---------------------------------------------------------------------------

_DAY12_FIRST_LLM = '''#!/usr/bin/env python3
"""
Day 12 示例：首次 LLM API 调用 —— requests + python-dotenv

演示如何通过 HTTP 调用大模型 API。支持：
  1. 真实 API（配置 .env 中的 API_KEY）
  2. Mock 模式（无密钥时自动降级，课堂可离线演示）
"""
from __future__ import annotations

import json
import os
import sys
from typing import Any

# 第三方库：pip install requests python-dotenv
try:
    import requests
    from dotenv import load_dotenv
except ImportError:
    print("请先安装依赖: pip install requests python-dotenv", file=sys.stderr)
    sys.exit(1)

# 加载 .env 文件（若存在）到环境变量
load_dotenv()

# ---------- 配置区 ----------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
DEFAULT_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
TIMEOUT_SECONDS = 30


def is_mock_mode() -> bool:
    """判断是否使用 Mock 模式（未配置有效 API Key）。"""
    key = OPENAI_API_KEY.strip()
    return not key or key.startswith("sk-your") or key == "mock"


def mock_chat_completion(messages: list[dict[str, str]], model: str) -> dict[str, Any]:
    """
    Mock 响应，结构与 OpenAI Chat Completions API 一致。
    课堂无网络/无密钥时可正常运行。
    """
    last_user = next(
        (m["content"] for m in reversed(messages) if m["role"] == "user"),
        "（空）",
    )
    return {
        "id": "chatcmpl-mock-day12",
        "object": "chat.completion",
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": (
                        f"[Mock 模式] 你好！我收到了你的消息：「{last_user}」\\n"
                        f"配置真实 OPENAI_API_KEY 后即可调用线上模型。"
                    ),
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": 20,
            "completion_tokens": 30,
            "total_tokens": 50,
        },
    }


def call_openai_chat(
    messages: list[dict[str, str]],
    model: str = DEFAULT_MODEL,
    temperature: float = 0.7,
) -> dict[str, Any]:
    """
    调用 OpenAI 兼容 Chat Completions API。

    Args:
        messages: [{"role": "user", "content": "..."}]
        model: 模型名称
        temperature: 采样温度 0-2

    Returns:
        API 响应 JSON 字典

    Raises:
        requests.HTTPError: HTTP 状态码非 2xx
        requests.Timeout: 请求超时
    """
    if is_mock_mode():
        print(">>> [提示] 当前为 Mock 模式，未配置有效 API Key", file=sys.stderr)
        return mock_chat_completion(messages, model)

    url = f"{OPENAI_BASE_URL.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }

    # POST 请求，设置超时防止挂起
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=TIMEOUT_SECONDS,
    )
    # 4xx/5xx 时抛出异常，附带响应体便于调试
    response.raise_for_status()
    return response.json()


def extract_reply(response: dict[str, Any]) -> str:
    """从 API 响应中提取助手回复文本。"""
    try:
        return response["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        raise ValueError(f"无法解析 API 响应: {response}") from e


def print_usage(response: dict[str, Any]) -> None:
    """打印 Token 用量，企业场景需做成本核算。"""
    usage = response.get("usage", {})
    if usage:
        print(
            f"  [Token] prompt={usage.get('prompt_tokens', '?')} "
            f"completion={usage.get('completion_tokens', '?')} "
            f"total={usage.get('total_tokens', '?')}"
        )


def main() -> None:
    """交互式单次问答演示。"""
    print("=" * 50)
    print("Day 12: 首次 LLM API 调用")
    print(f"模型: {DEFAULT_MODEL}  |  Mock: {is_mock_mode()}")
    print("=" * 50)

    user_input = input("\\n请输入问题（直接回车使用默认）: ").strip()
    if not user_input:
        user_input = "用三句话介绍什么是 NexusAgent 智能体平台。"

    messages = [
        {"role": "system", "content": "你是智链科技 Nexus 项目的 AI 助手，回答简洁专业。"},
        {"role": "user", "content": user_input},
    ]

    print("\\n正在请求 API...")
    try:
        resp = call_openai_chat(messages)
        reply = extract_reply(resp)
        print("\\n助手回复:")
        print("-" * 40)
        print(reply)
        print("-" * 40)
        print_usage(resp)
    except requests.HTTPError as e:
        print(f"HTTP 错误: {e}", file=sys.stderr)
        if e.response is not None:
            print(e.response.text[:500], file=sys.stderr)
        sys.exit(1)
    except requests.Timeout:
        print(f"请求超时（>{TIMEOUT_SECONDS}s）", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
'''

_DAY12_ENV_EXAMPLE = """\
# Day 12 环境变量配置示例
# 复制为 .env 并填入真实密钥: cp .env.example .env

# OpenAI 或兼容 API（DeepSeek、通义兼容模式等）
OPENAI_API_KEY=sk-your-key-here
OPENAI_BASE_URL=https://api.openai.com/v1

# 默认模型
LLM_MODEL=gpt-4o-mini
"""

DAY_12 = DayPlan(
    day=12,
    title="网络请求与 API — 首次 LLM 调用",
    phase="第一阶段:Python编程基础",
    epic="NEXUS-E1",
    jira_stories=["NEXUS-1201", "NEXUS-1202", "NEXUS-1203"],
    morning=[
        "09:00 站会：文档扫描工具验收，今日接入真实（或 Mock）大模型 API",
        "09:30 理论：HTTP 基础、GET/POST、状态码、JSON",
        "10:30 理论：requests 库、超时、异常处理",
        "11:00 理论：dotenv 环境变量、密钥安全管理",
    ],
    afternoon=[
        "14:00 跟敲 first_llm_call.py，先跑通 Mock 模式",
        "15:00 配置 .env，尝试真实 API 调用",
        "16:00 解析响应 JSON，提取 choices[0].message.content",
        "17:00 讨论：API Key 绝不能提交 Git，.gitignore 配置",
    ],
    evening=[
        "19:00 作业：封装 chat_once(prompt) 函数，支持重试",
        "20:00 阅读通义千问 DashScope HTTP API 文档",
    ],
    code_files={
        "first_llm_call.py": _DAY12_FIRST_LLM,
        ".env.example": _DAY12_ENV_EXAMPLE,
    },
    homework_desc="""\
在 `homework/chat_client.py` 中：

1. 封装 `chat_once(prompt: str, system: str = "") -> str`
2. HTTP 5xx 或超时时自动重试 3 次，间隔 2 秒
3. 将每次调用的 usage 追加写入 `usage.log`（JSON Lines 格式）
4. 命令行：`python chat_client.py "你的问题"`
""",
    homework_answer_hint="""\
```python
import time, json
from first_llm_call import call_openai_chat, extract_reply

def chat_once(prompt, system="", retries=3):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    for attempt in range(retries):
        try:
            resp = call_openai_chat(messages)
            with open("usage.log", "a") as f:
                f.write(json.dumps(resp.get("usage", {})) + "\\n")
            return extract_reply(resp)
        except Exception as e:
            if attempt == retries - 1:
                raise
            time.sleep(2)
```
""",
    architecture_mermaid="""\
sequenceDiagram
    participant CLI as first_llm_call.py
    participant ENV as .env
    participant API as LLM API
    CLI->>ENV: load_dotenv()
    alt 有 API Key
        CLI->>API: POST /chat/completions
        API-->>CLI: JSON response
    else Mock 模式
        CLI->>CLI: mock_chat_completion()
    end
    CLI->>CLI: extract_reply()
""",
    narration="""\
**林悦**：文档扫描只是预处理，用户真正需要的是「问问题得回答」。今天能打通大模型 API 吗？

**陈工**：今天 first_llm_call.py，用 requests 发 POST。密钥放 `.env`，python-dotenv 加载，**绝对不要** commit 到 GitLab。

**小王**：课堂上没 API Key 怎么办？

**陈工**：Mock 模式。检测 key 为空或是占位符 `sk-your` 就走本地假响应，结构与真实 API 一致。先 Mock 跑通逻辑，再换真 key。

**安全专员**：生产环境密钥走 Vault 或 K8s Secret，`.env` 只是本地开发。MR 里如果看到 sk- 开头的内容直接打回。

**架构老张**：这个调用函数 Day 14 会塞进 CLI 助手，Day 15 改成 FastAPI 端点。响应解析要健壮，API 格式变了不能崩。
""",
    key_concepts=[
        "HTTP 协议与 RESTful API",
        "requests.post 发送 JSON 请求",
        "HTTP 状态码与 raise_for_status",
        "请求超时 timeout 参数",
        "JSON 序列化与反序列化",
        "python-dotenv 环境变量管理",
        "API Key 安全与 .gitignore",
        "OpenAI Chat Completions 请求/响应结构",
        "Mock 模式离线开发与测试",
    ],
    platform_touches=[
        "platform/nexus_agent/llm/openai_client.py 第一版",
        "平台配置中心将管理多租户 API Key（Day 20+）",
        "usage 日志为后续成本核算模块奠基",
    ],
)


# ---------------------------------------------------------------------------
# Day 13 — 装饰器与异步
# ---------------------------------------------------------------------------

_DAY13_RETRY = '''#!/usr/bin/env python3
"""
Day 13 示例：重试装饰器 —— 企业级 API 调用的弹性保障

网络抖动、限流 429、服务端 5xx 时，自动重试是生产代码标配。
本模块用装饰器实现可配置的重试逻辑，Day 12 的 API 调用可直接套用。
"""
from __future__ import annotations

import functools
import random
import time
from typing import Any, Callable, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    jitter: bool = True,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    重试装饰器工厂。

    Args:
        max_attempts: 最大尝试次数（含首次）
        delay: 首次重试前等待秒数
        backoff: 指数退避倍数，第 n 次等待 delay * backoff^(n-1)
        jitter: 是否加随机抖动，避免惊群效应
        exceptions: 触发重试的异常类型元组

    Example:
        @retry(max_attempts=3, exceptions=(requests.HTTPError, requests.Timeout))
        def call_api():
            ...
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)  # 保留原函数元信息 __name__, __doc__
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_exc: Exception | None = None
            current_delay = delay

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    if attempt == max_attempts:
                        break
                    # 计算等待时间
                    wait = current_delay
                    if jitter:
                        wait *= 0.5 + random.random()  # 0.5x ~ 1.5x
                    print(
                        f"[retry] {func.__name__} 第 {attempt} 次失败: {e}，"
                        f"{wait:.1f}s 后重试..."
                    )
                    time.sleep(wait)
                    current_delay *= backoff

            assert last_exc is not None
            raise last_exc

        return wrapper

    return decorator


# ---------- 演示：模拟不稳定的 API ----------
class RateLimitError(Exception):
    """模拟 429 限流。"""


_call_count = 0


@retry(max_attempts=4, delay=0.5, exceptions=(RateLimitError,))
def unstable_api_call(query: str) -> str:
    """
    模拟前两次调用失败、第三次成功的 API。
    被 @retry 装饰后，调用方无感知重试。
    """
    global _call_count
    _call_count += 1
    print(f"  -> unstable_api_call 第 {_call_count} 次执行, query={query!r}")
    if _call_count < 3:
        raise RateLimitError(f"模拟限流，当前第 {_call_count} 次")
    return f"成功响应: {query}"


def demo_retry() -> None:
    global _call_count
    _call_count = 0
    print("=== 重试装饰器演示 ===")
    result = unstable_api_call("NexusAgent")
    print(f"最终结果: {result}")
    print(f"总调用次数: {_call_count}")


if __name__ == "__main__":
    demo_retry()
'''

_DAY13_ASYNC = '''#!/usr/bin/env python3
"""
Day 13 示例：asyncio 异步编程入门

FastAPI（Day 15+）基于 async/await。今日掌握协程、并发调用多个 API 的基础。
"""
from __future__ import annotations

import asyncio
import time
from typing import Any


async def fetch_data(source: str, delay: float) -> dict[str, Any]:
    """
    模拟异步 IO：等待 delay 秒后返回数据。
    await 会挂起当前协程，让事件循环执行其他任务。
    """
    print(f"[{source}] 开始请求...")
    await asyncio.sleep(delay)  # 非阻塞等待，模拟网络 IO
    print(f"[{source}] 完成 ({delay}s)")
    return {"source": source, "data": f"{source} 的响应内容"}


async def fetch_sequential() -> list[dict]:
    """串行调用：总耗时 = 各 delay 之和。"""
    print("\\n--- 串行调用 ---")
    t0 = time.perf_counter()
    results = []
    for name, delay in [("OpenAI", 1.0), ("Qwen", 1.0), ("DeepSeek", 1.0)]:
        results.append(await fetch_data(name, delay))
    elapsed = time.perf_counter() - t0
    print(f"串行总耗时: {elapsed:.2f}s")
    return results


async def fetch_parallel() -> list[dict]:
    """并行调用：asyncio.gather 并发执行，总耗时 ≈ 最长 delay。"""
    print("\\n--- 并行调用 (gather) ---")
    t0 = time.perf_counter()
    tasks = [
        fetch_data("OpenAI", 1.0),
        fetch_data("Qwen", 1.0),
        fetch_data("DeepSeek", 1.0),
    ]
    results = await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - t0
    print(f"并行总耗时: {elapsed:.2f}s")
    return results


async def async_retry_demo() -> None:
    """异步版重试逻辑（理解即可，Day 15 会结合 aiohttp）。"""
    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        try:
            await fetch_data("flaky_api", 0.3)
            break
        except Exception:
            if attempt == max_attempts:
                raise
            await asyncio.sleep(0.5 * attempt)


def run_async_main() -> None:
    """
    同步入口调用异步主函数的标准写法。
    asyncio.run() 创建事件循环并运行顶层协程。
    """
    print("=" * 50)
    print("Day 13: asyncio 异步演示")
    print("=" * 50)

    async def main() -> None:
        await fetch_sequential()
        await fetch_parallel()
        await async_retry_demo()

    asyncio.run(main())


if __name__ == "__main__":
    run_async_main()
'''

_DAY13_COMBINED = '''#!/usr/bin/env python3
"""
Day 13 综合：将 retry 装饰器应用于 Day 12 API 调用（同步版）
"""
from __future__ import annotations

import sys
from pathlib import Path

# 允许从同级目录导入 Day 12 模块
sys.path.insert(0, str(Path(__file__).resolve().parent))

from retry_decorator import retry

try:
    import requests
    from first_llm_call import call_openai_chat, extract_reply
except ImportError:
    print("请确保 first_llm_call.py 在同目录")
    sys.exit(1)


@retry(max_attempts=3, delay=2.0, exceptions=(requests.RequestException,))
def robust_chat(prompt: str) -> str:
    """带重试的单轮对话封装。"""
    messages = [{"role": "user", "content": prompt}]
    resp = call_openai_chat(messages)
    return extract_reply(resp)


if __name__ == "__main__":
    reply = robust_chat("async 和 sync 有什么区别？用一句话回答。")
    print(reply)
'''

DAY_13 = DayPlan(
    day=13,
    title="装饰器与异步 — 重试装饰器与 asyncio",
    phase="第一阶段:Python编程基础",
    epic="NEXUS-E1",
    jira_stories=["NEXUS-1301", "NEXUS-1302", "NEXUS-1303"],
    morning=[
        "09:00 站会：API 调用已通，今日加「弹性」——重试与异步",
        "09:30 理论：函数是一等公民、闭包、装饰器语法 @",
        "10:30 理论：functools.wraps、带参数的装饰器工厂",
        "11:00 跟敲 retry_decorator.py",
    ],
    afternoon=[
        "14:00 指数退避与 jitter 讲解，演示 unstable_api_call",
        "15:00 asyncio 基础：async def、await、asyncio.run",
        "16:00 串行 vs 并行：gather 性能对比",
        "17:00 将 @retry 套到 first_llm_call 上",
    ],
    evening=[
        "19:00 作业：实现 @timing 装饰器，打印函数耗时",
        "20:00 预习 FastAPI 异步路由（Day 15 铺垫）",
    ],
    code_files={
        "retry_decorator.py": _DAY13_RETRY,
        "async_demo.py": _DAY13_ASYNC,
        "robust_llm_demo.py": _DAY13_COMBINED,
    },
    homework_desc="""\
1. 实现 `@timing` 装饰器：记录函数每次执行耗时，写入 `timing.log`
2. 实现 `@cache_result(ttl=60)` 装饰器：60 秒内相同参数返回缓存
3. 用 `asyncio.gather` 并发调用 3 次 `fetch_data`，对比串行耗时
""",
    homework_answer_hint="""\
```python
import time, functools

def timing(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - t0
        with open("timing.log", "a") as f:
            f.write(f"{func.__name__}: {elapsed:.4f}s\\n")
        return result
    return wrapper
```
""",
    architecture_mermaid="""\
flowchart TB
    CALL[API 调用] --> RETRY[@retry 装饰器]
    RETRY -->|失败| WAIT[指数退避等待]
    WAIT --> RETRY
    RETRY -->|成功| RESULT[返回结果]
    subgraph async [异步并发]
        T1[fetch OpenAI]
        T2[fetch Qwen]
        T3[fetch DeepSeek]
    end
    GATHER[asyncio.gather] --> T1 & T2 & T3
""",
    narration="""\
**陈工**：昨天 API 一超时就崩，生产环境不行。今天写 `@retry` 装饰器——指数退避、随机 jitter，限流 429 时自动等一等再试。

**小王**：装饰器本质是什么？

**陈工**：高阶函数语法糖。`@retry(...)` 等于 `func = retry(...)(func)`。`functools.wraps` 保留原函数名字，不然日志里全是 wrapper。

**架构老张**：下午讲 async。FastAPI 路由默认 async，Day 15 会大量用。今天先理解 `await asyncio.sleep` 和 `time.sleep` 的区别——一个让出控制权，一个阻塞线程。

**林悦**：多模型对比时能并行问三个 API 吗？

**陈工**：`asyncio.gather` 并行，耗时从 3 秒变 1 秒。但要注意 API 并发限额，企业里要加 semaphore 限流，毕业设计阶段再细讲。

**测试小李**：我会测 retry 次数边界：第 max_attempts 次仍失败是否正确抛异常。
""",
    key_concepts=[
        "装饰器 decorator 与 @ 语法糖",
        "闭包与装饰器工厂",
        "functools.wraps 保留元信息",
        "指数退避 exponential backoff",
        "随机 jitter 避免惊群",
        "async def 定义协程",
        "await 挂起与让出控制权",
        "asyncio.run 事件循环入口",
        "asyncio.gather 并发执行",
        "同步 vs 异步 IO 模型",
    ],
    platform_touches=[
        "platform 所有 LLM 客户端将统一 @retry",
        "FastAPI 异步路由（Day 15）的前置知识",
        "多模型并行评测场景的技术储备",
    ],
)


# ---------------------------------------------------------------------------
# Day 14 — 阶段项目一：CLI 多轮对话助手（300+ 行）
# ---------------------------------------------------------------------------

_DAY14_CONFIG = '''"""cli_chat_assistant 配置模块 —— 集中管理环境变量与默认值。"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

# 加载项目根目录或当前目录的 .env
load_dotenv()


@dataclass
class AppConfig:
    """
    应用配置数据类。
    所有魔法字符串集中在此，便于测试与部署时覆盖。
    """

    # LLM 相关
    api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    base_url: str = field(default_factory=lambda: os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"))
    model: str = field(default_factory=lambda: os.getenv("LLM_MODEL", "gpt-4o-mini"))
    system_prompt: str = "你是智链科技 NexusAgent 平台的 AI 助手，回答简洁、专业、友好。"
    timeout: int = 30
    mock_mode: bool = False

    # 存储相关
    history_dir: Path = field(default_factory=lambda: Path("data/history"))
    default_save_name: str = "session.json"

    def __post_init__(self) -> None:
        """根据 api_key 自动判断是否 Mock 模式。"""
        key = self.api_key.strip()
        if not key or key.startswith("sk-your") or key == "mock":
            self.mock_mode = True
        self.history_dir.mkdir(parents=True, exist_ok=True)


def get_config() -> AppConfig:
    """获取全局配置单例（简化版，未用真正的单例模式）。"""
    return AppConfig()
'''

_DAY14_MODELS = '''"""cli_chat_assistant 领域模型 —— 消息与对话会话。"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class Role(str, Enum):
    """消息角色，与 OpenAI API 对齐。"""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass
class Message:
    """单条对话消息。"""

    role: Role
    content: str
    timestamp: datetime = field(default_factory=datetime.now)

    def to_api_dict(self) -> dict[str, str]:
        """转换为 LLM API 所需的 {role, content} 格式。"""
        return {"role": self.role.value, "content": self.content}

    def to_storage_dict(self) -> dict[str, Any]:
        """转换为可 JSON 序列化的完整字典。"""
        return {
            "role": self.role.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_storage_dict(cls, data: dict[str, Any]) -> Message:
        """从持久化数据恢复 Message 对象。"""
        ts = data.get("timestamp")
        timestamp = datetime.fromisoformat(ts) if isinstance(ts, str) else datetime.now()
        return cls(role=Role(data["role"]), content=data["content"], timestamp=timestamp)

    def preview(self, max_len: int = 60) -> str:
        """生成简短预览，用于历史列表。"""
        text = self.content.replace("\\n", " ")
        return text if len(text) <= max_len else text[: max_len - 3] + "..."


@dataclass
class ChatSession:
    """
    一次完整的对话会话，包含系统提示词与多轮消息历史。
  Day 8 ChatMessage 的升级版，增加了会话级管理。
    """

    session_id: str
    messages: list[Message] = field(default_factory=list)
    system_prompt: str = ""
    created_at: datetime = field(default_factory=datetime.now)

    def add_user(self, content: str) -> Message:
        """添加用户消息并返回。"""
        msg = Message(role=Role.USER, content=content)
        self.messages.append(msg)
        return msg

    def add_assistant(self, content: str) -> Message:
        """添加助手回复并返回。"""
        msg = Message(role=Role.ASSISTANT, content=content)
        self.messages.append(msg)
        return msg

    def clear(self) -> int:
        """清空对话历史（保留 system），返回清除条数。"""
        count = len(self.messages)
        self.messages.clear()
        return count

    def build_api_messages(self) -> list[dict[str, str]]:
        """
        构建发送给 LLM API 的 messages 数组。
        格式: [system, user, assistant, user, assistant, ...]
        """
        result: list[dict[str, str]] = []
        if self.system_prompt:
            result.append({"role": "system", "content": self.system_prompt})
        for msg in self.messages:
            result.append(msg.to_api_dict())
        return result

    def message_count(self) -> int:
        """返回当前消息条数。"""
        return len(self.messages)

    def last_exchange_preview(self) -> str:
        """返回最近一轮问答的预览文本。"""
        if not self.messages:
            return "（空会话）"
        last = self.messages[-1]
        return f"[{last.role.value}] {last.preview()}"
'''

_DAY14_LLM = '''"""cli_chat_assistant LLM 客户端 —— 封装 API 调用与 Mock。"""
from __future__ import annotations

from typing import Any

import requests

from cli_chat_assistant.config import AppConfig


def mock_completion(messages: list[dict[str, str]], model: str) -> dict[str, Any]:
    """
    Mock 模式响应，无需真实 API Key 即可演示完整 CLI 流程。
    会根据用户最后一条消息生成模板回复。
    """
    last_user = ""
    for m in reversed(messages):
        if m["role"] == "user":
            last_user = m["content"]
            break

    # 简单关键词回复，增加演示趣味性
    if "你好" in last_user or "hello" in last_user.lower():
        reply = "你好！我是 NexusAgent CLI 助手，有什么可以帮您？"
    elif "rag" in last_user.lower() or "检索" in last_user:
        reply = "RAG（检索增强生成）通过向量检索相关知识再生成回答，是 Day 25+ 的核心内容。"
    elif "/help" in last_user:
        reply = "输入普通文本即可对话。内置命令: /clear /save /exit /help"
    else:
        reply = (
            f"[Mock/{model}] 收到您的消息（{len(last_user)} 字）：\\n"
            f"「{last_user[:80]}{'...' if len(last_user) > 80 else ''}」\\n"
            f"配置 OPENAI_API_KEY 后可获得真实 AI 回复。"
        )

    return {
        "choices": [{"message": {"role": "assistant", "content": reply}}],
        "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
        "model": model,
    }


def chat_completion(messages: list[dict[str, str]], config: AppConfig) -> str:
    """
    发送多轮对话请求，返回助手回复文本。

    Args:
        messages: OpenAI 格式的消息列表
        config: 应用配置

    Returns:
        助手回复的纯文本

    Raises:
        requests.RequestException: 网络或 HTTP 错误
    """
    if config.mock_mode:
        resp = mock_completion(messages, config.model)
        return resp["choices"][0]["message"]["content"]

    url = f"{config.base_url.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {config.api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": config.model,
        "messages": messages,
        "temperature": 0.7,
    }

    response = requests.post(url, headers=headers, json=payload, timeout=config.timeout)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]
'''

_DAY14_STORAGE = '''"""cli_chat_assistant 持久化 —— 会话保存与加载。"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from cli_chat_assistant.models import ChatSession, Message


def session_to_dict(session: ChatSession) -> dict[str, Any]:
    """将会话对象序列化为可 JSON 存储的字典。"""
    return {
        "session_id": session.session_id,
        "system_prompt": session.system_prompt,
        "created_at": session.created_at.isoformat(),
        "messages": [m.to_storage_dict() for m in session.messages],
    }


def session_from_dict(data: dict[str, Any]) -> ChatSession:
    """从字典恢复 ChatSession 对象。"""
    created = data.get("created_at")
    created_at = datetime.fromisoformat(created) if isinstance(created, str) else datetime.now()
    session = ChatSession(
        session_id=data["session_id"],
        system_prompt=data.get("system_prompt", ""),
        created_at=created_at,
    )
    for msg_data in data.get("messages", []):
        session.messages.append(Message.from_storage_dict(msg_data))
    return session


def save_session(session: ChatSession, path: Path) -> None:
    """
    保存会话到 JSON 文件。

    文件格式 UTF-8，缩进 2 空格，便于人工查看与 Git diff。
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = session_to_dict(session)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def load_session(path: Path) -> ChatSession:
    """从 JSON 文件加载会话，文件不存在时抛出 FileNotFoundError。"""
    if not path.exists():
        raise FileNotFoundError(f"会话文件不存在: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    return session_from_dict(data)


def list_saved_sessions(history_dir: Path) -> list[Path]:
    """列出历史目录下所有 .json 会话文件。"""
    if not history_dir.exists():
        return []
    return sorted(history_dir.glob("*.json"))
'''

_DAY14_COMMANDS = '''"""cli_chat_assistant 内置斜杠命令处理。"""
from __future__ import annotations

from pathlib import Path

from cli_chat_assistant.config import AppConfig
from cli_chat_assistant.models import ChatSession
from cli_chat_assistant.storage import list_saved_sessions, save_session

# 所有支持的斜杠命令
BUILTIN_COMMANDS = ("/clear", "/save", "/exit", "/help", "/history")


def is_command(text: str) -> bool:
    """判断输入是否为斜杠命令。"""
    return text.strip().startswith("/")


def handle_command(text: str, session: ChatSession, config: AppConfig) -> tuple[bool, str]:
    """
    处理斜杠命令。

    Returns:
        (should_exit, message)
        - should_exit: True 表示应退出主循环
        - message: 反馈给用户的文本（空串表示无需额外输出）
    """
    cmd = text.strip().lower()
    parts = cmd.split(maxsplit=1)
    command = parts[0]
    arg = parts[1] if len(parts) > 1 else ""

    if command == "/exit":
        return True, "再见！感谢使用 NexusAgent CLI 助手。"

    if command == "/clear":
        count = session.clear()
        return False, f"已清空 {count} 条对话记录（系统提示词保留）。"

    if command == "/save":
        # /save 或 /save my_session.json
        filename = arg.strip() if arg else config.default_save_name
        if not filename.endswith(".json"):
            filename += ".json"
        path = config.history_dir / filename
        save_session(session, path)
        return False, f"会话已保存至 {path}（共 {session.message_count()} 条消息）。"

    if command == "/history":
        lines = [f"--- 当前会话 {session.session_id} ---"]
        for i, msg in enumerate(session.messages, 1):
            lines.append(f"  {i}. [{msg.role.value}] {msg.preview(50)}")
        if not session.messages:
            lines.append("  （暂无消息）")
        saved = list_saved_sessions(config.history_dir)
        if saved:
            lines.append(f"\\n已保存文件 ({len(saved)} 个):")
            for p in saved[-5:]:
                lines.append(f"  - {p.name}")
        return False, "\\n".join(lines)

    if command == "/help":
        help_text = """
可用命令:
  /clear          清空当前对话历史
  /save [文件名]   保存会话到 data/history/
  /history        查看当前会话消息列表
  /help           显示此帮助
  /exit           退出程序

直接输入文字即可与 AI 对话。
"""
        return False, help_text.strip()

    return False, f"未知命令: {command}，输入 /help 查看帮助。"
'''

_DAY14_INIT = '''"""
cli_chat_assistant — 阶段项目一：多轮对话 CLI 助手

智链科技 NexusAgent 训练营 Day 14 毕业项目（第一阶段）
功能：多轮对话、/clear /save /exit 指令、历史持久化、Mock/真实 API
"""
__version__ = "0.1.0"
'''

_DAY14_MAIN = '''#!/usr/bin/env python3
"""
cli_chat_assistant 主入口 —— 多轮对话 REPL

运行方式（在 code/ 目录下）:
    python -m cli_chat_assistant

或:
    python cli_chat_assistant/main.py
"""
from __future__ import annotations

import sys
import uuid
from datetime import datetime

from cli_chat_assistant.commands import handle_command, is_command
from cli_chat_assistant.config import get_config
from cli_chat_assistant.llm_client import chat_completion
from cli_chat_assistant.models import ChatSession


def print_banner(config) -> None:
    """打印启动横幅与模式提示。"""
    mode = "Mock 模式（无 API Key）" if config.mock_mode else f"在线模式 ({config.model})"
    print("=" * 56)
    print("  NexusAgent CLI 助手  |  阶段项目一  |  Day 14")
    print("  智链科技 SmartLink Tech")
    print("=" * 56)
    print(f"  会话模式: {mode}")
    print("  输入 /help 查看命令，/exit 退出")
    print("=" * 56)


def create_session(config) -> ChatSession:
    """创建新会话，生成唯一 session_id。"""
    sid = f"sess-{datetime.now():%Y%m%d}-{uuid.uuid4().hex[:8]}"
    return ChatSession(
        session_id=sid,
        system_prompt=config.system_prompt,
    )


def read_user_input() -> str | None:
    """
    读取用户输入，处理 EOF（Ctrl+D） gracefully。
    Returns None 表示用户请求退出。
    """
    try:
        return input("\\n你> ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\\n")
        return None


def run_chat_loop() -> int:
    """主对话循环，返回进程退出码。"""
    config = get_config()
    session = create_session(config)
    print_banner(config)

    while True:
        user_text = read_user_input()

        # EOF / Ctrl+C 视为退出
        if user_text is None:
            print("再见！")
            return 0

        if not user_text:
            continue

        # ---------- 斜杠命令分支 ----------
        if is_command(user_text):
            should_exit, msg = handle_command(user_text, session, config)
            if msg:
                print(msg)
            if should_exit:
                return 0
            continue

        # ---------- 普通对话分支 ----------
        session.add_user(user_text)
        api_messages = session.build_api_messages()

        print("助手> ", end="", flush=True)
        try:
            reply = chat_completion(api_messages, config)
            print(reply)
            session.add_assistant(reply)
        except Exception as e:
            # 请求失败时回滚刚添加的用户消息，保持历史一致
            session.messages.pop()
            print(f"\\n[错误] API 调用失败: {e}", file=sys.stderr)
            print("请检查网络与 API Key 配置，或稍后重试。", file=sys.stderr)

    return 0


def main() -> int:
    """程序入口。"""
    return run_chat_loop()


if __name__ == "__main__":
    raise SystemExit(main())
'''

_DAY14_RUN = '''#!/usr/bin/env python3
"""Day 14 快速启动脚本。"""
import sys
from pathlib import Path

# 将 code/ 加入 path，确保包可导入
sys.path.insert(0, str(Path(__file__).resolve().parent))

from cli_chat_assistant.main import main

if __name__ == "__main__":
    raise SystemExit(main())
'''

_DAY14_ENV = """\
# Day 14 CLI 助手环境变量
OPENAI_API_KEY=sk-your-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
"""

_DAY14_REQUIREMENTS = """\
# Day 14 依赖
requests>=2.28.0
python-dotenv>=1.0.0
"""

DAY_14 = DayPlan(
    day=14,
    title="阶段项目一：CLI 多轮对话助手",
    phase="第一阶段:Python编程基础",
    epic="NEXUS-E1",
    jira_stories=["NEXUS-1401", "NEXUS-1402", "NEXUS-1403", "NEXUS-1404"],
    morning=[
        "09:00 站会：第一阶段复盘，宣布项目一立项",
        "09:30 需求评审：多轮对话、/clear /save /exit、Mock 模式",
        "10:30 架构设计：config / models / llm_client / storage / commands 模块划分",
        "11:00 搭建 cli_chat_assistant 包骨架",
    ],
    afternoon=[
        "14:00 实现主循环 run_chat_loop 与斜杠命令分发",
        "15:00 接入 Day 12 LLM 调用，支持 Mock 降级",
        "16:00 实现会话 JSON 持久化 /save",
        "17:00 端到端测试：多轮对话 → /save → /clear → /exit",
    ],
    evening=[
        "19:00 项目答辩准备：演示脚本、README、MR 提交",
        "20:00 庆祝第一阶段完成，预习 Day 15 FastAPI 入门",
    ],
    code_files={
        "cli_chat_assistant/__init__.py": _DAY14_INIT,
        "cli_chat_assistant/config.py": _DAY14_CONFIG,
        "cli_chat_assistant/models.py": _DAY14_MODELS,
        "cli_chat_assistant/llm_client.py": _DAY14_LLM,
        "cli_chat_assistant/storage.py": _DAY14_STORAGE,
        "cli_chat_assistant/commands.py": _DAY14_COMMANDS,
        "cli_chat_assistant/main.py": _DAY14_MAIN,
        "run_cli.py": _DAY14_RUN,
        ".env.example": _DAY14_ENV,
        "requirements.txt": _DAY14_REQUIREMENTS,
    },
    homework_desc="""\
在项目一基础上扩展（选做 2 项以上）：

1. `/load <文件名>` 命令：从 data/history/ 加载历史会话
2. 流式输出：逐字打印助手回复（模拟 stream，可用 time.sleep）
3. `/model <name>` 命令：运行时切换模型
4. 编写 `tests/test_commands.py` 测试 /clear 和 /save 逻辑
5. 撰写项目 README：安装、配置、使用说明、架构图
""",
    homework_answer_hint="""\
```python
# commands.py 添加 /load
from cli_chat_assistant.storage import load_session

if command == "/load":
    filename = arg or config.default_save_name
    if not filename.endswith(".json"):
        filename += ".json"
    path = config.history_dir / filename
    loaded = load_session(path)
    session.messages = loaded.messages
    session.session_id = loaded.session_id
    return False, f"已加载 {path}，共 {session.message_count()} 条消息"
```
""",
    architecture_mermaid="""\
flowchart TB
    subgraph CLI["cli_chat_assistant"]
        MAIN[main.py REPL]
        CMD[commands.py]
        MODELS[models.py]
        LLM[llm_client.py]
        STORE[storage.py]
        CFG[config.py]
    end
  USER[用户终端] --> MAIN
    MAIN -->|斜杠命令| CMD
    MAIN -->|普通输入| MODELS
    MODELS --> LLM
    LLM -->|Mock| MOCK[mock_completion]
    LLM -->|真实| API[LLM API]
    CMD -->|/save| STORE
    STORE --> JSON[(data/history/*.json)]
    CFG --> LLM
    CFG --> MAIN
""",
    narration="""\
**林悦（产品经理）**：两周了，今天交付第一阶段里程碑——**命令行多轮对话 AI 助手**。验收标准：能连续聊、能清空、能保存、能退出。

**陈工（Tech Lead）**：模块拆清楚：`config` 管配置，`models` 管消息，`llm_client` 管 API，`storage` 管持久化，`commands` 管斜杠指令，`main` 跑 REPL 主循环。这是 platform/nexus_agent 的微缩版。

**小王（后端）**：没 API Key 的学员怎么办？

**陈工**：`mock_mode` 自动检测，Mock 回复也要走完整流程——加消息、构建 history、保存 JSON。逻辑通了再换真 key。

**测试小李**：我列了测试用例：空输入跳过、/clear 后 message_count 为 0、/save 后文件存在且可解析、API 失败时用户消息回滚。

**架构老张**：下午 17:00 代码冻结，19:00 每组 5 分钟演示。MR 标题 `[Day-14] feat: CLI 多轮对话助手 v0.1`，关联 Jira NEXUS-1401~1404。

**林悦**：恭喜大家完成第一阶段！明天开始 FastAPI，把这个助手搬上 Web。
""",
    key_concepts=[
        "REPL 主循环 read-eval-print loop",
        "斜杠命令解析与分发",
        "ChatSession 多轮上下文管理",
        "build_api_messages 构建 LLM 请求",
        "JSON 会话持久化 save/load",
        "Mock 模式开发与演示",
        "模块化包结构设计",
        "API 失败时状态回滚",
        "配置集中管理 AppConfig",
        "阶段项目 MVP 交付流程",
    ],
    platform_touches=[
        "NexusAgent v0.1 CLI 版本正式交付",
        "platform/nexus_agent/cli/chat.py 由此演进",
        "Day 15 将本助手改写为 FastAPI + SSE 流式 Web 版",
        "会话 JSON 格式与平台 Redis 会话存储协议对齐（字段兼容）",
    ],
)


# ---------------------------------------------------------------------------
# 导出
# ---------------------------------------------------------------------------

DAYS_08_TO_14: list[DayPlan] = [
    DAY_08,
    DAY_09,
    DAY_10,
    DAY_11,
    DAY_12,
    DAY_13,
    DAY_14,
]
