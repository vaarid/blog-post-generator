import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware  # 👈 добавили
from fastapi.responses import JSONResponse

# === 1. Загружаем ключи из .env ===
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ Не найден API-ключ. Добавь его в файл .env")

client = OpenAI(api_key=api_key)

# === 2. Инициализация приложения ===
app = FastAPI(title="Blog Post Generator API", version="1.0.0")

# === 3. Добавляем CORS (исправление Swagger UI) ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # разрешаем любые источники (для теста)
    allow_credentials=True,
    allow_methods=["*"],          # разрешаем все методы (GET, POST, ...)
    allow_headers=["*"],          # разрешаем любые заголовки
)

# === 4. Модель данных ===
class Topic(BaseModel):
    topic: str

# === 5. Основная функция генерации ===
def generate_post(topic: str):
    try:
        prompt = (
            f"Создай структурированный пост для Telegram на тему '{topic}'. "
            f"Формат: заголовок, метаописание, текст с подзаголовками и короткими абзацами."
        )
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.7,
        )
        content = response.choices[0].message.content.strip()
        return {"topic": topic, "post": content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# === 6. Эндпоинты ===
@app.post("/generate-post")
async def generate_post_api(data: Topic):
    post = generate_post(data.topic)
    return JSONResponse(
        content={"topic": data.topic, "post": post},
        ensure_ascii=False  # 🔥 выключаем экранирование русских символов
    )

@app.get("/")
async def root():
    """
    Корневой маршрут. Возвращает краткую информацию о проекте.
    """
    return {
        "message": "🚀 Blog Post Generator API is running",
        "version": "1.0.0",
        "author": "vaarid (Евгений)"
    }

@app.get("/heartbeat")
async def heartbeat():
    return {"status": "OK"}

# === 7. Точка входа при локальном запуске ===
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
