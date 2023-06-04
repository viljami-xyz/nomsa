"""
Main file to run the application with uvicorn
"""

from fastapi.staticfiles import StaticFiles

import uvicorn
from app.config.settings import Settings
from app.routes import authentication, home, books, diary, reflections

settings = Settings()

HOST = settings.host
PORT = int(settings.port)

app = home.app
app.include_router(authentication.router)
app.include_router(books.router)
app.include_router(diary.router)
app.include_router(reflections.router)

app.mount("/static", StaticFiles(directory="static"), name="static")



if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
    