import re
from pathlib import Path

BOOK_DIR = Path("data/book")

all_chunks = []

for md_file in sorted(BOOK_DIR.glob("*.md")):
    with open(md_file, encoding="utf-8") as f:
        content = f.read()

    parts = re.split(r"(?=^### \d+\.)", content, flags=re.MULTILINE)
    chunks = [p.strip() for p in parts if p.strip().startswith("### ")]

    for chunk in chunks:
        lines = chunk.split("\n")
        title = lines[0]  # ### 1. xxx

        # 提取“说人话”那一行
        plain = ""
        for line in lines:
            if line.startswith("- 说人话："):
                plain = line[len("- 说人话："):].strip()
                break

        # 搜索用的文本：标题 + 说人话
        search_text = f"{title}\n{plain}"

        all_chunks.append({
            "section": md_file.stem,
            "title": title,
            "plain": plain,
            "search_text": search_text,
            "content": chunk,       # 完整原文，展示用
        })

print(f"总共: {len(all_chunks)} 块")

lengths = [len(c["search_text"]) for c in all_chunks]
print(f"\n搜索文本大小:")
print(f"  最小: {min(lengths)} 字符")
print(f"  最大: {max(lengths)} 字符")
print(f"  平均: {sum(lengths) // len(lengths)} 字符")

# 超过 500 字符的
long = [c for c in all_chunks if len(c["search_text"]) > 500]
print(f"\n超过 500 字符的搜索文本: {len(long)} 块")

print(f"\n第一块预览:")
print(f"标题: {all_chunks[0]['title']}")
print(f"说人话: {all_chunks[0]['plain'][:200]}")