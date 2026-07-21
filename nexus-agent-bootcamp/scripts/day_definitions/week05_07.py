"""
NexusAgent 训练营 Day 25-50 课件定义
Phase 3: LangChain RAG 知识库 (NEXUS-E3, Day 25-38)
Phase 4: 多 Agent 编排 (NEXUS-E4, Day 39-50)
"""
from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from generate_courseware import DayPlan  # noqa: E402

PHASE_3 = "Phase 3：LangChain RAG 知识库"
PHASE_4 = "Phase 4：多 Agent 编排"
EPIC_E3 = "NEXUS-E3"
EPIC_E4 = "NEXUS-E4"

DAY_25 = DayPlan(
    day=25,
    title='LangChain 入门',
    phase='Phase 3：LangChain RAG 知识库',
    epic='NEXUS-E3',
    jira_stories=['NEXUS-251', 'NEXUS-252'],
    morning=['09:00 站会：Nexus v0.3 RAG 阶段启动', '09:30 LangChain 生态：Model / Prompt / Parser', '10:30 ChatOpenAI 对接 DeepSeek', '11:00 跟敲 hello_langchain'],
    afternoon=['14:00 PromptTemplate 变量注入', '15:00 OutputParser 结构化输出', '16:30 封装 build_llm 工厂', '17:00 Code Review'],
    evening=['19:00 作业：企业客服 System Prompt', '20:00 预习 LCEL'],
    code_files={
        'hello_langchain.py': '#!/usr/bin/env python3\n"""Day 25: LangChain 入门 — ChatOpenAI 最小调用"""\nimport os\nfrom langchain_openai import ChatOpenAI\nfrom langchain_core.messages import HumanMessage, SystemMessage\n\ndef build_llm() -> ChatOpenAI:\n    # OpenAI 兼容协议连接 DeepSeek\n    return ChatOpenAI(\n        model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),\n        api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),\n        base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),\n        temperature=0.3,\n    )\n\ndef main() -> None:\n    llm = build_llm()\n    messages = [\n        SystemMessage(content="你是智链科技 Nexus 项目 AI 助教，回答简洁专业。"),\n        HumanMessage(content="用三句话介绍 LangChain 的核心价值。"),\n    ]\n    if os.getenv("DEEPSEEK_API_KEY"):\n        print(llm.invoke(messages).content)\n    else:\n        print("[MOCK] LangChain 统一 Model/Prompt/Chain 抽象，降低 LLM 应用开发成本。")\n\nif __name__ == "__main__":\n    main()\n',
        'prompt_template.py': '#!/usr/bin/env python3\n"""Day 25: PromptTemplate 与变量注入"""\nimport os\nfrom langchain_core.prompts import ChatPromptTemplate\nfrom langchain_openai import ChatOpenAI\n\nprompt = ChatPromptTemplate.from_messages([\n    ("system", "你是{role}，负责解答{domain}相关问题。"),\n    ("human", "{question}"),\n])\nllm = ChatOpenAI(\n    model="deepseek-chat",\n    api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),\n    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),\n)\nchain = prompt.partial(role="Nexus 知识库助手", domain="RAG") | llm\n\nif __name__ == "__main__":\n    result = chain.invoke({"question": "什么是向量检索？"})\n    print(getattr(result, "content", result))\n',
        'output_parser.py': '#!/usr/bin/env python3\n"""Day 25: JsonOutputParser 结构化输出"""\nimport json\nimport os\nfrom langchain_core.output_parsers import JsonOutputParser\nfrom langchain_core.prompts import PromptTemplate\nfrom langchain_openai import ChatOpenAI\n\nparser = JsonOutputParser()\nprompt = PromptTemplate(\n    template="列出 {topic} 的三个关键点。\\n{format_instructions}",\n    input_variables=["topic"],\n    partial_variables={"format_instructions": parser.get_format_instructions()},\n)\nllm = ChatOpenAI(\n    model="deepseek-chat",\n    api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),\n    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),\n)\nchain = prompt | llm | parser\n\nif __name__ == "__main__":\n    try:\n        data = chain.invoke({"topic": "LangChain"})\n        print(json.dumps(data, ensure_ascii=False, indent=2))\n    except Exception:\n        print({"points": ["Runnable", "LCEL", "集成生态"]})\n',
    },
    homework_desc='修改 hello_langchain.py 的 System Prompt 为「企业知识库客服」，并记录对话到 logs/day25.log。',
    homework_answer_hint="logging.basicConfig(filename='logs/day25.log') 记录输入输出。",
    architecture_mermaid='flowchart LR\\n  USER[用户] --> PROMPT[PromptTemplate]\\n  PROMPT --> LLM[ChatOpenAI]\\n  LLM --> PARSER[OutputParser]',
    narration='**陈工**：Nexus v0.3 进入 RAG 阶段，本周统一 LangChain 技术栈。**林悦**：先跑通最小链再谈优化。',
    key_concepts=['LangChain 核心抽象', 'ChatOpenAI', 'PromptTemplate', 'OutputParser'],
    platform_touches=['为 NexusAgent RAG 服务层引入 LangChain'],
)

DAY_26 = DayPlan(
    day=26,
    title='LCEL 链式表达',
    phase='Phase 3：LangChain RAG 知识库',
    epic='NEXUS-E3',
    jira_stories=['NEXUS-261', 'NEXUS-262'],
    morning=['09:00 LCEL 管道符 | 与 Runnable', '10:00 invoke/stream/batch', '11:00 RunnableLambda 组合'],
    afternoon=['14:00 问答链骨架', '15:30 流式输出', '17:00 单元测试'],
    evening=['19:00 作业：本地 txt 检索', '20:00 预习 Memory'],
    code_files={
        'lcel_basics.py': '#!/usr/bin/env python3\n"""Day 26: LCEL 基础链与流式输出"""\nimport os\nfrom langchain_core.prompts import ChatPromptTemplate\nfrom langchain_core.output_parsers import StrOutputParser\nfrom langchain_openai import ChatOpenAI\n\nprompt = ChatPromptTemplate.from_template("用一句话解释：{concept}")\nllm = ChatOpenAI(\n    model="deepseek-chat",\n    api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),\n    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),\n)\nchain = prompt | llm | StrOutputParser()\n\nif __name__ == "__main__":\n    print(chain.invoke({"concept": "LCEL"}))\n    for chunk in chain.stream({"concept": "Runnable"}):\n        print(chunk, end="", flush=True)\n    print()\n',
        'chain_composition.py': '#!/usr/bin/env python3\n"""Day 26: RunnableLambda 链组合"""\nimport os\nfrom langchain_core.runnables import RunnableLambda, RunnablePassthrough\nfrom langchain_core.prompts import ChatPromptTemplate\nfrom langchain_openai import ChatOpenAI\n\ndef uppercase(text: str) -> str:\n    return text.upper()\n\nprompt = ChatPromptTemplate.from_template("总结工单：{ticket}")\nllm = ChatOpenAI(\n    model="deepseek-chat",\n    api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),\n    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),\n)\nchain = (\n    {"ticket": RunnablePassthrough()} | prompt | llm\n    | RunnableLambda(lambda m: m.content) | RunnableLambda(uppercase)\n)\nif __name__ == "__main__":\n    print(chain.invoke("客户反馈登录慢，已复现。"))\n',
        'rag_chain_stub.py': '#!/usr/bin/env python3\n"""Day 26: RAG 链骨架（检索占位）"""\nimport os\nfrom langchain_core.runnables import RunnablePassthrough, RunnableLambda\nfrom langchain_core.prompts import ChatPromptTemplate\nfrom langchain_core.output_parsers import StrOutputParser\nfrom langchain_openai import ChatOpenAI\n\ndef fake_retrieve(query: str) -> str:\n    return f"[占位上下文] 关于「{query}」的企业文档摘要。"\n\nprompt = ChatPromptTemplate.from_template(\n    "根据上下文回答。\\n上下文：{context}\\n问题：{question}"\n)\nllm = ChatOpenAI(\n    model="deepseek-chat",\n    api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),\n    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),\n)\nrag_chain = (\n    {"context": RunnableLambda(fake_retrieve), "question": RunnablePassthrough()}\n    | prompt | llm | StrOutputParser()\n)\nif __name__ == "__main__":\n    print(rag_chain.invoke("年假政策是什么？"))\n',
    },
    homework_desc='将 rag_chain_stub.py 的 fake_retrieve 改为读取 data/faq.txt 关键词匹配。',
    homework_answer_hint='pathlib 读取，if kw in line 过滤后 join。',
    architecture_mermaid='flowchart LR\\n  Q[问题] --> RET[检索] --> MERGE --> PROMPT --> LLM --> OUT',
    narration='**陈工**：前端要流式输出，LCEL stream 是硬指标。**小王**：管道符比回调清晰。',
    key_concepts=['LCEL 管道', 'Runnable', '链组合', '流式输出'],
    platform_touches=['NexusAgent chat 接入 LCEL 流式链路'],
)

DAY_27 = DayPlan(
    day=27,
    title='Memory 对话记忆',
    phase='Phase 3：LangChain RAG 知识库',
    epic='NEXUS-E3',
    jira_stories=['NEXUS-271', 'NEXUS-272'],
    morning=['09:00 ConversationBufferMemory 原理', '10:00 ChatMessageHistory 持久化', '11:00 多轮对话链'],
    afternoon=['14:00 实现带记忆的客服链', '16:00 Redis 会话存储预习', '17:00 记忆窗口截断策略'],
    evening=['19:00 作业：限制记忆 10 轮', '20:00 预习文档分割'],
    code_files={
        'conversation_buffer.py': '#!/usr/bin/env python3\n"""Day 27: ConversationBufferMemory 多轮对话"""\nimport os\nfrom langchain.memory import ConversationBufferMemory\nfrom langchain.chains import ConversationChain\nfrom langchain_openai import ChatOpenAI\n\ndef build_chain() -> ConversationChain:\n  # 缓冲全部历史消息\n  memory = ConversationBufferMemory()\n  llm = ChatOpenAI(\n    model="deepseek-chat",\n    api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),\n    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),\n  )\n  return ConversationChain(llm=llm, memory=memory, verbose=True)\n\nif __name__ == "__main__":\n  chain = build_chain()\n  print(chain.predict(input="我叫小明，在智链科技实习。"))\n  print(chain.predict(input="我叫什么？在哪实习？"))\n',
        'chat_session.py': '#!/usr/bin/env python3\n"""Day 27: 会话 ID 与内存字典模拟 Redis"""\nfrom __future__ import annotations\nfrom dataclasses import dataclass, field\n\n@dataclass\nclass ChatSession:\n  session_id: str\n  messages: list[dict[str, str]] = field(default_factory=list)\n\n  def append(self, role: str, content: str) -> None:\n    self.messages.append({"role": role, "content": content})\n\n  def context_text(self, max_turns: int = 10) -> str:\n    # 只保留最近 max_turns 轮，防止 token 爆炸\n    recent = self.messages[-(max_turns * 2):]\n    return "\\n".join(f"{m[\'role\']}: {m[\'content\']}" for m in recent)\n\nSESSION_STORE: dict[str, ChatSession] = {}\n\ndef get_session(sid: str) -> ChatSession:\n  if sid not in SESSION_STORE:\n    SESSION_STORE[sid] = ChatSession(session_id=sid)\n  return SESSION_STORE[sid]\n\nif __name__ == "__main__":\n  s = get_session("user-001")\n  s.append("user", "Nexus 支持私有化吗？")\n  s.append("assistant", "支持 Docker 私有化部署。")\n  print(s.context_text())\n',
        'memory_window.py': '#!/usr/bin/env python3\n"""Day 27: ConversationBufferWindowMemory 滑动窗口"""\nimport os\nfrom langchain.memory import ConversationBufferWindowMemory\nfrom langchain.chains import ConversationChain\nfrom langchain_openai import ChatOpenAI\n\nmemory = ConversationBufferWindowMemory(k=2)  # 仅保留最近 2 轮\nllm = ChatOpenAI(\n  model="deepseek-chat",\n  api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),\n  base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),\n)\nchain = ConversationChain(llm=llm, memory=memory)\n\nif __name__ == "__main__":\n  for q in ["A", "B", "C", "你还记得 A 吗？"]:\n    print("Q:", q)\n    print("A:", chain.predict(input=q)[:80])\n',
    },
    homework_desc='扩展 chat_session.py：将会话序列化到 data/sessions/{id}.json，重启可恢复。',
    homework_answer_hint='json.dump(messages) 写入，启动时 json.load 恢复。',
    architecture_mermaid='flowchart LR\\n  USER --> CHAIN --> MEMORY --> LLM\\n  MEMORY --> HISTORY[(消息历史)]',
    narration='**林悦**：客服场景必须记住上文。**陈工**：生产用 Redis，今天先用内存字典理解模型。',
    key_concepts=['ConversationBufferMemory', '滑动窗口', '会话持久化', 'token 控制'],
    platform_touches=['对齐 NexusAgent Redis 会话模块设计'],
)

