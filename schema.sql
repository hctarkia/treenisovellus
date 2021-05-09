CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE workouts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    sent TIMESTAMP,
    workout TEXT,
    duration INTEGER,
    description TEXT,
    visible INTEGER
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    workout_id INTEGER REFERENCES workouts,
    sent TIMESTAMP,
    comment TEXT
);