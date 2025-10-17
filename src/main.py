import uvicorn
from fastapi import FastAPI

from src.auth.router import router as auth_router

app = FastAPI(
    title="Svetlya4kiAPI",
    description="API service for business management in the technical production sector.",
    contact={
        "name": "Kirill Salnikov",
        "url": "https://t.me/Klr11111",
        "email": "my@ksalnikov.ru"
    }
)

app.include_router(auth_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