DAY_28 = DayPlan(
    day=28,
    title='文档分割',
    phase='Phase 3：LangChain RAG 知识库',
    epic='NEXUS-E3',
    jira_stories=['NEXUS-281', 'NEXUS-282'],
    morning=['09:00 为何需要 Chunking', '10:00 RecursiveCharacterTextSplitter', '11:00 按标题/语义分割'],
    afternoon=['14:00 加载 PDF/TXT', '15:30 chunk_size 实验', '17:00 overlap 对召回的影响'],
    evening=['19:00 作业：分割公司手册', '20:00 预习 Chroma'],
    code_files={
        'text_splitter.py': '#!/usr/bin/env python3\n"""Day 28: RecursiveCharacterTextSplitter 文档切分"""\nfrom langchain_text_splitters import RecursiveCharacterTextSplitter\n\nSAMPLE = """\n# Nexus 员工手册\n## 考勤制度\n员工应按时打卡。迟到三次记警告。\n## 年假\n工作满一年享 5 天年假。\n## 报销\n差旅费需附发票，30 日内提交。\n""" * 3\n\ndef split_document(text: str, chunk_size: int = 200, overlap: int = 50) -> list[str]:\n  splitter = RecursiveCharacterTextSplitter(\n    chunk_size=chunk_size,\n    chunk_overlap=overlap,\n    separators=["\\n## ", "\\n", "。", " "],\n  )\n  return splitter.split_text(text)\n\nif __name__ == "__main__":\n  chunks = split_document(SAMPLE)\n  for i, ch in enumerate(chunks):\n    print(f"--- chunk {i} ({len(ch)} chars) ---")\n    print(ch[:120])\n',
        'doc_loader.py': '#!/usr/bin/env python3\n"""Day 28: 文档加载与元数据"""\nfrom pathlib import Path\nfrom langchain_community.document_loaders import TextLoader\nfrom langchain_text_splitters import RecursiveCharacterTextSplitter\n\ndef load_and_split(path: Path) -> list:\n  loader = TextLoader(str(path), encoding="utf-8")\n  docs = loader.load()\n  splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=60)\n  chunks = splitter.split_documents(docs)\n  for c in chunks:\n    c.metadata["source_file"] = path.name\n  return chunks\n\nif __name__ == "__main__":\n  p = Path("data/handbook.txt")\n  p.parent.mkdir(exist_ok=True)\n  if not p.exists():\n    p.write_text("Nexus 平台支持 RAG 知识库问答。", encoding="utf-8")\n  for doc in load_and_split(p):\n    print(doc.metadata, doc.page_content[:60])\n',
        'chunk_experiment.py': '#!/usr/bin/env python3\n"""Day 28: chunk_size / overlap 对比实验"""\nfrom text_splitter import split_document, SAMPLE\n\nif __name__ == "__main__":\n  for size, ov in [(100, 20), (300, 50), (500, 100)]:\n    chunks = split_document(SAMPLE, size, ov)\n    print(f"size={size} overlap={ov} -> {len(chunks)} chunks")\n',
    },
    homework_desc='将 data/handbook.txt 按 ## 标题分割，每个 chunk 附带 section 元数据。',
    homework_answer_hint='MarkdownHeaderTextSplitter 或手动解析标题写入 metadata。',
    architecture_mermaid='flowchart LR\\n  DOC[原始文档] --> LOAD[Loader] --> SPLIT[Splitter] --> CHUNKS[文本块]',
    narration='**陈工**：Chunk 太大检索不准，太小丢上下文。今天用实验找甜蜜点。',
    key_concepts=['RecursiveCharacterTextSplitter', 'chunk_overlap', 'Document Loader', '元数据'],
    platform_touches=['Nexus RAG 文档入库管道第一步'],
)

DAY_29 = DayPlan(
    day=29,
    title='向量库 Chroma',
    phase='Phase 3：LangChain RAG 知识库',
    epic='NEXUS-E3',
    jira_stories=['NEXUS-291', 'NEXUS-292'],
    morning=['09:00 Embedding 原理回顾', '10:00 Chroma 本地持久化', '11:00 similarity_search'],
    afternoon=['14:00 文档向量化入库', '16:00 相似度检索调试', '17:00 集合管理'],
    evening=['19:00 作业：FAQ 向量库', '20:00 预习完整 RAG'],
    code_files={
        'chroma_basics.py': '#!/usr/bin/env python3\n"""Day 29: Chroma 向量库基础"""\nimport os\nfrom langchain_chroma import Chroma\nfrom langchain_openai import OpenAIEmbeddings\n\ndef build_vectorstore(texts: list[str], persist_dir: str = "./chroma_db") -> Chroma:\n  embeddings = OpenAIEmbeddings(\n    model=os.getenv("EMBED_MODEL", "text-embedding-3-small"),\n    api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),\n    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),\n  )\n  return Chroma.from_texts(texts, embedding=embeddings, persist_directory=persist_dir)\n\nif __name__ == "__main__":\n  faq = ["Nexus 支持 DeepSeek", "年假 5 天起", "报销需发票"]\n  vs = build_vectorstore(faq)\n  results = vs.similarity_search("用什么模型？", k=2)\n  for r in results:\n    print(r.page_content)\n',
        'embeddings_demo.py': '#!/usr/bin/env python3\n"""Day 29: Embedding 向量维度与余弦相似度"""\nimport math\n\ndef cosine(a: list[float], b: list[float]) -> float:\n  dot = sum(x * y for x, y in zip(a, b))\n  na = math.sqrt(sum(x * x for x in a))\n  nb = math.sqrt(sum(x * x for x in b))\n  return dot / (na * nb) if na and nb else 0.0\n\n# 教学用伪向量\nv1 = [1.0, 0.2, 0.1]\nv2 = [0.9, 0.3, 0.0]\nv3 = [0.0, 1.0, 0.0]\nprint("相似问句:", cosine(v1, v2))\nprint("无关问句:", cosine(v1, v3))\n',
        'ingest_chroma.py': '#!/usr/bin/env python3\n"""Day 29: 切分文档并写入 Chroma"""\nfrom pathlib import Path\nfrom doc_loader import load_and_split\nfrom chroma_basics import build_vectorstore\n\nif __name__ == "__main__":\n  p = Path("data/handbook.txt")\n  chunks = load_and_split(p)\n  texts = [c.page_content for c in chunks]\n  vs = build_vectorstore(texts, persist_dir="./data/chroma_handbook")\n  print("入库完成，共", len(texts), "条")\n',
    },
    homework_desc='构建 data/faq_chroma，包含 20 条 FAQ，实现 similarity_search_with_score 打印分数。',
    homework_answer_hint='Chroma.from_texts 后调用 similarity_search_with_score(query, k=3)。',
    architecture_mermaid='flowchart LR\\n  CHUNKS --> EMB[Embedding] --> CHROMA[(Chroma)]\\n  Q --> EMB --> SEARCH[相似检索]',
    narration='**陈工**：Chroma 本地够用，生产可换 Milvus。**运维**：persist_directory 要挂载卷。',
    key_concepts=['Chroma', 'Embedding', 'similarity_search', '持久化'],
    platform_touches=['NexusAgent 向量库默认 Chroma 实现'],
)

DAY_30 = DayPlan(
    day=30,
    title='完整 RAG',
    phase='Phase 3：LangChain RAG 知识库',
    epic='NEXUS-E3',
    jira_stories=['NEXUS-301', 'NEXUS-302'],
    morning=['09:00 RAG 架构：检索+生成', '10:00 RetrievalQA 链', '11:00 引用溯源'],
    afternoon=['14:00 端到端问答', '16:00 检索结果注入 Prompt', '17:00 幻觉检测'],
    evening=['19:00 作业：带来源回答', '20:00 预习调优'],
    code_files={
        'rag_pipeline.py': '#!/usr/bin/env python3\n"""Day 30: 完整 RAG 管道"""\nimport os\nfrom langchain_chroma import Chroma\nfrom langchain_openai import ChatOpenAI, OpenAIEmbeddings\nfrom langchain.chains import RetrievalQA\nfrom langchain_core.prompts import PromptTemplate\n\nPROMPT = PromptTemplate(\n  template="""根据以下上下文回答问题，不知道就说不知道。\n上下文：\n{context}\n问题：{question}\n回答（中文，简洁）：""",\n  input_variables=["context", "question"],\n)\n\ndef build_rag(persist_dir: str = "./data/chroma_handbook") -> RetrievalQA:\n  emb = OpenAIEmbeddings(\n    api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),\n    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),\n  )\n  vs = Chroma(persist_directory=persist_dir, embedding_function=emb)\n  retriever = vs.as_retriever(search_kwargs={"k": 3})\n  llm = ChatOpenAI(\n    model="deepseek-chat",\n    api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),\n    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),\n  )\n  return RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")\n\nif __name__ == "__main__":\n  qa = build_rag()\n  print(qa.invoke({"query": "年假有几天？"}))\n',
        'rag_with_sources.py': '#!/usr/bin/env python3\n"""Day 30: 带引用溯源的 RAG"""\nfrom langchain_core.runnables import RunnablePassthrough\nfrom langchain_core.output_parsers import StrOutputParser\nfrom langchain_core.prompts import ChatPromptTemplate\nfrom rag_pipeline import build_rag\n\ndef format_docs(docs) -> str:\n  parts = []\n  for i, d in enumerate(docs, 1):\n    src = d.metadata.get("source_file", "unknown")\n    parts.append(f"[{i}] ({src}) {d.page_content}")\n  return "\\n\\n".join(parts)\n\nif __name__ == "__main__":\n  qa = build_rag()\n  retriever = qa.retriever\n  prompt = ChatPromptTemplate.from_template(\n    "上下文：\\n{context}\\n\\n问题：{question}\\n请回答并标注引用编号。"\n  )\n  chain = (\n    {"context": retriever | format_docs, "question": RunnablePassthrough()}\n    | prompt | qa.chain.llm | StrOutputParser()\n  )\n  print(chain.invoke("报销流程是什么？"))\n',
        'hallucination_check.py': '#!/usr/bin/env python3\n"""Day 30: 简单幻觉检测 — 答案是否包含上下文关键词"""\n\ndef grounded(answer: str, context: str, min_overlap: int = 2) -> bool:\n  # 教学用启发式：答案中至少 min_overlap 个上下文词出现\n  tokens = [t for t in context.split() if len(t) > 1]\n  hits = sum(1 for t in set(tokens) if t in answer)\n  return hits >= min_overlap\n\nif __name__ == "__main__":\n  ctx = "年假 5 天 工作满一年"\n  print(grounded("工作满一年有 5 天年假", ctx))\n  print(grounded("无限年假随便休", ctx))\n',
    },
    homework_desc='扩展 rag_with_sources.py：返回答案 + sources 列表 JSON。',
    homework_answer_hint="return {'answer': ..., 'sources': [d.metadata for d in docs]}",
    architecture_mermaid='flowchart TD\\n  Q --> RET[Retriever] --> CTX[上下文]\\n  Q --> LLM\\n  CTX --> LLM --> A[答案+引用]',
    narration='**林悦**：客户要求每句答案能点开原文。**陈工**：metadata.source_file 就是溯源关键。',
    key_concepts=['RetrievalQA', '引用溯源', 'stuff chain', '幻觉检测'],
    platform_touches=['NexusAgent v0.3 RAG 核心链路'],
)

DAY_31 = DayPlan(
    day=31,
    title='周测与 RAG 调优',
    phase='Phase 3：LangChain RAG 知识库',
    epic='NEXUS-E3',
    jira_stories=['NEXUS-311', 'NEXUS-312'],
    morning=['09:00 周测讲评', '10:00 top_k / chunk_size 调参', '11:00 temperature 对忠实度的影响'],
    afternoon=['14:00 A/B 对比实验', '16:00 构建评测集', '17:00 调优报告'],
    evening=['19:00 整理调优 checklist', '20:00 预习高级 RAG'],
    code_files={
        'rag_tuning.py': '#!/usr/bin/env python3\n"""Day 31: RAG 超参数网格搜索"""\nfrom dataclasses import dataclass\n\n@dataclass\nclass RagConfig:\n  chunk_size: int\n  top_k: int\n  temperature: float\n\nEVAL_QUERIES = [\n  ("年假几天", "5"),\n  ("报销要什么", "发票"),\n]\n\ndef score_config(cfg: RagConfig) -> float:\n  # 教学 mock：chunk 适中、top_k=3、temperature 低 得分高\n  s = 0.0\n  if 200 <= cfg.chunk_size <= 400: s += 0.4\n  if cfg.top_k == 3: s += 0.3\n  if cfg.temperature <= 0.3: s += 0.3\n  return s\n\nif __name__ == "__main__":\n  best = max(\n    [RagConfig(cs, k, t) for cs in [200, 300, 500] for k in [2, 3, 5] for t in [0.0, 0.3, 0.7]],\n    key=score_config,\n  )\n  print("最佳配置:", best, "score=", score_config(best))\n',
        'ab_test.py': '#!/usr/bin/env python3\n"""Day 31: A/B 测试记录"""\nimport json\nfrom pathlib import Path\n\ndef log_result(variant: str, query: str, answer: str, score: float) -> None:\n  p = Path("logs/ab_test.jsonl")\n  p.parent.mkdir(exist_ok=True)\n  with p.open("a", encoding="utf-8") as f:\n    f.write(json.dumps({"variant": variant, "query": query, "answer": answer, "score": score}, ensure_ascii=False) + "\\n")\n\nif __name__ == "__main__":\n  log_result("A_k2", "年假", "5天", 0.9)\n  log_result("B_k5", "年假", "5天年假", 0.85)\n',
        'eval_set.json': '[\n  {"query": "年假有几天", "expected_keywords": ["5", "年假"]},\n  {"query": "怎么报销", "expected_keywords": ["发票", "30"]}\n]\n',
    },
    homework_desc='用 eval_set.json 跑 5 组配置，输出 Markdown 调优报告。',
    homework_answer_hint='遍历配置，检查 expected_keywords 是否出现在答案中。',
    architecture_mermaid='flowchart LR\\n  CFG[超参数] --> RAG --> EVAL[评测集] --> REPORT[报告]',
    narration='**陈工**：没有评测集的调优是玄学。今天建立 Nexus RAG baseline。',
    key_concepts=['超参数调优', 'A/B 测试', '评测集', 'baseline'],
    platform_touches=['建立 Nexus RAG 性能 baseline'],
)

