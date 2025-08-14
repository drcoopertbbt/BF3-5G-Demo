# File location: 5G_Emulator_API/core_network/udsf.py
# File location: 5G_Emulator_API/core_network/udsf.py
# File location: 5G_Emulator_API/core_network/udsf.py
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import uvicorn

app = FastAPI()

class UnstructuredData(BaseModel):
    id: str
    data: str

def init_db():
    conn = sqlite3.connect('udsf.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS unstructured_data (
            id TEXT PRIMARY KEY,
            data TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.post("/store_data")
def store_data(data: UnstructuredData):
    conn = sqlite3.connect('udsf.db')
    c = conn.cursor()
    c.execute('INSERT INTO unstructured_data (id, data) VALUES (?, ?)', (data.id, data.data))
    conn.commit()
    conn.close()
    return {"message": "Data stored successfully"}

@app.get("/get_data/{id}")
def get_data(id: str):
    conn = sqlite3.connect('udsf.db')
    c = conn.cursor()
    c.execute('SELECT data FROM unstructured_data WHERE id = ?', (id,))
    data = c.fetchone()
    conn.close()
    if data:
        return {"id": id, "data": data[0]}
    else:
        return {"message": "Data not found"}

if __name__ == "__main__":
    init_db()
    uvicorn.run(app, host="127.0.0.1", port=9006)
