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

question = "怎么戒烟？"

# 问题转向量
response = ollama.embeddings(
    model="bge-m3",
    prompt=question
)
q_vector = response["embedding"]

# 搜最相似的 3 块
cur.execute(
    """
    SELECT id, section, title, plain, embedding <-> %s::vector AS distance
    FROM document_chunk
    ORDER BY distance
    LIMIT 3
    """,
    (q_vector,)
)

results = cur.fetchall()

print(f"问题: {question}\n")
for row in results:
    id, section, title, plain, distance = row
    print(f"--- 距离: {distance:.4f} ---")
    print(f"节: {section}")
    print(f"标题: {title}")
    print(f"说人话: {plain}")
    print()

cur.close()
conn.close()