DAY_32 = DayPlan(
    day=32,
    title='高级 RAG（上）',
    phase='Phase 3：LangChain RAG 知识库',
    epic='NEXUS-E3',
    jira_stories=['NEXUS-321', 'NEXUS-322'],
    morning=['09:00 Query Transformation', '10:00 Multi-Query Retriever', '11:00 HyDE 概念'],
    afternoon=['14:00 查询扩展实现', '16:00 Reranker 接入', '17:00 效果对比'],
    evening=['19:00 作业：Multi-Query', '20:00 预习混合检索'],
    code_files={
        'query_expansion.py': '#!/usr/bin/env python3\n"""Day 32: 多查询扩展检索"""\nimport os\nfrom langchain_openai import ChatOpenAI\nfrom langchain_core.prompts import ChatPromptTemplate\nfrom langchain_core.output_parsers import StrOutputParser\n\nprompt = ChatPromptTemplate.from_template(\n  "将用户问题改写成 3 个不同表述的检索查询，每行一个：\\n{question}"\n)\nllm = ChatOpenAI(\n  model="deepseek-chat",\n  api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),\n  base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),\n)\nexpand_chain = prompt | llm | StrOutputParser()\n\ndef multi_query(question: str) -> list[str]:\n  text = expand_chain.invoke({"question": question})\n  return [line.strip() for line in text.splitlines() if line.strip()][:3]\n\nif __name__ == "__main__":\n  print(multi_query("员工年假怎么算？"))\n',
        'reranker.py': '#!/usr/bin/env python3\n"""Day 32: 简易 Reranker — 按关键词重叠重排"""\nfrom dataclasses import dataclass\n\n@dataclass\nclass Doc:\n  text: str\n  score: float = 0.0\n\ndef rerank(query: str, docs: list[Doc]) -> list[Doc]:\n  q_tokens = set(query)\n  for d in docs:\n    d.score = sum(1 for c in q_tokens if c in d.text) / max(len(q_tokens), 1)\n  return sorted(docs, key=lambda x: x.score, reverse=True)\n\nif __name__ == "__main__":\n  docs = [Doc("年假 5 天"), Doc("报销发票"), Doc("考勤打卡")]\n  for d in rerank("年假", docs):\n    print(d.score, d.text)\n',
        'hyde_stub.py': '#!/usr/bin/env python3\n"""Day 32: HyDE — 先生成假设文档再检索（占位）"""\nimport os\nfrom langchain_openai import ChatOpenAI\n\nllm = ChatOpenAI(\n  model="deepseek-chat",\n  api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),\n  base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),\n)\n\ndef hyde_query(question: str) -> str:\n  # 生成一段「假设性答案」作为检索 query\n  return f"假设文档：关于「{question}」的标准解答段落..."\n\nif __name__ == "__main__":\n  print(hyde_query("远程办公政策"))\n',
    },
    homework_desc='实现 Multi-Query Retriever：扩展 3 个 query 分别检索后去重合并。',
    homework_answer_hint='对每个 query 调用 retriever，用 set 按 page_content 去重。',
    architecture_mermaid='flowchart TD\\n  Q --> EXP[查询扩展] --> Q1 Q2 Q3\\n  Q1 --> RET --> MERGE --> RERANK',
    narration='**陈工**：用户问法千奇百怪，Multi-Query 是性价比最高的高级技巧。',
    key_concepts=['Query Expansion', 'Multi-Query', 'Reranker', 'HyDE'],
    platform_touches=['Nexus 检索层支持多查询扩展'],
)

DAY_33 = DayPlan(
    day=33,
    title='高级 RAG（下）混合检索',
    phase='Phase 3：LangChain RAG 知识库',
    epic='NEXUS-E3',
    jira_stories=['NEXUS-331', 'NEXUS-332'],
    morning=['09:00 BM25 关键词检索', '10:00 向量+BM25 融合', '11:00 Ensemble Retriever'],
    afternoon=['14:00 实现混合检索', '16:00 权重调优', '17:00 稀疏稠密对比'],
    evening=['19:00 作业：alpha 参数实验', '20:00 预习 Ragas'],
    code_files={
        'bm25_search.py': '#!/usr/bin/env python3\n"""Day 33: 简易 BM25 关键词检索"""\nimport math\nfrom collections import Counter\n\ndef bm25_score(query: str, doc: str, avgdl: float = 100, k1: float = 1.5, b: float = 0.75) -> float:\n  q_terms = query.split()\n  d_terms = doc.split()\n  dl = len(d_terms)\n  tf = Counter(d_terms)\n  score = 0.0\n  for t in q_terms:\n    if t in tf:\n      freq = tf[t]\n      score += (freq * (k1 + 1)) / (freq + k1 * (1 - b + b * dl / avgdl))\n  return score\n\nCORPUS = ["年假 5 天 工作满一年", "报销 需要 发票 30 日", "远程 办公 需 申请"]\n\nif __name__ == "__main__":\n  q = "年假"\n  ranked = sorted(CORPUS, key=lambda d: bm25_score(q, d), reverse=True)\n  print(ranked)\n',
        'hybrid_search.py': '#!/usr/bin/env python3\n"""Day 33: 向量 + BM25 混合检索"""\nfrom bm25_search import bm25_score, CORPUS\n\ndef dense_score(query: str, doc: str) -> float:\n  # 教学 mock：字符重叠\n  return sum(1 for c in query if c in doc) / max(len(query), 1)\n\ndef hybrid_search(query: str, alpha: float = 0.5) -> list[tuple[str, float]]:\n  results = []\n  for doc in CORPUS:\n    s = alpha * dense_score(query, doc) + (1 - alpha) * bm25_score(query, doc)\n    results.append((doc, s))\n  return sorted(results, key=lambda x: x[1], reverse=True)\n\nif __name__ == "__main__":\n  for doc, s in hybrid_search("年假政策", alpha=0.6):\n    print(f"{s:.3f} {doc}")\n',
        'ensemble_retriever.py': '#!/usr/bin/env python3\n"""Day 33: Ensemble Retriever 概念演示"""\nfrom hybrid_search import hybrid_search\n\nclass EnsembleRetriever:\n  def __init__(self, alpha: float = 0.5):\n    self.alpha = alpha\n\n  def invoke(self, query: str, k: int = 3) -> list[str]:\n    return [d for d, _ in hybrid_search(query, self.alpha)[:k]]\n\nif __name__ == "__main__":\n  r = EnsembleRetriever(0.5)\n  print(r.invoke("报销流程"))\n',
    },
    homework_desc='对 alpha=0.0,0.3,0.5,0.7,1.0 跑评测集，绘制准确率曲线（可用 print 表格）。',
    homework_answer_hint='遍历 alpha，统计 expected_keywords 命中率。',
    architecture_mermaid='flowchart LR\\n  Q --> BM25\\n  Q --> DENSE[向量]\\n  BM25 --> FUSE[加权融合]\\n  DENSE --> FUSE',
    narration='**陈工**：专有名词用 BM25，语义用向量，混合检索是企业标配。',
    key_concepts=['BM25', '混合检索', 'Ensemble', 'alpha 融合'],
    platform_touches=['Nexus 检索服务支持 hybrid 模式'],
)

DAY_34 = DayPlan(
    day=34,
    title='Ragas 评估',
    phase='Phase 3：LangChain RAG 知识库',
    epic='NEXUS-E3',
    jira_stories=['NEXUS-341', 'NEXUS-342'],
    morning=['09:00 RAG 评估指标', '10:00 faithfulness / answer_relevancy', '11:00 Ragas 框架'],
    afternoon=['14:00 构建评估数据集', '16:00 跑 Ragas 评测', '17:00 解读报告'],
    evening=['19:00 作业：5 条人工标注', '20:00 预习 LlamaIndex'],
    code_files={
        'ragas_eval.py': '#!/usr/bin/env python3\n"""Day 34: Ragas 评估（可选依赖，无则 mock）"""\nfrom dataclasses import dataclass\n\n@dataclass\nclass RagSample:\n  question: str\n  answer: str\n  contexts: list[str]\n  ground_truth: str\n\ndef faithfulness(answer: str, contexts: list[str]) -> float:\n  # 答案是否可由上下文推出\n  ctx = " ".join(contexts)\n  overlap = sum(1 for w in answer.split() if w in ctx)\n  return min(overlap / max(len(answer.split()), 1), 1.0)\n\ndef answer_relevancy(answer: str, question: str) -> float:\n  overlap = sum(1 for w in question.split() if w in answer)\n  return min(overlap / max(len(question.split()), 1), 1.0)\n\nif __name__ == "__main__":\n  s = RagSample("年假几天", "5天年假", ["工作满一年享5天年假"], "5天")\n  print("faithfulness:", faithfulness(s.answer, s.contexts))\n  print("relevancy:", answer_relevancy(s.answer, s.question))\n',
        'eval_dataset.json': '[\n  {"question": "年假有几天", "ground_truth": "5天", "contexts": ["工作满一年享5天年假"]},\n  {"question": "报销期限", "ground_truth": "30日内", "contexts": ["差旅费30日内提交"]}\n]\n',
        'run_ragas.py': '#!/usr/bin/env python3\n"""Day 34: 批量评估脚本"""\nimport json\nfrom pathlib import Path\nfrom ragas_eval import RagSample, faithfulness, answer_relevancy\n\ndef run_eval() -> None:\n  data = json.loads(Path("eval_dataset.json").read_text(encoding="utf-8"))\n  for row in data:\n    ans = row.get("predicted", row["ground_truth"])\n    f = faithfulness(ans, row["contexts"])\n    r = answer_relevancy(ans, row["question"])\n    print(row["question"], f"F={f:.2f} R={r:.2f}")\n\nif __name__ == "__main__":\n  run_eval()\n',
    },
    homework_desc='扩展 eval_dataset.json 至 10 条，接入真实 RAG 输出跑评估。',
    homework_answer_hint='对每条 question 调用 rag_pipeline，将 answer 写入 predicted 字段。',
    architecture_mermaid='flowchart LR\\n  RAG --> PRED[预测]\\n  GT[标注] --> RAGAS --> METRICS[指标]',
    narration='**林悦**：没有 Ragas 报告不准上线。**陈工**：faithfulness 低就是幻觉重灾区。',
    key_concepts=['Ragas', 'faithfulness', 'answer_relevancy', '评估数据集'],
    platform_touches=['Nexus RAG 质量门禁指标'],
)

