from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.routes import router
from app.api.routes_metrics import router as metrics_router

app = FastAPI(title="Rate Limiting Service")

# 1) Serve files from app/static at the URL path /static
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 2) Include API routers
app.include_router(router)
app.include_router(metrics_router)

# 3) Make "/" return the frontend HTML page
@app.get("/")
def home():
    return FileResponse("app/static/index.html")


