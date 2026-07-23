#!/usr/bin/env python3
"""企业知识库 — Streamlit 简易 UI（可选）"""
import streamlit as st
import requests

API = "http://localhost:8000"

st.title("Nexus 企业知识库")
q = st.text_input("请输入问题")
if st.button("提问") and q:
  r = requests.post(f"{API}/query", json={"question": q}, timeout=30)
  data = r.json()
  st.write(data.get("answer", ""))
  st.json(data.get("sources", []))