DAY_35 = DayPlan(
    day=35,
    title='LlamaIndex',
    phase='Phase 3：LangChain RAG 知识库',
    epic='NEXUS-E3',
    jira_stories=['NEXUS-351', 'NEXUS-352'],
    morning=['09:00 LlamaIndex vs LangChain', '10:00 VectorStoreIndex', '11:00 QueryEngine'],
    afternoon=['14:00 文档索引构建', '16:00 对比 LangChain RAG', '17:00 选型讨论'],
    evening=['19:00 作业：LlamaIndex 索引', '20:00 预习企业知识库项目'],
    code_files={
        'llamaindex_basics.py': '#!/usr/bin/env python3\n"""Day 35: LlamaIndex 基础索引（可选依赖）"""\nfrom pathlib import Path\n\ndef mock_index(texts: list[str]) -> dict:\n  # 无 llama-index 时的教学占位\n  return {f"doc_{i}": t for i, t in enumerate(texts)}\n\ndef query(index: dict, q: str) -> str:\n  for k, v in index.items():\n    if any(c in v for c in q):\n      return v\n  return "未找到相关文档"\n\nif __name__ == "__main__":\n  idx = mock_index(["年假5天", "报销需发票"])\n  print(query(idx, "年假"))\n',
        'index_query.py': '#!/usr/bin/env python3\n"""Day 35: LlamaIndex QueryEngine 概念"""\ntry:\n  from llama_index.core import VectorStoreIndex, Document\n  HAS_LLAMA = True\nexcept ImportError:\n  HAS_LLAMA = False\n\ndef build_engine(texts: list[str]):\n  if not HAS_LLAMA:\n    from llamaindex_basics import mock_index, query\n    idx = mock_index(texts)\n    return lambda q: query(idx, q)\n  docs = [Document(text=t) for t in texts]\n  index = VectorStoreIndex.from_documents(docs)\n  return index.as_query_engine()\n\nif __name__ == "__main__":\n  engine = build_engine(["Nexus 支持 RAG", "Agent 编排用 LangGraph"])\n  print(engine("RAG 用什么？"))\n',
        'compare_frameworks.md': '# LangChain vs LlamaIndex\n\n| 维度 | LangChain | LlamaIndex |\n|------|-----------|------------|\n| 定位 | 通用 LLM 编排 | 数据索引与检索 |\n| RAG | 链式组合灵活 | 索引 API 简洁 |\n| 选型 | Agent + 多工具 | 重度知识库场景 |\n',
    },
    homework_desc='用 LlamaIndex 或 mock 实现 handbook 索引，对比与 LangChain RAG 延迟。',
    homework_answer_hint='time.perf_counter() 计时 invoke。',
    architecture_mermaid='flowchart LR\\n  DOCS --> INDEX[LlamaIndex] --> ENGINE[QueryEngine] --> ANS',
    narration='**陈工**：不是二选一，Nexus 检索层可抽象，上层换框架。',
    key_concepts=['LlamaIndex', 'VectorStoreIndex', 'QueryEngine', '框架选型'],
    platform_touches=['评估 Nexus 检索层框架抽象可行性'],
)

DAY_36 = DayPlan(
    day=36,
    title='企业知识库项目（上）',
    phase='Phase 3：LangChain RAG 知识库',
    epic='NEXUS-E3',
    jira_stories=['NEXUS-361', 'NEXUS-362', 'NEXUS-363'],
    morning=['09:00 项目需求评审', '10:00 架构设计：ingest/retriever/api', '11:00 环境搭建'],
    afternoon=['14:00 实现 config + ingest', '16:00 文档上传与切分', '17:00 向量入库验证'],
    evening=['19:00 继续 retriever', '20:00 联调准备'],
    code_files={
        'enterprise_kb/config.py': '#!/usr/bin/env python3\n"""企业知识库项目 — 配置模块"""\nimport os\nfrom pathlib import Path\n\n# 数据与向量库路径\nDATA_DIR = Path(os.getenv("NEXUS_DATA_DIR", "data"))\nCHROMA_DIR = DATA_DIR / "chroma_enterprise"\nUPLOAD_DIR = DATA_DIR / "uploads"\n\n# 模型配置\nLLM_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")\nEMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")\nAPI_KEY = os.getenv("DEEPSEEK_API_KEY", "")\nAPI_BASE = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")\n\n# RAG 超参数\nCHUNK_SIZE = 400\nCHUNK_OVERLAP = 80\nTOP_K = 4\n',
        'enterprise_kb/ingest.py': '#!/usr/bin/env python3\n"""企业知识库 — 文档入库管道"""\nfrom pathlib import Path\nfrom langchain_community.document_loaders import TextLoader, DirectoryLoader\nfrom langchain_text_splitters import RecursiveCharacterTextSplitter\nfrom langchain_chroma import Chroma\nfrom langchain_openai import OpenAIEmbeddings\nfrom config import UPLOAD_DIR, CHROMA_DIR, CHUNK_SIZE, CHUNK_OVERLAP, API_KEY, API_BASE, EMBED_MODEL\n\ndef load_documents(src: Path) -> list:\n  if src.is_file():\n    return TextLoader(str(src), encoding="utf-8").load()\n  loader = DirectoryLoader(str(src), glob="**/*.txt", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"})\n  return loader.load()\n\ndef ingest(src: Path) -> int:\n  docs = load_documents(src)\n  splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)\n  chunks = splitter.split_documents(docs)\n  emb = OpenAIEmbeddings(model=EMBED_MODEL, api_key=API_KEY or "mock", base_url=API_BASE)\n  Chroma.from_documents(chunks, embedding=emb, persist_directory=str(CHROMA_DIR))\n  return len(chunks)\n\nif __name__ == "__main__":\n  UPLOAD_DIR.mkdir(parents=True, exist_ok=True)\n  sample = UPLOAD_DIR / "policy.txt"\n  if not sample.exists():\n    sample.write_text("智链科技员工手册：年假5天，报销需发票。", encoding="utf-8")\n  print("入库 chunks:", ingest(UPLOAD_DIR))\n',
        'enterprise_kb/retriever.py': '#!/usr/bin/env python3\n"""企业知识库 — 检索与问答"""\nimport os\nfrom langchain_chroma import Chroma\nfrom langchain_openai import OpenAIEmbeddings, ChatOpenAI\nfrom langchain.chains import RetrievalQA\nfrom config import CHROMA_DIR, API_KEY, API_BASE, EMBED_MODEL, LLM_MODEL, TOP_K\n\ndef build_qa() -> RetrievalQA:\n  emb = OpenAIEmbeddings(model=EMBED_MODEL, api_key=API_KEY or "mock", base_url=API_BASE)\n  vs = Chroma(persist_directory=str(CHROMA_DIR), embedding_function=emb)\n  retriever = vs.as_retriever(search_kwargs={"k": TOP_K})\n  llm = ChatOpenAI(model=LLM_MODEL, api_key=API_KEY or "mock", base_url=API_BASE, temperature=0.1)\n  return RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)\n\nif __name__ == "__main__":\n  qa = build_qa()\n  r = qa({"query": "年假有几天？"})\n  print(r["result"])\n',
        'enterprise_kb/api.py': '#!/usr/bin/env python3\n"""企业知识库 — FastAPI 接口"""\nfrom fastapi import FastAPI, UploadFile, File\nfrom pydantic import BaseModel\nfrom pathlib import Path\nfrom ingest import ingest\nfrom retriever import build_qa\nfrom config import UPLOAD_DIR\n\napp = FastAPI(title="Nexus Enterprise KB")\nqa_chain = None\n\nclass QueryRequest(BaseModel):\n  question: str\n\n@app.on_event("startup")\ndef startup() -> None:\n  global qa_chain\n  qa_chain = build_qa()\n\n@app.post("/upload")\nasync def upload(file: UploadFile = File(...)):\n  UPLOAD_DIR.mkdir(parents=True, exist_ok=True)\n  dest = UPLOAD_DIR / file.filename\n  dest.write_bytes(await file.read())\n  n = ingest(dest)\n  return {"status": "ok", "chunks": n}\n\n@app.post("/query")\ndef query(req: QueryRequest):\n  r = qa_chain({"query": req.question})\n  sources = [d.metadata for d in r.get("source_documents", [])]\n  return {"answer": r["result"], "sources": sources}\n\nif __name__ == "__main__":\n  import uvicorn\n  uvicorn.run(app, host="0.0.0.0", port=8000)\n',
    },
    homework_desc='完成 ingest.py，支持目录批量导入 txt，输出入库日志。',
    homework_answer_hint="DirectoryLoader glob='**/*.txt' 遍历 uploads。",
    architecture_mermaid='flowchart TD\\n  UPLOAD[上传] --> INGEST --> CHROMA[(Chroma)]\\n  CHROMA --> RET[Retriever]',
    narration='**林悦**：这是 v0.3 里程碑交付。**陈工**：先打通 ingest，明天接 API。',
    key_concepts=['项目架构', '文档入库', 'Chroma 持久化', '模块化设计'],
    platform_touches=['NexusAgent v0.3 企业知识库 MVP'],
)

DAY_37 = DayPlan(
    day=37,
    title='企业知识库项目（下）',
    phase='Phase 3：LangChain RAG 知识库',
    epic='NEXUS-E3',
    jira_stories=['NEXUS-371', 'NEXUS-372'],
    morning=['09:00 实现 retriever 带溯源', '10:30 FastAPI 接口设计', '11:00 上传接口'],
    afternoon=['14:00 联调 query 接口', '16:00 Streamlit UI', '17:00 集成测试'],
    evening=['19:00 准备答辩材料', '20:00 彩排'],
    code_files={
        'enterprise_kb/config.py': '#!/usr/bin/env python3\n"""企业知识库项目 — 配置模块"""\nimport os\nfrom pathlib import Path\n\n# 数据与向量库路径\nDATA_DIR = Path(os.getenv("NEXUS_DATA_DIR", "data"))\nCHROMA_DIR = DATA_DIR / "chroma_enterprise"\nUPLOAD_DIR = DATA_DIR / "uploads"\n\n# 模型配置\nLLM_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")\nEMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")\nAPI_KEY = os.getenv("DEEPSEEK_API_KEY", "")\nAPI_BASE = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")\n\n# RAG 超参数\nCHUNK_SIZE = 400\nCHUNK_OVERLAP = 80\nTOP_K = 4\n',
        'enterprise_kb/ingest.py': '#!/usr/bin/env python3\n"""企业知识库 — 文档入库管道"""\nfrom pathlib import Path\nfrom langchain_community.document_loaders import TextLoader, DirectoryLoader\nfrom langchain_text_splitters import RecursiveCharacterTextSplitter\nfrom langchain_chroma import Chroma\nfrom langchain_openai import OpenAIEmbeddings\nfrom config import UPLOAD_DIR, CHROMA_DIR, CHUNK_SIZE, CHUNK_OVERLAP, API_KEY, API_BASE, EMBED_MODEL\n\ndef load_documents(src: Path) -> list:\n  if src.is_file():\n    return TextLoader(str(src), encoding="utf-8").load()\n  loader = DirectoryLoader(str(src), glob="**/*.txt", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"})\n  return loader.load()\n\ndef ingest(src: Path) -> int:\n  docs = load_documents(src)\n  splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)\n  chunks = splitter.split_documents(docs)\n  emb = OpenAIEmbeddings(model=EMBED_MODEL, api_key=API_KEY or "mock", base_url=API_BASE)\n  Chroma.from_documents(chunks, embedding=emb, persist_directory=str(CHROMA_DIR))\n  return len(chunks)\n\nif __name__ == "__main__":\n  UPLOAD_DIR.mkdir(parents=True, exist_ok=True)\n  sample = UPLOAD_DIR / "policy.txt"\n  if not sample.exists():\n    sample.write_text("智链科技员工手册：年假5天，报销需发票。", encoding="utf-8")\n  print("入库 chunks:", ingest(UPLOAD_DIR))\n',
        'enterprise_kb/retriever.py': '#!/usr/bin/env python3\n"""企业知识库 — 检索与问答"""\nimport os\nfrom langchain_chroma import Chroma\nfrom langchain_openai import OpenAIEmbeddings, ChatOpenAI\nfrom langchain.chains import RetrievalQA\nfrom config import CHROMA_DIR, API_KEY, API_BASE, EMBED_MODEL, LLM_MODEL, TOP_K\n\ndef build_qa() -> RetrievalQA:\n  emb = OpenAIEmbeddings(model=EMBED_MODEL, api_key=API_KEY or "mock", base_url=API_BASE)\n  vs = Chroma(persist_directory=str(CHROMA_DIR), embedding_function=emb)\n  retriever = vs.as_retriever(search_kwargs={"k": TOP_K})\n  llm = ChatOpenAI(model=LLM_MODEL, api_key=API_KEY or "mock", base_url=API_BASE, temperature=0.1)\n  return RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)\n\nif __name__ == "__main__":\n  qa = build_qa()\n  r = qa({"query": "年假有几天？"})\n  print(r["result"])\n',
        'enterprise_kb/api.py': '#!/usr/bin/env python3\n"""企业知识库 — FastAPI 接口"""\nfrom fastapi import FastAPI, UploadFile, File\nfrom pydantic import BaseModel\nfrom pathlib import Path\nfrom ingest import ingest\nfrom retriever import build_qa\nfrom config import UPLOAD_DIR\n\napp = FastAPI(title="Nexus Enterprise KB")\nqa_chain = None\n\nclass QueryRequest(BaseModel):\n  question: str\n\n@app.on_event("startup")\ndef startup() -> None:\n  global qa_chain\n  qa_chain = build_qa()\n\n@app.post("/upload")\nasync def upload(file: UploadFile = File(...)):\n  UPLOAD_DIR.mkdir(parents=True, exist_ok=True)\n  dest = UPLOAD_DIR / file.filename\n  dest.write_bytes(await file.read())\n  n = ingest(dest)\n  return {"status": "ok", "chunks": n}\n\n@app.post("/query")\ndef query(req: QueryRequest):\n  r = qa_chain({"query": req.question})\n  sources = [d.metadata for d in r.get("source_documents", [])]\n  return {"answer": r["result"], "sources": sources}\n\nif __name__ == "__main__":\n  import uvicorn\n  uvicorn.run(app, host="0.0.0.0", port=8000)\n',
        'enterprise_kb/ui.py': '#!/usr/bin/env python3\n"""企业知识库 — Streamlit 简易 UI（可选）"""\nimport streamlit as st\nimport requests\n\nAPI = "http://localhost:8000"\n\nst.title("Nexus 企业知识库")\nq = st.text_input("请输入问题")\nif st.button("提问") and q:\n  r = requests.post(f"{API}/query", json={"question": q}, timeout=30)\n  data = r.json()\n  st.write(data.get("answer", ""))\n  st.json(data.get("sources", []))\n',
        'enterprise_kb/README.md': '# 企业知识库项目（Day 36-37）\n\n## 模块\n- `config.py` 配置\n- `ingest.py` 文档入库\n- `retriever.py` RAG 问答\n- `api.py` FastAPI 接口\n- `ui.py` Streamlit 前端\n\n## 启动\n```bash\npython ingest.py\nuvicorn api:app --reload\nstreamlit run ui.py\n```\n',
    },
    homework_desc='部署本地 demo：上传手册 + 问答 + 显示引用来源，录屏 3 分钟。',
    homework_answer_hint='return_source_documents=True，sources 返回 metadata。',
    architecture_mermaid='flowchart LR\\n  UI --> API --> QA[RAG] --> CHROMA\\n  API --> SOURCES[引用]',
    narration='**陈工**：明天答辩看端到端 demo，引用溯源必须能点开。',
    key_concepts=['FastAPI', '文件上传', '引用溯源', '端到端集成'],
    platform_touches=['NexusAgent v0.3 里程碑交付'],
)

