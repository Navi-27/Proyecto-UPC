import requests
import json
from models.pokemon import Pokemon
from models.pokedex import Pokedex
from models.database import get_connection

class PokeAPI:
    BASE_URL = "https://pokeapi.co/api/v2"

    def obtener_lista_pokemones(self, limite=151, offset=0):
        url = f"{self.BASE_URL}/pokemon?limit={limite}&offset={offset}"
        respuesta = requests.get(url)
        datos = respuesta.json()

        pokedex = Pokedex()
        for i, item in enumerate(datos["results"]):
            numero = offset + i + 1
            imagen = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{numero}.png"
            pokemon = Pokemon(
                id=numero,
                nombre=item["name"],
                tipos=[],
                altura=0,
                peso=0,
                imagen=imagen,
                stats={}
            )
            pokedex.agregar_pokemon(pokemon)

        return pokedex

    def obtener_pokemon(self, nombre_o_id):
        # 1. Buscar en caché primero
        try:
            conn = get_connection()
            row = conn.execute(
                "SELECT * FROM cache_pokemon WHERE nombre = ? OR id = ?",
                (str(nombre_o_id), str(nombre_o_id))
            ).fetchone()
            conn.close()

            if row:
                return Pokemon(
                    id=row["id"],
                    nombre=row["nombre"],
                    tipos=json.loads(row["tipos"]),
                    altura=row["altura"],
                    peso=row["peso"],
                    imagen=row["imagen"],
                    stats=json.loads(row["stats"])
                )
        except:
            pass

        # 2. Si no está en caché, llamar la API
        try:
            url = f"{self.BASE_URL}/pokemon/{nombre_o_id}"
            respuesta = requests.get(url, timeout=5)

            if respuesta.status_code != 200:
                return None

            datos = respuesta.json()

            pokemon = Pokemon(
                id=datos["id"],
                nombre=datos["name"],
                tipos=[t["type"]["name"] for t in datos["types"]],
                altura=datos["height"],
                peso=datos["weight"],
                imagen=datos["sprites"]["front_default"],
                stats={s["stat"]["name"]: s["base_stat"] for s in datos["stats"]}
            )

            # 3. Guardar en caché
            try:
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
            except:
                pass

            return pokemon

        except:
            return None

    def obtener_por_tipo(self, tipo):
        url = f"{self.BASE_URL}/type/{tipo}"
        respuesta = requests.get(url)
        datos = respuesta.json()

        pokedex = Pokedex()
        for i, item in enumerate(datos["pokemon"]):
            nombre = item["pokemon"]["name"]
            numero = item["pokemon"]["url"].split("/")[-2]
            imagen = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{numero}.png"
            pokemon = Pokemon(
                id=int(numero),
                nombre=nombre,
                tipos=[tipo],
                altura=0,
                peso=0,
                imagen=imagen,
                stats={}
            )
            pokedex.agregar_pokemon(pokemon)

        return pokedex