from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"info": "Go to /api for end points"}


@app.get("/api")
def doc():
    return {"health": "Get connection health"}


@app.get("/api/health")
def health_check():
    return {"status": "OK"}