DAY_38 = DayPlan(
    day=38,
    title='Phase 3 答辩',
    phase='Phase 3：LangChain RAG 知识库',
    epic='NEXUS-E3',
    jira_stories=['NEXUS-381'],
    morning=['09:00 答辩规则说明', '10:00 小组演示（8min+2min Q&A）', '12:00 讲师点评'],
    afternoon=['14:00 代码走查', '16:00 RAG 常见问题复盘', '17:00 进入 Phase 4 Agent'],
    evening=['19:00 预习 ReAct 论文', '20:00 阅读 LangGraph 文档'],
    code_files={
        'demo_script.py': '#!/usr/bin/env python3\n"""Day 38: 答辩演示脚本"""\nimport subprocess\nimport sys\n\nSTEPS = [\n  ("入库", [sys.executable, "enterprise_kb/ingest.py"]),\n  ("问答", [sys.executable, "enterprise_kb/retriever.py"]),\n]\n\ndef main() -> None:\n  print("=== Nexus 企业知识库答辩 Demo ===")\n  for name, cmd in STEPS:\n    print(f"\\n>> {name}")\n    subprocess.run(cmd, check=False)\n\nif __name__ == "__main__":\n  main()\n',
        'presentation_outline.md': '# Phase 3 答辩提纲\n\n1. 项目背景与目标（1min）\n2. 架构图与模块说明（2min）\n3. 现场 Demo：上传 + 问答 + 溯源（3min）\n4. 调优与评估（Ragas/混合检索）（1min）\n5. Q&A（2min）\n',
        'review_checklist.md': '# 答辩评审清单\n\n- [ ] ingest 可批量导入\n- [ ] 问答准确率可接受\n- [ ] 引用溯源完整\n- [ ] API 可调用\n- [ ] 代码注释与结构清晰\n',
    },
    homework_desc='根据评委反馈修复 2 个 P0 问题，提交 hotfix 分支。',
    homework_answer_hint='优先修 ingest 失败和溯源缺失。',
    architecture_mermaid='flowchart LR\\n  DEMO[演示] --> QNA[Q&A] --> REVIEW[评审] --> PHASE4[Phase4]',
    narration='**林悦**：答辩不是秀 PPT，是证明你们能交付。**全班**：RAG 终于跑通了！',
    key_concepts=['技术答辩', 'Demo 演练', '代码走查', '阶段复盘'],
    platform_touches=['v0.3 里程碑评审通过'],
)

DAY_39 = DayPlan(
    day=39,
    title='ReAct 手写',
    phase='Phase 4：多 Agent 编排',
    epic='NEXUS-E4',
    jira_stories=['NEXUS-391', 'NEXUS-392'],
    morning=['09:00 ReAct 论文精读', '10:00 Thought-Action-Observation 循环', '11:00 手写 Agent 框架'],
    afternoon=['14:00 实现 search 工具', '16:00 多轮推理循环', '17:00 解析 Action 格式'],
    evening=['19:00 作业：新增 calculator 工具', '20:00 预习 LangChain Agent'],
    code_files={
        'react_agent.py': '#!/usr/bin/env python3\n"""Day 39: 手写 ReAct Agent"""\nimport re\nfrom tools import TOOLS\n\nSYSTEM = """你是助手，使用以下格式：\nThought: 思考\nAction: 工具名[参数]\nObservation: 工具返回\n... 最终 Answer: 结论\n可用工具: search, calculator\n"""\n\ndef parse_action(text: str) -> tuple[str, str] | None:\n  m = re.search(r"Action:\\s*(\\w+)\\[(.*?)\\]", text, re.DOTALL)\n  return (m.group(1), m.group(2)) if m else None\n\ndef react_loop(question: str, max_steps: int = 5) -> str:\n  history = SYSTEM + f"\\nQuestion: {question}\\n"\n  for _ in range(max_steps):\n    # 教学 mock：规则生成 Thought/Action\n    if "计算" in question or "+" in question:\n      thought = "Thought: 需要计算\\nAction: calculator[2+3]\\n"\n    else:\n      thought = "Thought: 需要搜索\\nAction: search[Nexus RAG]\\n"\n    history += thought\n    action = parse_action(thought)\n    if not action:\n      break\n    name, arg = action\n    obs = TOOLS[name](arg)\n    history += f"Observation: {obs}\\n"\n    if "Answer:" in obs:\n      return obs\n  return history + "Answer: 未能在限定步数内完成"\n\nif __name__ == "__main__":\n  print(react_loop("Nexus 用什么做 RAG？"))\n  print(react_loop("计算 2+3"))\n',
        'tools.py': '#!/usr/bin/env python3\n"""Day 39: ReAct 工具集"""\nimport ast\nimport operator\n\ndef search(query: str) -> str:\n  # 模拟搜索\n  kb = {"Nexus RAG": "Nexus 使用 LangChain + Chroma 实现 RAG。"}\n  for k, v in kb.items():\n    if k.lower() in query.lower() or query.lower() in k.lower():\n      return v\n  return "未找到相关信息"\n\ndef calculator(expr: str) -> str:\n  # 安全计算：仅允许数字与运算符\n  allowed = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}\n  def _eval(node):\n    if isinstance(node, ast.Num):\n      return node.n\n    if isinstance(node, ast.BinOp):\n      return allowed[type(node.op)](_eval(node.left), _eval(node.right))\n    raise ValueError("非法表达式")\n  try:\n    return str(_eval(ast.parse(expr, mode="eval").body))\n  except Exception as e:\n    return f"计算错误: {e}"\n\nTOOLS = {"search": search, "calculator": calculator}\n',
        'react_prompt.py': '#!/usr/bin/env python3\n"""Day 39: ReAct Prompt 模板"""\nREACT_TEMPLATE = """\nAnswer the following question using interleaving Thought, Action, Observation steps.\nQuestion: {question}\n{scratchpad}\n"""\n',
    },
    homework_desc='扩展 react_agent.py：接入真实 LLM 生成 Thought/Action（替换 mock）。',
    homework_answer_hint='llm.invoke(history) 解析返回文本中的 Action。',
    architecture_mermaid='flowchart TD\\n  Q --> THOUGHT --> ACTION --> TOOL --> OBS --> THOUGHT',
    narration='**陈工**：理解 ReAct 比调库重要，今天禁止直接用 AgentExecutor。',
    key_concepts=['ReAct', 'Thought-Action-Observation', '工具调用', '推理循环'],
    platform_touches=['Nexus Agent 引擎理论基础'],
)

DAY_40 = DayPlan(
    day=40,
    title='LangChain Agent',
    phase='Phase 4：多 Agent 编排',
    epic='NEXUS-E4',
    jira_stories=['NEXUS-401', 'NEXUS-402'],
    morning=['09:00 create_react_agent', '10:00 AgentExecutor', '11:00 Tool 装饰器'],
    afternoon=['14:00 多工具 Agent', '16:00 错误处理与 max_iterations', '17:00 对比手写 ReAct'],
    evening=['19:00 作业：3 工具 Agent', '20:00 预习 LangGraph'],
    code_files={
        'langchain_agent.py': '#!/usr/bin/env python3\n"""Day 40: LangChain ReAct Agent"""\nimport os\nfrom langchain.agents import create_react_agent, AgentExecutor\nfrom langchain_core.tools import tool\nfrom langchain_core.prompts import PromptTemplate\nfrom langchain_openai import ChatOpenAI\n\n@tool\ndef get_weather(city: str) -> str:\n  """查询城市天气"""\n  return f"{city}：晴，25°C"\n\n@tool\ndef kb_search(query: str) -> str:\n  """搜索企业知识库"""\n  return f"关于「{query}」：Nexus 支持 RAG 问答。"\n\nllm = ChatOpenAI(\n  model="deepseek-chat",\n  api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),\n  base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),\n)\ntools = [get_weather, kb_search]\nprompt = PromptTemplate.from_template("你有工具: {tools}\\n问题: {input}\\n{agent_scratchpad}")\nagent = create_react_agent(llm, tools, prompt)\nexecutor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=5)\n\nif __name__ == "__main__":\n  print(executor.invoke({"input": "北京天气怎么样？"}))\n',
        'agent_executor.py': '#!/usr/bin/env python3\n"""Day 40: AgentExecutor 配置与回调"""\nfrom langchain.agents import AgentExecutor\nfrom langchain_core.callbacks import BaseCallbackHandler\n\nclass LogHandler(BaseCallbackHandler):\n  def on_tool_start(self, serialized, input_str, **kwargs):\n    print(f"[TOOL] {serialized.get(\'name\')} input={input_str}")\n\n# 在 langchain_agent 中: AgentExecutor(..., callbacks=[LogHandler()])\n',
        'custom_tools.py': '#!/usr/bin/env python3\n"""Day 40: 自定义 Tool"""\nfrom langchain_core.tools import StructuredTool\nfrom pydantic import BaseModel, Field\n\nclass CalcInput(BaseModel):\n  expression: str = Field(description="数学表达式")\n\ndef calc(expression: str) -> str:\n  return str(eval(expression))  # 教学简化，生产需沙箱\n\ncalc_tool = StructuredTool.from_function(func=calc, name="calculator", description="计算表达式", args_schema=CalcInput)\n',
    },
    homework_desc='实现含 weather/kb/calculator 三工具的 Agent，处理工具调用失败重试。',
    homework_answer_hint='AgentExecutor handle_parsing_errors=True。',
    architecture_mermaid='flowchart LR\\n  Q --> AGENT --> TOOL1 & TOOL2 --> AGENT --> ANS',
    narration='**陈工**：生产用 LangChain Agent，但你们得知道 Executor 里发生了什么。',
    key_concepts=['create_react_agent', 'AgentExecutor', '@tool', 'StructuredTool'],
    platform_touches=['Nexus 工具注册中心原型'],
)

DAY_41 = DayPlan(
    day=41,
    title='LangGraph 入门',
    phase='Phase 4：多 Agent 编排',
    epic='NEXUS-E4',
    jira_stories=['NEXUS-411', 'NEXUS-412'],
    morning=['09:00 状态图概念', '10:00 StateGraph 基础', '11:00 节点与边'],
    afternoon=['14:00 构建两节点图', '16:00 编译与 invoke', '17:00 可视化'],
    evening=['19:00 作业：三节点流水线', '20:00 预习条件边'],
    code_files={
        'state_graph.py': '#!/usr/bin/env python3\n"""Day 41: LangGraph StateGraph 入门"""\nfrom typing import TypedDict\nfrom langgraph.graph import StateGraph, END\n\nclass AgentState(TypedDict):\n  messages: list[str]\n  step: int\n\ndef research(state: AgentState) -> AgentState:\n  state["messages"].append("检索: Nexus RAG 文档")\n  state["step"] += 1\n  return state\n\ndef write(state: AgentState) -> AgentState:\n  state["messages"].append("生成: 基于检索的回答草稿")\n  state["step"] += 1\n  return state\n\ngraph = StateGraph(AgentState)\ngraph.add_node("research", research)\ngraph.add_node("write", write)\ngraph.set_entry_point("research")\ngraph.add_edge("research", "write")\ngraph.add_edge("write", END)\napp = graph.compile()\n\nif __name__ == "__main__":\n  out = app.invoke({"messages": [], "step": 0})\n  print(out)\n',
        'simple_graph.py': '#!/usr/bin/env python3\n"""Day 41: 消息列表状态"""\nfrom langgraph.graph import MessagesState, StateGraph, END\n\ndef chatbot(state: MessagesState):\n  return {"messages": state["messages"] + [{"role": "assistant", "content": "收到"}]}\n\ng = StateGraph(MessagesState)\ng.add_node("bot", chatbot)\ng.set_entry_point("bot")\ng.add_edge("bot", END)\napp = g.compile()\n',
        'visualize_graph.py': '#!/usr/bin/env python3\n"""Day 41: 导出 Mermaid 图"""\nfrom state_graph import app\ntry:\n  print(app.get_graph().draw_mermaid())\nexcept Exception:\n  print("graph TD\\n  research --> write --> END")\n',
    },
    homework_desc='构建 research -> analyze -> write 三节点图，每节点追加 messages。',
    homework_answer_hint='add_node + add_edge 串联三个函数。',
    architecture_mermaid='stateDiagram-v2\\n  [*] --> research\\n  research --> write\\n  write --> [*]',
    narration='**陈工**：Agent 不是链，是图。LangGraph 是 Nexus v0.4 编排核心。',
    key_concepts=['StateGraph', 'TypedDict 状态', '节点与边', 'compile'],
    platform_touches=['Nexus Agent 编排引擎选型 LangGraph'],
)

