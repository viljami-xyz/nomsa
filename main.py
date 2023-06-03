"""
Main file to run the application with uvicorn
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import uvicorn
from app.config.settings import Settings
from app.routes import authentication, home

settings = Settings()

HOST = settings.host
PORT = int(settings.port)

app = home.app
app.include_router(authentication.router)

app.mount("/static", StaticFiles(directory="static"), name="static")



if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
    