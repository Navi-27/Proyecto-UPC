from werkzeug.security import generate_password_hash, check_password_hash
from models.database import get_connection

class Usuario:
    def __init__(self, id, username):
        self.id = id
        self.username = username

    @staticmethod
    def crear(username, password):
        conn = get_connection()
        try:
            conn.execute(
                "INSERT INTO usuarios (username, password) VALUES (?,?)",
                (username, generate_password_hash(password))
            )
            conn.commit()
            return True
        except:
            return False 
        finally:
            conn.close()
    
    @staticmethod
    def login(username, password):
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM usuarios WHERE username = ?",(username,)
        ).fetchone()
        conn.close()

        if row and check_password_hash(row["password"], password):
            return Usuario(row["id"], row["username"])
        return None