DAY_42 = DayPlan(
    day=42,
    title='LangGraph 进阶',
    phase='Phase 4：多 Agent 编排',
    epic='NEXUS-E4',
    jira_stories=['NEXUS-421', 'NEXUS-422'],
    morning=['09:00 条件边 conditional_edges', '10:00 循环与终止条件', '11:00 Checkpoint 持久化'],
    afternoon=['14:00 人工审批节点', '16:00 MemorySaver', '17:00 断点续跑'],
    evening=['19:00 作业：审批流', '20:00 预习多 Agent'],
    code_files={
        'conditional_edges.py': '#!/usr/bin/env python3\n"""Day 42: 条件路由"""\nfrom typing import TypedDict, Literal\nfrom langgraph.graph import StateGraph, END\n\nclass State(TypedDict):\n  query: str\n  route: str\n  answer: str\n\ndef classify(state: State) -> State:\n  state["route"] = "kb" if "政策" in state["query"] or "年假" in state["query"] else "general"\n  return state\n\ndef kb_node(state: State) -> State:\n  state["answer"] = "知识库回答: 年假5天"\n  return state\n\ndef general_node(state: State) -> State:\n  state["answer"] = "通用回答: 请问具体需求"\n  return state\n\ndef route_fn(state: State) -> Literal["kb", "general"]:\n  return state["route"]\n\ng = StateGraph(State)\ng.add_node("classify", classify)\ng.add_node("kb", kb_node)\ng.add_node("general", general_node)\ng.set_entry_point("classify")\ng.add_conditional_edges("classify", route_fn, {"kb": "kb", "general": "general"})\ng.add_edge("kb", END)\ng.add_edge("general", END)\napp = g.compile()\n\nif __name__ == "__main__":\n  print(app.invoke({"query": "年假政策", "route": "", "answer": ""}))\n',
        'checkpointing.py': '#!/usr/bin/env python3\n"""Day 42: MemorySaver 检查点"""\nfrom langgraph.checkpoint.memory import MemorySaver\nfrom state_graph import app as base_app\n\nmemory = MemorySaver()\napp = base_app  # 教学：编译时 checkpointer=memory\n\nif __name__ == "__main__":\n  config = {"configurable": {"thread_id": "session-1"}}\n  print("Checkpoint 演示 thread_id=session-1")\n',
        'human_approval.py': '#!/usr/bin/env python3\n"""Day 42: 人工审批节点（概念）"""\nfrom typing import TypedDict\n\nclass State(TypedDict):\n  draft: str\n  approved: bool\n\ndef generate_draft(state: State) -> State:\n  state["draft"] = "待审批的邮件草稿..."\n  return state\n\ndef wait_approval(state: State) -> State:\n  # 生产环境对接审批 API；教学用 input 模拟\n  ans = input("批准此草稿? y/n: ")\n  state["approved"] = ans.lower() == "y"\n  return state\n',
    },
    homework_desc='实现 classify -> (kb|web) -> human_review -> send 流程，未批准不发送。',
    homework_answer_hint='add_conditional_edges 检查 approved 字段。',
    architecture_mermaid='flowchart TD\\n  C[classify] -->|kb| KB\\n  C -->|general| GEN\\n  KB --> APPROVE{审批}',
    narration='**林悦**：敏感操作必须人工审批。**陈工**：LangGraph 原生支持 interrupt。',
    key_concepts=['conditional_edges', 'Checkpoint', '人工审批', '循环控制'],
    platform_touches=['Nexus 人工审批工作流'],
)

DAY_43 = DayPlan(
    day=43,
    title='多 Agent 协作',
    phase='Phase 4：多 Agent 编排',
    epic='NEXUS-E4',
    jira_stories=['NEXUS-431', 'NEXUS-432'],
    morning=['09:00 Supervisor 模式', '10:00 专家 Agent 分工', '11:00 消息传递'],
    afternoon=['14:00 实现调度器', '16:00 Researcher + Writer', '17:00 结果汇总'],
    evening=['19:00 作业：三 Agent 协作', '20:00 预习 MCP'],
    code_files={
        'multi_agent.py': '#!/usr/bin/env python3\n"""Day 43: 多 Agent 消息传递"""\nfrom dataclasses import dataclass, field\n\n@dataclass\nclass Agent:\n  name: str\n  role: str\n\n  def run(self, task: str, context: str = "") -> str:\n    return f"[{self.name}/{self.role}] 处理: {task} | 上下文: {context[:50]}"\n\n@dataclass\nclass Team:\n  agents: list[Agent] = field(default_factory=list)\n\n  def delegate(self, task: str) -> str:\n    results = []\n    ctx = ""\n    for a in self.agents:\n      out = a.run(task, ctx)\n      results.append(out)\n      ctx += out + "\\n"\n    return "\\n".join(results)\n\nif __name__ == "__main__":\n  team = Team([Agent("researcher", "检索"), Agent("writer", "写作")])\n  print(team.delegate("写一份 RAG 技术简报"))\n',
        'supervisor.py': '#!/usr/bin/env python3\n"""Day 43: Supervisor 调度"""\nfrom multi_agent import Agent\n\nclass Supervisor:\n  def __init__(self, workers: dict[str, Agent]):\n    self.workers = workers\n\n  def route(self, task: str) -> str:\n    if "搜索" in task or "检索" in task:\n      return self.workers["researcher"].run(task)\n    if "写" in task or "报告" in task:\n      return self.workers["writer"].run(task)\n    return self.workers["researcher"].run(task)\n\nif __name__ == "__main__":\n  sup = Supervisor({\n    "researcher": Agent("R", "检索"),\n    "writer": Agent("W", "写作"),\n  })\n  print(sup.route("写项目周报"))\n',
        'langgraph_supervisor.py': '#!/usr/bin/env python3\n"""Day 43: LangGraph Supervisor 骨架"""\n# 生产使用 langgraph-supervisor 或自定义 StateGraph\n# 状态包含: messages, next_agent, final_answer\nSUPERVISOR_NOTE = "Supervisor 节点决定 next_agent in [researcher, writer, END]"\nprint(SUPERVISOR_NOTE)\n',
    },
    homework_desc='用 LangGraph 实现 Supervisor + 2 Worker，Supervisor 决定下一个节点。',
    homework_answer_hint='State 含 next 字段，conditional_edges 路由到 worker 或 END。',
    architecture_mermaid='flowchart TD\\n  SUP[Supervisor] --> R[Researcher]\\n  SUP --> W[Writer]\\n  R --> SUP\\n  W --> SUP',
    narration='**陈工**：单 Agent 搞不定复杂办公流，Supervisor 是 Nexus v0.4 架构。',
    key_concepts=['Supervisor', '多 Agent 分工', '消息传递', '任务路由'],
    platform_touches=['Nexus 多 Agent 协作架构'],
)

DAY_44 = DayPlan(
    day=44,
    title='MCP 协议',
    phase='Phase 4：多 Agent 编排',
    epic='NEXUS-E4',
    jira_stories=['NEXUS-441', 'NEXUS-442'],
    morning=['09:00 MCP 架构：Host/Client/Server', '10:00 Tools/Resources 暴露', '11:00 stdio 传输'],
    afternoon=['14:00 实现 MCP Server', '16:00 Client 调用工具', '17:00 与 Agent 集成'],
    evening=['19:00 作业：暴露 kb_search 工具', '20:00 预习 Dify'],
    code_files={
        'mcp_server.py': '#!/usr/bin/env python3\n"""Day 44: 简易 MCP Server（教学 mock）"""\nimport json\nfrom typing import Any\n\nTOOLS = {\n  "kb_search": {"description": "搜索知识库", "params": {"query": "string"}},\n  "get_time": {"description": "获取当前时间", "params": {}},\n}\n\ndef handle_request(req: dict[str, Any]) -> dict[str, Any]:\n  method = req.get("method")\n  if method == "tools/list":\n    return {"tools": [{"name": k, **v} for k, v in TOOLS.items()]}\n  if method == "tools/call":\n    name = req["params"]["name"]\n    if name == "kb_search":\n      return {"content": f"检索结果: {req[\'params\'].get(\'query\')}"}\n    if name == "get_time":\n      import datetime\n      return {"content": datetime.datetime.now().isoformat()}\n  return {"error": "unknown method"}\n\nif __name__ == "__main__":\n  sample = {"method": "tools/call", "params": {"name": "kb_search", "query": "年假"}}\n  print(json.dumps(handle_request(sample), ensure_ascii=False))\n',
        'mcp_client.py': '#!/usr/bin/env python3\n"""Day 44: MCP Client 调用 Server"""\nimport json\nimport subprocess\n\nclass MCPClient:\n  def __init__(self, server_cmd: list[str]):\n    self.proc = subprocess.Popen(server_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)\n\n  def call(self, method: str, params: dict | None = None) -> dict:\n    req = {"method": method, "params": params or {}}\n    self.proc.stdin.write(json.dumps(req) + "\\n")\n    self.proc.stdin.flush()\n    line = self.proc.stdout.readline()\n    return json.loads(line) if line else {}\n\n# 教学：直接 import server 演示\nfrom mcp_server import handle_request\n\nif __name__ == "__main__":\n  print(handle_request({"method": "tools/list"}))\n',
        'agent_mcp_integration.py': '#!/usr/bin/env python3\n"""Day 44: Agent 通过 MCP 调用工具"""\nfrom mcp_server import handle_request\n\ndef mcp_tool(name: str, **kwargs) -> str:\n  r = handle_request({"method": "tools/call", "params": {"name": name, **kwargs}})\n  return r.get("content", str(r))\n\nif __name__ == "__main__":\n  print(mcp_tool("kb_search", query="报销流程"))\n',
    },
    homework_desc='用官方 mcp SDK 实现 stdio Server，暴露 kb_search 与 calendar 工具。',
    homework_answer_hint='pip install mcp，参考官方 quickstart。',
    architecture_mermaid='flowchart LR\\n  AGENT --> CLIENT[MCP Client] --> SERVER[MCP Server] --> TOOLS',
    narration='**陈工**：MCP 是工具标准化的未来，Nexus 工具中心将支持 MCP 插件。',
    key_concepts=['MCP 协议', 'Tool 暴露', 'stdio 传输', 'Agent 集成'],
    platform_touches=['Nexus 工具注册中心 MCP 支持'],
)

DAY_45 = DayPlan(
    day=45,
    title='周测与 Dify',
    phase='Phase 4：多 Agent 编排',
    epic='NEXUS-E4',
    jira_stories=['NEXUS-451', 'NEXUS-452'],
    morning=['09:00 周测讲评', '10:00 Dify 平台介绍', '11:00 工作流 vs Agent'],
    afternoon=['14:00 Dify API 对接', '16:00 导入 Nexus 知识库', '17:00 对比自研 Agent'],
    evening=['19:00 整理选型报告', '20:00 预习工程化'],
    code_files={
        'dify_integration.py': '#!/usr/bin/env python3\n"""Day 45: Dify API 对接"""\nimport os\nimport json\nimport urllib.request\n\nDIFY_API = os.getenv("DIFY_API_BASE", "https://api.dify.ai/v1")\nDIFY_KEY = os.getenv("DIFY_API_KEY", "")\n\ndef chat(message: str, user: str = "nexus-user") -> str:\n  if not DIFY_KEY:\n    return f"[MOCK Dify] 回复: {message[:50]}..."\n  payload = {"inputs": {}, "query": message, "user": user, "response_mode": "blocking"}\n  req = urllib.request.Request(\n    f"{DIFY_API}/chat-messages",\n    data=json.dumps(payload).encode(),\n    headers={"Authorization": f"Bearer {DIFY_KEY}", "Content-Type": "application/json"},\n    method="POST",\n  )\n  with urllib.request.urlopen(req, timeout=60) as resp:\n    return json.loads(resp.read())["answer"]\n\nif __name__ == "__main__":\n  print(chat("Nexus 平台有哪些功能？"))\n',
        'workflow_api.py': '#!/usr/bin/env python3\n"""Day 45: Dify 工作流 API"""\nimport os\n\ndef run_workflow(inputs: dict) -> dict:\n  # 教学占位：生产调用 Dify workflow run API\n  return {"outputs": {"summary": f"工作流处理完成: {inputs}"}}\n\nif __name__ == "__main__":\n  print(run_workflow({"doc": "季度报告"}))\n',
        'dify_vs_custom.md': '# Dify vs 自研 Agent\n\n| 维度 | Dify | 自研 LangGraph |\n|------|------|----------------|\n| 上线速度 | 快 | 慢 |\n| 定制深度 | 中 | 高 |\n| 多租户 | 内置 | 需开发 |\n| Nexus 选型 | 运营配置 | 核心引擎 |\n',
    },
    homework_desc='在 Dify 创建 Agent 应用，用 dify_integration.py 完成 5 轮对话测试。',
    homework_answer_hint='配置 DIFY_API_KEY 环境变量。',
    architecture_mermaid='flowchart LR\\n  NEXUS --> DIFY_API --> KB[(知识库)]\\n  DIFY_API --> WORKFLOW',
    narration='**林悦**：运营用 Dify 配 FAQ，研发用 LangGraph 做深度编排，不冲突。',
    key_concepts=['Dify 平台', '工作流 API', '低代码 vs 代码', '选型'],
    platform_touches=['Nexus 运营配置层对接 Dify'],
)

