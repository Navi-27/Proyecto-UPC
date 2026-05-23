import requests
import json
from time import sleep
from models.pokemon import Pokemon
from models.pokedex import Pokedex
from models.database import get_connection

class PokeAPI:
    BASE_URL = "https://pokeapi.co/api/v2"
    pokedex = Pokedex

    def obtener_lista_pokemones(self, limite, offset=0):
        url = f"{self.BASE_URL}/pokemon?limit={limite}&offset={offset}"
        respuesta = requests.get(url)
        datos = respuesta.json()

        pokedex = Pokedex()

        for i, item in enumerate(datos["results"]):
            sleep(0.5)
            print(f"Descargando {i+1}/{limite}...")
            url = item["url"]
            respuesta = requests.get(url)
            datos_pokemon = respuesta.json()

            numero = offset + i + 1
            imagen = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{numero}.png"
            pokemon = Pokemon(
                id=numero,
                nombre=datos_pokemon["name"],
                tipos=[t["type"]["name"] for t in datos_pokemon["types"]] if "types" in datos_pokemon else [],
                altura=datos_pokemon["height"] if "height" in datos_pokemon else 0,
                peso=datos_pokemon["weight"] if "weight" in datos_pokemon else 0,
                imagen=imagen,
                stats=datos_pokemon["stats"] if "stats" in datos_pokemon else {}
            )
            pokedex.agregar_pokemon(pokemon)
        pokedex.guardar_en_db()
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
        conn = get_connection()
        rows = conn.execute("SELECT * FROM cache_pokemon WHERE tipos LIKE ?",(tipo,)).fetchall()
        conn.close
        print(f"{rows}")
        pokemones = []
        for row in rows:
            pokemon = Pokemon(
                id=row["id"],
                nombre=row["nombre"],
                tipos=json.loads(row["tipos"]),
                altura=row["altura"],
                peso=row["peso"],
                imagen=row["imagen"],
                stats=json.loads(row["stats"]))
            pokemones.append(pokemon)
        return pokemones



        

