# 企业知识库项目（Day 36-37）

## 模块
- `config.py` 配置
- `ingest.py` 文档入库
- `retriever.py` RAG 问答
- `api.py` FastAPI 接口
- `ui.py` Streamlit 前端

## 启动
```bash
python ingest.py
uvicorn api:app --reload
streamlit run ui.py
```
