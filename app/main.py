from fastapi import FastAPI
from app.api.routes import router as demo_router

app = FastAPI(title="Rate-Limiting Service")

app.include_router(demo_router)

@app.get("/")
def home():
    return {"message" : "Server is up and running." }
