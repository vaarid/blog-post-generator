import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_post(topic: str):
    prompt_title = f"Придумай привлекательный заголовок для поста на тему: {topic}"
    title = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt_title}],
        max_tokens=50,
        temperature=0.7
    ).choices[0].message.content.strip()

    prompt_meta = f"Напиши краткое мета-описание для поста «{title}»."
    meta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt_meta}],
        max_tokens=80,
        temperature=0.7
    ).choices[0].message.content.strip()

    prompt_post = (
        f"Напиши увлекательный пост на тему «{topic}». "
        f"Используй короткие абзацы, подзаголовки и примеры."
    )
    content = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt_post}],
        max_tokens=800,
        temperature=0.7
    ).choices[0].message.content.strip()

    return {"title": title, "meta": meta, "content": content}

if __name__ == "__main__":
    topic = input("Введите тему поста: ")
    post = generate_post(topic)
    print("\n=== Сгенерированный пост ===")
    print(f"📌 {post['title']}\n\n📝 {post['meta']}\n\n{post['content']}")
