# rag-demo

个人 RAG 应用，基于《高性价比人生指南》654 条建议。

## 做了什么

一个完整的 RAG 系统：

1. 读取 654 条建议文档
2. 用 embedding 模型把文本转向量
3. 存进 PostgreSQL + pgvector
4. 用户提问时，搜索最相似的 3 条
5. 把条目 + 问题发给大模型，生成回答
6. 提供 Streamlit Web 界面

## 我负责

全部（从需求拆解到编码、测试、部署）

## 用了哪些工具

- Python 3.11
- Ollama（本地跑模型）
- bge-m3（embedding，1024 维）
- qwen2.5:3b（对话模型）
- PostgreSQL + pgvector（向量存储）
- Streamlit（Web 界面）
- LangChain
- AI 辅助开发

## 收获

- 理解了 RAG 完整流程：读文档 → 切块 → 转向量 → 存向量 → 搜索 → 生成回答
- 踩过 all-minilm 中文支持差的坑，换成 bge-m3 后搜索准确
- 踩过 GPU 驱动不兼容的坑（0xc0000005），更新驱动到 582.78 后解决
- 从 CPU 到 GPU，生成速度提升 10 倍
- 学会了用向量距离判断搜索结果的相关性

## 文件说明

| 文件 | 作用 |
|---|---|
| 01_load_docs.py | 读文档、切块 |
| 02_embed_and_store.py | 转向量、存 pgvector |
| 03_search.py | 搜索相似 |
| 04_rag.py | 命令行版 RAG |
| 05_app.py | Streamlit Web 界面 |

## 本地运行

### 1. 启动数据库

```bash
cd /e/IdeaProjects/InterestingBooks
docker compose up -d