DAY_46 = DayPlan(
    day=46,
    title='Agent 工程化',
    phase='Phase 4：多 Agent 编排',
    epic='NEXUS-E4',
    jira_stories=['NEXUS-461', 'NEXUS-462'],
    morning=['09:00 日志与可观测性', '10:00 配置管理', '11:00 错误重试与超时'],
    afternoon=['14:00 FastAPI Agent 服务', '16:00 结构化日志', '17:00 健康检查'],
    evening=['19:00 作业：添加 metrics', '20:00 预习 Text2SQL'],
    code_files={
        'agent_service.py': '#!/usr/bin/env python3\n"""Day 46: Agent FastAPI 服务"""\nfrom fastapi import FastAPI\nfrom pydantic import BaseModel\nimport logging\n\nlogging.basicConfig(level=logging.INFO)\nlogger = logging.getLogger("nexus.agent")\n\napp = FastAPI(title="Nexus Agent Service")\n\nclass ChatRequest(BaseModel):\n  message: str\n  session_id: str = "default"\n\n@app.get("/health")\ndef health():\n  return {"status": "ok"}\n\n@app.post("/chat")\ndef chat(req: ChatRequest):\n  logger.info("chat session=%s msg=%s", req.session_id, req.message[:80])\n  # 接入 LangGraph app\n  answer = f"Agent 回复: {req.message}"\n  return {"answer": answer, "session_id": req.session_id}\n\nif __name__ == "__main__":\n  import uvicorn\n  uvicorn.run(app, host="0.0.0.0", port=8001)\n',
        'logging_config.py': '#!/usr/bin/env python3\n"""Day 46: 结构化日志"""\nimport json\nimport logging\nfrom datetime import datetime\n\nclass JsonFormatter(logging.Formatter):\n  def format(self, record: logging.LogRecord) -> str:\n    return json.dumps({\n      "ts": datetime.utcnow().isoformat(),\n      "level": record.levelname,\n      "msg": record.getMessage(),\n      "module": record.module,\n    }, ensure_ascii=False)\n\ndef setup_logging() -> None:\n  h = logging.StreamHandler()\n  h.setFormatter(JsonFormatter())\n  logging.getLogger().handlers = [h]\n  logging.getLogger().setLevel(logging.INFO)\n',
        'retry_utils.py': '#!/usr/bin/env python3\n"""Day 46: 重试装饰器"""\nimport time\nfrom functools import wraps\n\ndef retry(max_attempts: int = 3, delay: float = 1.0):\n  def deco(fn):\n    @wraps(fn)\n    def wrapper(*args, **kwargs):\n      last_err = None\n      for i in range(max_attempts):\n        try:\n          return fn(*args, **kwargs)\n        except Exception as e:\n          last_err = e\n          time.sleep(delay * (i + 1))\n      raise last_err\n    return wrapper\n  return deco\n\n@retry(max_attempts=3)\ndef flaky_llm_call(prompt: str) -> str:\n  import random\n  if random.random() < 0.5:\n    raise ConnectionError("timeout")\n  return "ok"\n',
    },
    homework_desc='为 agent_service 添加 /metrics 端点，统计请求数与平均延迟。',
    homework_answer_hint='用全局 counter 和 deque 记录最近 N 次耗时。',
    architecture_mermaid='flowchart TD\\n  API --> AGENT --> LOG[结构化日志]\\n  API --> METRICS[指标]',
    narration='**运维老周**：没有日志和 health check 不准上生产。**陈工**：今天把 Agent 当微服务做。',
    key_concepts=['FastAPI 服务化', '结构化日志', '重试', '健康检查'],
    platform_touches=['Nexus Agent 微服务化'],
)

DAY_47 = DayPlan(
    day=47,
    title='Text2SQL',
    phase='Phase 4：多 Agent 编排',
    epic='NEXUS-E4',
    jira_stories=['NEXUS-471', 'NEXUS-472'],
    morning=['09:00 Text2SQL 场景', '10:00 Schema 注入', '11:00 SQL 安全校验'],
    afternoon=['14:00 实现 schema 工具', '16:00 生成并执行 SQL', '17:00 结果解释'],
    evening=['19:00 作业：3 表 JOIN', '20:00 预习毕业项目'],
    code_files={
        'text2sql.py': '#!/usr/bin/env python3\n"""Day 47: Text2SQL Agent"""\nimport os\nimport sqlite3\nfrom langchain_openai import ChatOpenAI\nfrom langchain_core.prompts import ChatPromptTemplate\n\nSCHEMA = """\nCREATE TABLE employees (id INT, name TEXT, dept TEXT, salary INT);\nCREATE TABLE orders (id INT, emp_id INT, amount REAL, created_at TEXT);\n"""\n\nprompt = ChatPromptTemplate.from_template(\n  "根据 Schema 将问题转为 SQLite SQL，只输出 SQL。\\nSchema:\\n{schema}\\n问题:{question}"\n)\nllm = ChatOpenAI(\n  model="deepseek-chat",\n  api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),\n  base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),\n)\n\ndef generate_sql(question: str) -> str:\n  r = (prompt | llm).invoke({"schema": SCHEMA, "question": question})\n  return r.content.strip().strip("`").replace("sql\\n", "")\n\ndef run_sql(sql: str, db: str = ":memory:") -> list:\n  # 安全：仅允许 SELECT\n  if not sql.strip().upper().startswith("SELECT"):\n    raise ValueError("仅允许 SELECT 查询")\n  conn = sqlite3.connect(db)\n  cur = conn.execute(sql)\n  rows = cur.fetchall()\n  conn.close()\n  return rows\n\nif __name__ == "__main__":\n  q = "查询销售部员工数量"\n  sql = generate_sql(q) if os.getenv("DEEPSEEK_API_KEY") else "SELECT COUNT(*) FROM employees WHERE dept=\'销售\'"\n  print("SQL:", sql)\n',
        'schema_tools.py': '#!/usr/bin/env python3\n"""Day 47: Schema 工具与示例数据"""\nimport sqlite3\n\ndef init_demo_db(path: str = "data/demo.db") -> None:\n  conn = sqlite3.connect(path)\n  conn.executescript("""\n    CREATE TABLE IF NOT EXISTS employees (id INT, name TEXT, dept TEXT, salary INT);\n    INSERT OR IGNORE INTO employees VALUES (1,\'张三\',\'销售\',8000),(2,\'李四\',\'研发\',12000);\n    CREATE TABLE IF NOT EXISTS orders (id INT, emp_id INT, amount REAL);\n    INSERT OR IGNORE INTO orders VALUES (1,1,5000.0),(2,1,3000.0);\n  """)\n  conn.commit()\n  conn.close()\n\nif __name__ == "__main__":\n  init_demo_db()\n  print("demo.db 已初始化")\n',
        'sql_guard.py': '#!/usr/bin/env python3\n"""Day 47: SQL 安全守卫"""\nFORBIDDEN = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", ";--"]\n\ndef is_safe_sql(sql: str) -> bool:\n  upper = sql.upper()\n  if not upper.strip().startswith("SELECT"):\n    return False\n  return not any(kw in upper for kw in FORBIDDEN)\n\nif __name__ == "__main__":\n  print(is_safe_sql("SELECT * FROM employees"))\n  print(is_safe_sql("DROP TABLE employees"))\n',
    },
    homework_desc='扩展 text2sql.py：先 init_demo_db，对自然语言问题生成 SQL、校验、执行并自然语言解释结果。',
    homework_answer_hint='sql_guard.is_safe_sql 通过后 run_sql，再用 LLM 解释 rows。',
    architecture_mermaid='flowchart LR\\n  Q --> LLM --> SQL --> GUARD --> DB --> EXPLAIN[结果解释]',
    narration='**林悦**：销售要自助查数据，Text2SQL 是办公助手核心能力。',
    key_concepts=['Text2SQL', 'Schema 注入', 'SQL 安全', '结果解释'],
    platform_touches=['Nexus 数据分析 Agent'],
)

DAY_48 = DayPlan(
    day=48,
    title='多 Agent 办公助手（上）',
    phase='Phase 4：多 Agent 编排',
    epic='NEXUS-E4',
    jira_stories=['NEXUS-481', 'NEXUS-482', 'NEXUS-483'],
    morning=['09:00 项目需求：办公自动化', '10:00 Agent 分工设计', '11:00 项目脚手架'],
    afternoon=['14:00 实现 Researcher/Writer', '16:00 Scheduler Agent', '17:00 单元测试'],
    evening=['19:00 开始 LangGraph 工作流', '20:00 联调'],
    code_files={
        'office_assistant/config.py': '#!/usr/bin/env python3\n"""多 Agent 办公助手 — 配置"""\nimport os\nfrom pathlib import Path\n\nDATA_DIR = Path("data")\nLLM_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")\nAPI_KEY = os.getenv("DEEPSEEK_API_KEY", "")\nAPI_BASE = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")\nMAX_ITERATIONS = 8\n',
        'office_assistant/agents/researcher.py': '#!/usr/bin/env python3\n"""Researcher Agent — 检索与信息收集"""\nfrom dataclasses import dataclass\n\n@dataclass\nclass ResearchResult:\n  query: str\n  findings: list[str]\n\nclass ResearcherAgent:\n  def run(self, task: str) -> ResearchResult:\n    # 模拟检索企业知识库与网络\n    findings = [\n      f"内部文档: 关于「{task}」的政策摘要",\n      f"近期工单: 3 条相关记录",\n    ]\n    return ResearchResult(query=task, findings=findings)\n',
        'office_assistant/agents/writer.py': '#!/usr/bin/env python3\n"""Writer Agent — 文档与邮件撰写"""\nfrom dataclasses import dataclass\n\n@dataclass\nclass Draft:\n  title: str\n  body: str\n\nclass WriterAgent:\n  def run(self, task: str, context: str) -> Draft:\n    body = f"根据以下资料撰写:\\n{context}\\n\\n---\\n{task} 的回复草稿..."\n    return Draft(title=task[:30], body=body)\n',
        'office_assistant/agents/scheduler.py': '#!/usr/bin/env python3\n"""Scheduler Agent — 会议与日程安排"""\nfrom dataclasses import dataclass\nfrom datetime import datetime, timedelta\n\n@dataclass\nclass Meeting:\n  title: str\n  start: datetime\n  duration_min: int\n\nclass SchedulerAgent:\n  def propose(self, title: str) -> Meeting:\n    start = datetime.now() + timedelta(days=1)\n    return Meeting(title=title, start=start, duration_min=60)\n\n  def format_invite(self, m: Meeting) -> str:\n    return f"会议邀请: {m.title} @ {m.start.isoformat()} ({m.duration_min}min)"\n',
        'office_assistant/graph/workflow.py': '#!/usr/bin/env python3\n"""LangGraph 工作流 — Supervisor 调度多 Agent"""\nfrom typing import TypedDict, Literal\nfrom langgraph.graph import StateGraph, END\nimport sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path(__file__).resolve().parent.parent))\nfrom agents.researcher import ResearcherAgent\nfrom agents.writer import WriterAgent\nfrom agents.scheduler import SchedulerAgent\n\nclass OfficeState(TypedDict):\n  task: str\n  route: str\n  context: str\n  output: str\n\nresearcher = ResearcherAgent()\nwriter = WriterAgent()\nscheduler = SchedulerAgent()\n\ndef supervisor(state: OfficeState) -> OfficeState:\n  t = state["task"]\n  if "会议" in t or "日程" in t:\n    state["route"] = "scheduler"\n  elif "写" in t or "邮件" in t or "报告" in t:\n    state["route"] = "writer"\n  else:\n    state["route"] = "researcher"\n  return state\n\ndef run_researcher(state: OfficeState) -> OfficeState:\n  r = researcher.run(state["task"])\n  state["context"] = "\\n".join(r.findings)\n  state["output"] = state["context"]\n  return state\n\ndef run_writer(state: OfficeState) -> OfficeState:\n  if not state.get("context"):\n    run_researcher(state)\n  d = writer.run(state["task"], state["context"])\n  state["output"] = d.body\n  return state\n\ndef run_scheduler(state: OfficeState) -> OfficeState:\n  m = scheduler.propose(state["task"])\n  state["output"] = scheduler.format_invite(m)\n  return state\n\ndef route(state: OfficeState) -> Literal["researcher", "writer", "scheduler"]:\n  return state["route"]\n\ndef build_graph():\n  g = StateGraph(OfficeState)\n  g.add_node("supervisor", supervisor)\n  g.add_node("researcher", run_researcher)\n  g.add_node("writer", run_writer)\n  g.add_node("scheduler", run_scheduler)\n  g.set_entry_point("supervisor")\n  g.add_conditional_edges("supervisor", route, {\n    "researcher": "researcher", "writer": "writer", "scheduler": "scheduler"\n  })\n  g.add_edge("researcher", END)\n  g.add_edge("writer", END)\n  g.add_edge("scheduler", END)\n  return g.compile()\n\nif __name__ == "__main__":\n  app = build_graph()\n  for task in ["查询年假政策", "写一封项目周报邮件", "安排下周评审会议"]:\n    print(task, "->", app.invoke({"task": task, "route": "", "context": "", "output": ""})["output"][:80])\n',
    },
    homework_desc='完成三个 Agent 类，各写 2 个单元测试。',
    homework_answer_hint='pytest 测试 ResearcherAgent.run 返回 findings 非空。',
    architecture_mermaid='flowchart TD\\n  TASK --> SUP[Supervisor]\\n  SUP --> R & W & S',
    narration='**林悦**：Phase 4 毕业项目 — 办公助手要能写邮件、查政策、排会议。',
    key_concepts=['多 Agent 架构', '角色分工', '项目脚手架', '单元测试'],
    platform_touches=['Nexus v0.4 办公自动化 MVP'],
)

