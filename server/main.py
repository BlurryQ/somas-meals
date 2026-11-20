import os
import sqlite3
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field


# --- config ---

DB_PATH = os.environ.get("MEALS_DB_PATH", str(Path(__file__).parent / "meals.db"))
SCHEMA_PATH = Path(__file__).parent / "schema.sql"


# --- models ---

class MealUpdate(BaseModel):
    meals_remaining: int = Field(ge=0)
    last_action_at: datetime


# --- app setup ---

@asynccontextmanager
async def lifespan(app):
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(SCHEMA_PATH.read_text())
    finally:
        conn.close()
    yield


app = FastAPI(lifespan=lifespan)


# --- endpoints ---

@app.get("/")
def root():
    return {"info": "Go to /docs for end points"}


@app.get("/api/health")
def health_check():
    return {"status": "OK"}


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


@app.put("/api/state/{meal_type}")
def update_state(meal_type: Literal["lunch", "dinner"], update: MealUpdate):
    ts = update.last_action_at.isoformat(timespec="milliseconds").replace("+00:00", "Z")
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.execute(
            "UPDATE meal_state SET meals_remaining =?, last_action_at = ? "
            "WHERE type = ? AND last_action_at < ?",
            (update.meals_remaining, ts, meal_type, ts),
        )
        conn.commit()
        return {"meal_state_updated": cur.rowcount == 1}
    finally:
        conn.close()
