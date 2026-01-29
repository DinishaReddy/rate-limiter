from fastapi import FastAPI

app = FastAPI(title="Rate-Limiting Service")

@app.get("/")
def home():
    return {"message" : "Server is up and running." }
