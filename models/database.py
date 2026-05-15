import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'pokedex.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript('''
            CREATE TABLE IF NOT EXISTS usuarios(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            );


            CREATE TABLE IF NOT EXISTS equipos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                pokemon_id INTEGER NOT NULL,
                pokemon_nombre TEXT NOT NULL,
                pokemon_imagen TEXT,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            );

            CREATE TABLE IF NOT EXISTS cache_pokemon (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                tipos TEXT,
                altura INTEGER,
                peso INTEGER,
                imagen TEXT,
                stats TEXT
            );

            ''');
    conn.commit()
    conn.close()
        
    