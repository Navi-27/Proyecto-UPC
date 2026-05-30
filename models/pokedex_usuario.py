from models.database import get_connection

class PokedexUsuario:
    

    @staticmethod
    def registrar_visto(usuario_id, pokemon_id, pokemon_nombre):
        conn = get_connection()
        conn.execute('''
            INSERT OR IGNORE INTO pokedex_usuario 
            (usuario_id, pokemon_id, pokemon_nombre)
            VALUES (?,?,?)
        ''',(usuario_id, pokemon_id, pokemon_nombre)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def obtener_vistos(usuario_id):
        conn = get_connection()
        rows = conn.execute('''
            SELECT * FROM pokedex_usuario WHERE usuario_id = ? ORDER BY fecha_visto DESC
        ''',(usuario_id,)).fetchall()
        conn.close()
        return rows
    
    @staticmethod
    def esta_visto(usuario_id, pokemon_id):
        conn = get_connection()
        row = conn.execute(
            """SELECT 1 FROM pokedex_usuario 
            WHERE usuario_id = ? AND pokemon_id = ?""",
            (usuario_id, pokemon_id)
        ).fetchone()
        conn.close()
        return row is not None
