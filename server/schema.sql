CREATE TABLE IF NOT EXISTS meal_state (
    type TEXT PRIMARY KEY CHECK (type IN ('lunch', 'dinner')),
    meals_remaining INTEGER NOT NULL DEFAULT 0 CHECK (meals_remaining >= 0),
    last_action_at  TEXT    NOT NULL
);


CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE NOT NULL COLLATE NOCASE,
    password_hash TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS sessions (
    token      TEXT PRIMARY KEY,
    user_id    INTEGER NOT NULL REFERENCES users(id),
    created_at TEXT NOT NULL
);


INSERT OR IGNORE INTO meal_state (type, meals_remaining, last_action_at) VALUES
    ('lunch',  0, '1970-01-01T00:00:00.000Z'),
    ('dinner', 0, '1970-01-01T00:00:00.000Z');
