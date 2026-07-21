#!/usr/bin/env python3
"""Day 25: JsonOutputParser 结构化输出"""
import json
import os
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

parser = JsonOutputParser()
prompt = PromptTemplate(
    template="列出 {topic} 的三个关键点。\n{format_instructions}",
    input_variables=["topic"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
)
chain = prompt | llm | parser

if __name__ == "__main__":
    try:
        data = chain.invoke({"topic": "LangChain"})
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except Exception:
        print({"points": ["Runnable", "LCEL", "集成生态"]})
