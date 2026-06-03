import json

class Pokedex:
    pokemones: str

    def __init__(self):
        self.pokemones = []

    def agregar_pokemon(self,pokemon):
        self.pokemones.append(pokemon)

    def guardar_en_db(self):
        if not self.pokemones:
            return

        from models.database import get_connection
        conn = get_connection()
        for pokemon in self.pokemones:
            validacion = conn.execute("SELECT 1 FROM cache_pokemon WHERE id = ?",(pokemon.id,)).fetchone() is not None
            if validacion == False:
                conn.execute(
                    "INSERT OR IGNORE INTO cache_pokemon (id, nombre, tipos, altura, peso, imagen, stats) VALUES (?,?,?,?,?,?,?)",
                    (pokemon.id,pokemon.nombre,json.dumps(pokemon.tipos),pokemon.altura,pokemon.peso,pokemon.imagen,json.dumps(pokemon.stats))
                )
                conn.commit()
            else:
                conn.execute(
                    "UPDATE cache_pokemon SET nombre=?, tipos=?, altura=?, peso=?, imagen=?, stats=? WHERE id=?",
                    (pokemon.nombre, json.dumps(pokemon.tipos), pokemon.altura, pokemon.peso, pokemon.imagen, json.dumps(pokemon.stats), pokemon.id)
                )
                conn.commit()
        conn.close()

    def buscar_por_nombre(self, nombre):
        pokemones = []
        nombre = nombre.lower()
        for pokemon in self.pokemones:
            if nombre in pokemon.nombre.lower():
                pokemones.append(pokemon)
        return pokemones

    def filtrar_por_tipo(self, tipo):
        tipo =  tipo.lower()
        return [p for p in self.pokemones if tipo in p.tipos]
    
    def obtener_todos(self):
        return self.pokemones

    def __len__(self):
        return len(self.pokemones)
    
    def listar(self):
        for pokemon in self.pokemones:
            print(f"pokemon {pokemon.nombre}")