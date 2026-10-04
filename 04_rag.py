import psycopg2
import ollama

conn = psycopg2.connect(
    host="localhost",
    port=5332,
    dbname="interestingbooks",
    user="postgres",
    password="password"
)
cur = conn.cursor()

# 用户提问
question = "被裁了该拿多少补偿？"

# 1. 问题转向量
response = ollama.embeddings(
    model="bge-m3",
    prompt=question
)
q_vector = response["embedding"]

# 2. 搜最相似的 3 块
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

# 3. 拼 prompt
context = "\n\n".join([f"【{title}】\n{content}" for title, content, _ in results])

prompt = f"""你是一个助手，请根据下面的资料回答用户问题。
如果资料里没有答案，就说“资料里没有提到”。

资料：
{context}

用户问题：{question}

回答："""

# 4. 调对话模型
print("生成回答中...\n")
response = ollama.chat(
    model="qwen2.5:3b",
    messages=[{"role": "user", "content": prompt}]
)

print("=== 回答 ===")
print(response["message"]["content"])

cur.close()
conn.close()