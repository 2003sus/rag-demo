import re
import psycopg2
import ollama
from pathlib import Path

BOOK_DIR = Path("data/book")

# 数据库连接
conn = psycopg2.connect(
    host="localhost",
    port=5332,
    dbname="interestingbooks",
    user="postgres",
    password="password"
)
cur = conn.cursor()

# 清空旧数据（如果重跑）
cur.execute("TRUNCATE document_chunk RESTART IDENTITY")
conn.commit()

total = 0

for md_file in sorted(BOOK_DIR.glob("*.md")):
    with open(md_file, encoding="utf-8") as f:
        content = f.read()

    parts = re.split(r"(?=^### \d+\.)", content, flags=re.MULTILINE)
    chunks = [p.strip() for p in parts if p.strip().startswith("### ")]

    section = md_file.stem

    for chunk in chunks:
        lines = chunk.split("\n")
        title = lines[0]

        plain = ""
        for line in lines:
            if line.startswith("- 说人话："):
                plain = line[len("- 说人话："):].strip()
                break

        search_text = f"{title}\n{plain}"

        # 转向量
        response = ollama.embeddings(
            model="bge-m3",
            prompt=search_text
        )
        embedding = response["embedding"]

        # 存进数据库
        cur.execute(
            """
            INSERT INTO document_chunk (section, title, plain, content, search_text, embedding)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (section, title, plain, chunk, search_text, embedding)
        )

        total += 1
        if total % 50 == 0:
            print(f"已处理 {total} 块")
            conn.commit()

conn.commit()
cur.close()
conn.close()

print(f"\n完成: {total} 块已存入数据库")