from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, desires

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Разрешаем запросы с фронтенда
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы
    allow_headers=["*"],  # Разрешаем все заголовки
)

@app.get("/")
async def welcome() -> dict:
    return {"message": "My e-commerce app"}

app.include_router(auth.router)
app.include_router(desires.router)

#uvicorn app.main:app --port 8000 --reload
#cd frontend && npm run dev