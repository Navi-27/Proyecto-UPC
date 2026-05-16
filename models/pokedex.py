from models.pokemon import Pokemon
import json

class Pokedex:
    def __init__(self):
        self.pokemones = []

    def agregar_pokemon(self,pokemon):
        self.pokemones.append(pokemon)
        from models.database import get_connection
        conn = get_connection()
        conn.execute(
            "INSERT OR IGNORE INTO cache_pokemon (id, nombre, tipos, altura, peso, imagen, stats) VALUES (?,?,?,?,?,?,?)",
            (
                pokemon.id,
                pokemon.nombre,
                json.dumps(pokemon.tipos),
                pokemon.altura,
                pokemon.peso,
                pokemon.imagen,
                json.dumps(pokemon.stats)
            )
        )
        conn.commit()
        conn.close()
        conn = get_connection()
        conn.execute(
            "UPDATE cache_pokemon SET nombre=?, tipos=?, altura=?, peso=?, imagen=?, stats=? WHERE id=?",
            (
                pokemon.nombre,
                json.dumps(pokemon.tipos),
                pokemon.altura,
                pokemon.peso,
                pokemon.imagen,
                json.dumps(pokemon.stats),
                pokemon.id
            )
        )
        conn.commit()
        conn.close()
        print({ "UPDATE cache_pokemon SET nombre=?, tipos=?, altura=?, peso=?, imagen=?, stats=? WHERE id=?",
            (
                pokemon.nombre,
                json.dumps(pokemon.tipos,True),
                pokemon.altura,
                pokemon.peso,
                pokemon.imagen,
                json.dumps(pokemon.stats,True),
                pokemon.id
            )})

    def buscar_por_nombre(self, nombre):
        nombre = nombre.lower()
        return [p for p in self.pokemones if nombre in p.nombre.lower()]
    
    def filtrar_por_tipo(self, tipo):
        tipo =  tipo.lower()
        return [p for p in self.pokemones if tipo in p.tipos]
    
    def obtener_todos(self):
        return self.pokemones
    
    def __len__(self):
        return len(self.pokemones)