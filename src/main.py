import uvicorn
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse

from src.auth.router import router as auth_router
from src.core.exceptions import DatabaseError, DatabaseInternalError

app = FastAPI(
    title="Svetlya4kiAPI",
    description="API service for business management in the technical production sector.",
    contact={
        "name": "Kirill Salnikov",
        "url": "https://t.me/Klr11111",
        "email": "my@ksalnikov.ru"
    }
)

@app.exception_handler(DatabaseError)
def db_internal_handler(request: Request, exc: Exception):
    """ Обработчик внутренних ошибок базы данных """
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Internal Error"
    )

@app.exception_handler(DatabaseInternalError)
def db_exception_handler(request: Request, exc: Exception):
    """ Обработчик ошибок базы данных """
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Некорректные данные"
    )


app.include_router(auth_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
