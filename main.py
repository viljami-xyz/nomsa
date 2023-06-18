"""
Main file to run the application with uvicorn
"""


import uvicorn

from app.config.settings import Settings

settings = Settings()

HOST = settings.host
PORT = int(settings.port)


if __name__ == "__main__":
    uvicorn.run("app.app:app", host=HOST, port=PORT, reload=True)
