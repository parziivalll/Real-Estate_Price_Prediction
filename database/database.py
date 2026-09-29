import sqlite3, os

BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH=os.path.join(BASE,"database","real_estate.db")

def get_connection():
    con=sqlite3.connect(DB_PATH)
    con.row_factory=sqlite3.Row
    return con

def init_db():
    con=get_connection()
    con.execute("""
    CREATE TABLE IF NOT EXISTS predictions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location TEXT NOT NULL,
        property_type TEXT NOT NULL,
        area_sqft REAL NOT NULL,
        bhk INTEGER NOT NULL,
        bathrooms INTEGER NOT NULL,
        floor INTEGER NOT NULL,
        property_age INTEGER NOT NULL,
        parking TEXT NOT NULL,
        furnishing TEXT NOT NULL,
        predicted_price REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    con.commit()
    con.close()
