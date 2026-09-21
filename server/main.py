from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"info": "Go to /api for docs"}


@app.get("/api/health")
def health_check():
    return {"status": "OK"}