DAY_49 = DayPlan(
    day=49,
    title='多 Agent 办公助手（下）',
    phase='Phase 4：多 Agent 编排',
    epic='NEXUS-E4',
    jira_stories=['NEXUS-491', 'NEXUS-492'],
    morning=['09:00 完成 LangGraph 工作流', '10:30 FastAPI 接口', '11:00 Text2SQL 集成'],
    afternoon=['14:00 端到端联调', '16:00 MCP 工具接入', '17:00 性能与日志'],
    evening=['19:00 准备答辩', '20:00 彩排'],
    code_files={
        'office_assistant/config.py': '#!/usr/bin/env python3\n"""多 Agent 办公助手 — 配置"""\nimport os\nfrom pathlib import Path\n\nDATA_DIR = Path("data")\nLLM_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")\nAPI_KEY = os.getenv("DEEPSEEK_API_KEY", "")\nAPI_BASE = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")\nMAX_ITERATIONS = 8\n',
        'office_assistant/agents/researcher.py': '#!/usr/bin/env python3\n"""Researcher Agent — 检索与信息收集"""\nfrom dataclasses import dataclass\n\n@dataclass\nclass ResearchResult:\n  query: str\n  findings: list[str]\n\nclass ResearcherAgent:\n  def run(self, task: str) -> ResearchResult:\n    # 模拟检索企业知识库与网络\n    findings = [\n      f"内部文档: 关于「{task}」的政策摘要",\n      f"近期工单: 3 条相关记录",\n    ]\n    return ResearchResult(query=task, findings=findings)\n',
        'office_assistant/agents/writer.py': '#!/usr/bin/env python3\n"""Writer Agent — 文档与邮件撰写"""\nfrom dataclasses import dataclass\n\n@dataclass\nclass Draft:\n  title: str\n  body: str\n\nclass WriterAgent:\n  def run(self, task: str, context: str) -> Draft:\n    body = f"根据以下资料撰写:\\n{context}\\n\\n---\\n{task} 的回复草稿..."\n    return Draft(title=task[:30], body=body)\n',
        'office_assistant/agents/scheduler.py': '#!/usr/bin/env python3\n"""Scheduler Agent — 会议与日程安排"""\nfrom dataclasses import dataclass\nfrom datetime import datetime, timedelta\n\n@dataclass\nclass Meeting:\n  title: str\n  start: datetime\n  duration_min: int\n\nclass SchedulerAgent:\n  def propose(self, title: str) -> Meeting:\n    start = datetime.now() + timedelta(days=1)\n    return Meeting(title=title, start=start, duration_min=60)\n\n  def format_invite(self, m: Meeting) -> str:\n    return f"会议邀请: {m.title} @ {m.start.isoformat()} ({m.duration_min}min)"\n',
        'office_assistant/graph/workflow.py': '#!/usr/bin/env python3\n"""LangGraph 工作流 — Supervisor 调度多 Agent"""\nfrom typing import TypedDict, Literal\nfrom langgraph.graph import StateGraph, END\nimport sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path(__file__).resolve().parent.parent))\nfrom agents.researcher import ResearcherAgent\nfrom agents.writer import WriterAgent\nfrom agents.scheduler import SchedulerAgent\n\nclass OfficeState(TypedDict):\n  task: str\n  route: str\n  context: str\n  output: str\n\nresearcher = ResearcherAgent()\nwriter = WriterAgent()\nscheduler = SchedulerAgent()\n\ndef supervisor(state: OfficeState) -> OfficeState:\n  t = state["task"]\n  if "会议" in t or "日程" in t:\n    state["route"] = "scheduler"\n  elif "写" in t or "邮件" in t or "报告" in t:\n    state["route"] = "writer"\n  else:\n    state["route"] = "researcher"\n  return state\n\ndef run_researcher(state: OfficeState) -> OfficeState:\n  r = researcher.run(state["task"])\n  state["context"] = "\\n".join(r.findings)\n  state["output"] = state["context"]\n  return state\n\ndef run_writer(state: OfficeState) -> OfficeState:\n  if not state.get("context"):\n    run_researcher(state)\n  d = writer.run(state["task"], state["context"])\n  state["output"] = d.body\n  return state\n\ndef run_scheduler(state: OfficeState) -> OfficeState:\n  m = scheduler.propose(state["task"])\n  state["output"] = scheduler.format_invite(m)\n  return state\n\ndef route(state: OfficeState) -> Literal["researcher", "writer", "scheduler"]:\n  return state["route"]\n\ndef build_graph():\n  g = StateGraph(OfficeState)\n  g.add_node("supervisor", supervisor)\n  g.add_node("researcher", run_researcher)\n  g.add_node("writer", run_writer)\n  g.add_node("scheduler", run_scheduler)\n  g.set_entry_point("supervisor")\n  g.add_conditional_edges("supervisor", route, {\n    "researcher": "researcher", "writer": "writer", "scheduler": "scheduler"\n  })\n  g.add_edge("researcher", END)\n  g.add_edge("writer", END)\n  g.add_edge("scheduler", END)\n  return g.compile()\n\nif __name__ == "__main__":\n  app = build_graph()\n  for task in ["查询年假政策", "写一封项目周报邮件", "安排下周评审会议"]:\n    print(task, "->", app.invoke({"task": task, "route": "", "context": "", "output": ""})["output"][:80])\n',
        'office_assistant/main.py': '#!/usr/bin/env python3\n"""多 Agent 办公助手 — CLI 入口"""\nimport argparse\nfrom graph.workflow import build_graph\n\ndef main() -> None:\n  parser = argparse.ArgumentParser(description="Nexus 办公助手")\n  parser.add_argument("task", help="办公任务描述")\n  args = parser.parse_args()\n  app = build_graph()\n  result = app.invoke({"task": args.task, "route": "", "context": "", "output": ""})\n  print("=== 办公助手输出 ===")\n  print(result["output"])\n\nif __name__ == "__main__":\n  main()\n',
        'office_assistant/api.py': '#!/usr/bin/env python3\n"""办公助手 FastAPI 服务"""\nfrom fastapi import FastAPI\nfrom pydantic import BaseModel\nfrom graph.workflow import build_graph\n\napp = FastAPI(title="Nexus Office Assistant")\nworkflow = build_graph()\n\nclass TaskRequest(BaseModel):\n  task: str\n\n@app.post("/assist")\ndef assist(req: TaskRequest):\n  r = workflow.invoke({"task": req.task, "route": "", "context": "", "output": ""})\n  return {"output": r["output"], "route": r["route"]}\n',
        'office_assistant/README.md': '# 多 Agent 办公助手（Day 48-49）\n\n## Agent 分工\n- **Researcher**: 知识检索\n- **Writer**: 文档撰写\n- **Scheduler**: 会议安排\n\n## 运行\n```bash\npython main.py "写项目周报邮件"\nuvicorn api:app --app-dir office_assistant --reload\n```\n',
    },
    homework_desc='完成端到端 demo：CLI + API + 三种任务类型，录屏 5 分钟。',
    homework_answer_hint='main.py 与 api.py 均可调用 build_graph()。',
    architecture_mermaid='flowchart LR\\n  CLI --> GRAPH --> AGENTS\\n  API --> GRAPH\\n  GRAPH --> MCP[MCP工具]',
    narration='**陈工**：明天答辩，Supervisor 路由必须演示清楚，日志要有 session_id。',
    key_concepts=['LangGraph 工作流', 'FastAPI', '端到端集成', 'MCP 接入'],
    platform_touches=['Nexus v0.4 里程碑交付'],
)

DAY_50 = DayPlan(
    day=50,
    title='Phase 4 答辩',
    phase='Phase 4：多 Agent 编排',
    epic='NEXUS-E4',
    jira_stories=['NEXUS-501'],
    morning=['09:00 答辩规则', '10:00 小组演示（10min+3min Q&A）', '12:00 点评'],
    afternoon=['14:00 Agent 架构复盘', '16:00 Phase 5 微调预告', '17:00 庆祝与合影'],
    evening=['19:00 预习 LoRA 论文', '20:00 阅读部署文档'],
    code_files={
        'final_demo.py': '#!/usr/bin/env python3\n"""Day 50: Phase 4 答辩总演示"""\nimport subprocess\nimport sys\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parent / "office_assistant"\n\nDEMOS = [\n  ("办公助手-写邮件", [sys.executable, str(ROOT / "main.py"), "写项目周报邮件"]),\n  ("办公助手-排会议", [sys.executable, str(ROOT / "main.py"), "安排下周评审会议"]),\n  ("Text2SQL", [sys.executable, "text2sql.py"]),\n]\n\ndef main() -> None:\n  print("=== Nexus Phase 4 毕业答辩 Demo ===")\n  for name, cmd in DEMOS:\n    print(f"\\n>> {name}")\n    subprocess.run(cmd, cwd=Path(__file__).parent, check=False)\n\nif __name__ == "__main__":\n  main()\n',
        'presentation_checklist.md': '# Phase 4 答辩清单\n\n- [ ] Supervisor 路由演示（3 种任务）\n- [ ] ReAct / LangGraph 架构讲解\n- [ ] MCP 或 Dify 集成说明\n- [ ] Text2SQL 安全守卫演示\n- [ ] 工程化：日志 / health / API\n- [ ] 代码结构与中文注释\n',
        'phase4_retrospective.md': '# Phase 4 复盘\n\n## 收获\n- 手写 ReAct 理解 Agent 本质\n- LangGraph 状态图编排\n- 多 Agent + MCP 工程实践\n\n## 下一步\n- Phase 5: LoRA 微调与 Docker 部署\n',
    },
    homework_desc='根据答辩反馈修复 P0，合并到 develop 并打 tag v0.4-milestone。',
    homework_answer_hint='git tag v0.4-milestone && git push origin v0.4-milestone',
    architecture_mermaid='flowchart LR\\n  DEMO --> REVIEW --> V04[v0.4] --> P5[Phase5]',
    narration='**全班**：从 RAG 到 Agent，五十天你们已经能交付企业级原型。**陈工**：微调与部署，下半场见。',
    key_concepts=['技术答辩', '架构复盘', '里程碑发布', 'Phase 5 预告'],
    platform_touches=['v0.4 里程碑评审通过'],
)

DAYS_25_TO_50: list[DayPlan] = [
    DAY_25,
    DAY_26,
    DAY_27,
    DAY_28,
    DAY_29,
    DAY_30,
    DAY_31,
    DAY_32,
    DAY_33,
    DAY_34,
    DAY_35,
    DAY_36,
    DAY_37,
    DAY_38,
    DAY_39,
    DAY_40,
    DAY_41,
    DAY_42,
    DAY_43,
    DAY_44,
    DAY_45,
    DAY_46,
    DAY_47,
    DAY_48,
    DAY_49,
    DAY_50,
]
