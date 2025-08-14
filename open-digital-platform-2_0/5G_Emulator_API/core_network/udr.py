# File location: 5G_Emulator_API/core_network/udr.py
# File location: 5G_Emulator_API/core_network/udr.py
# File location: 5G_Emulator_API/core_network/udr.py
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import uvicorn

app = FastAPI()

class UserData(BaseModel):
    imsi: str
    key: str

def init_db():
    conn = sqlite3.connect('udr.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            imsi TEXT PRIMARY KEY,
            key TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.post("/register_user")
def register_user(user: UserData):
    conn = sqlite3.connect('udr.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (imsi, key) VALUES (?, ?)', (user.imsi, user.key))
    conn.commit()
    conn.close()
    return {"message": "User registered successfully"}

@app.get("/get_user/{imsi}")
def get_user(imsi: str):
    conn = sqlite3.connect('udr.db')
    c = conn.cursor()
    c.execute('SELECT key FROM users WHERE imsi = ?', (imsi,))
    user = c.fetchone()
    conn.close()
    if user:
        return {"imsi": imsi, "key": user[0]}
    else:
        return {"message": "User not found"}

if __name__ == "__main__":
    init_db()
    uvicorn.run(app, host="127.0.0.1", port=9005)
