import streamlit as st
import psycopg2
import ollama

st.set_page_config(page_title="个人 RAG 助手", page_icon="📚")
st.title("📚 个人 RAG 助手")
st.caption("基于《高性价比人生指南》654 条建议")

@st.cache_resource
def get_conn():
    return psycopg2.connect(
        host="localhost",
        port=5332,
        dbname="interestingbooks",
        user="postgres",
        password="password"
    )

conn = get_conn()
cur = conn.cursor()

question = st.text_input("输入你的问题：", placeholder="比如：怎么戒烟？")

if st.button("提问") and question:
    with st.spinner("检索中..."):
        response = ollama.embeddings(model="bge-m3", prompt=question)
        q_vector = response["embedding"]

        cur.execute(
            """
            SELECT title, content, embedding <-> %s::vector AS distance
            FROM document_chunk
            ORDER BY distance
            LIMIT 3
            """,
            (q_vector,)
        )
        results = cur.fetchall()

    with st.spinner("生成回答中..."):
        context = "\n\n".join([f"【{title}】\n{content}" for title, content, _ in results])

        prompt = f"""你是一个助手，请根据下面的资料回答用户问题。
如果资料里没有答案，就说"资料里没有提到"。

资料：
{context}

用户问题：{question}

回答："""

        response = ollama.chat(
            model="qwen2.5:3b",
            messages=[{"role": "user", "content": prompt}]
        )

    st.markdown("### 回答")
    st.write(response["message"]["content"])

    with st.expander("查看参考资料"):
        for i, (title, content, distance) in enumerate(results, 1):
            st.markdown(f"**{i}. {title}**")
            st.caption(f"距离: {distance:.2f}")
            st.text(content[:300] + "...")
            st.divider()