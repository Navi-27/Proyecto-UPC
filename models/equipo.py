from models.database import get_connection

class Equipo:
    MAX_POKEMONES = 6

    @staticmethod
    def obtener_equipo(usuario_id):
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM equipos WHERE usuario_id = ?",(usuario_id,)
        ).fetchall()
        conn.close()
        return rows
    
    @staticmethod
    def agregar_pokemon(usuario_id, pokemon_id, pokemon_nombre, pokemon_imagen):
        equipo = Equipo.obtener_equipo(usuario_id)
        if len(equipo) >= Equipo.MAX_POKEMONES:
            return False, "El equipo ya esta completo (6 Pokemones)"
        
        for p in equipo:
            if p["pokemin_id"] == pokemon_id:
                return False, "El pokemon ya se encuentra en tu equipo"
            
        conn = get_connection()
        conn.execute(
            "INSERT INTO equipos (usuario_id, pokemon_id, pokemon_nombre, pokemon_imagen) VALUES (?,?,?,?)",
            (usuario_id,pokemon_id,pokemon_nombre,pokemon_imagen)
        )
        conn.commit()
        conn.close()
        return True, "Pokemon Agregado"
    
    @staticmethod
    def eliminar_pokemon(usuario_id, pokemon_id):
        equipo = Equipo.obtener_equipo(usuario_id)
        
        encontrado = False
        for p in equipo:
            if p['pokemon_id'] == pokemon_id:
                encontrado = True
                break
        
        if not encontrado:
            return False, "Este pokémon no está en tu equipo"

        conn = get_connection()
        conn.execute(
            "DELETE FROM equipos WHERE usuario_id = ? AND pokemon_id = ?",
            (usuario_id, pokemon_id)
        )
        conn.commit()
        conn.close()
        return True, "Pokémon eliminado"