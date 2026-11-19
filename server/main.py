from fastapi import FastAPI
from pathlib import Path
from contextlib import asynccontextmanager
import sqlite3
import os


DB_PATH = os.environ.get("MEALS_DB_PATH", str(Path(__file__).parent / "meals.db"))
SCHEMA_PATH = Path(__file__).parent / "schema.sql"


@asynccontextmanager
async def lifespan(app):
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(SCHEMA_PATH.read_text())
    finally:
        conn.close()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {"info": "Go to /docs for end points"}


@app.get("/api/state")
def get_state():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            "SELECT type, meals_remaining, last_action_at FROM meal_state"
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


@app.get("/api/health")
def health_check():
    return {"status": "OK"}