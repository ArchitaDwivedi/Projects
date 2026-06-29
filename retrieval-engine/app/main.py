from fastapi import FastAPI
from .routers.ask import router as ask_router
from .routers.upload import router as upload_router

app = FastAPI()

app.include_router(ask_router)
app.include_router(upload_router)


@app.get("/")
def health_check():

    return {
        "status": "running"
    }
