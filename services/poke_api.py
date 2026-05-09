import requests
from models.pokemon import Pokemon
from models.pokedex import Pokedex

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
        url = f"{self.BASE_URL}/pokemon/{nombre_o_id}"
        respuesta = requests.get(url)

        if respuesta.status_code != 200:
            return None

        datos = respuesta.json()

        return Pokemon(
            id=datos["id"],
            nombre=datos["name"],
            tipos=[t["type"]["name"] for t in datos["types"]],
            altura=datos["height"],
            peso=datos["weight"],
            imagen=datos["sprites"]["front_default"],
            stats={s["stat"]["name"]: s["base_stat"] for s in datos["stats"]}
        )
    
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