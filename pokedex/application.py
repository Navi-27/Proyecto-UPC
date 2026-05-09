from flask import Flask, render_template, request
from services.poke_api import PokeAPI

application = Flask(__name__)
api = PokeAPI()

@application.route("/")
def index():
    tipo = request.args.get("tipo", "")
    busqueda = request.args.get("busqueda", "")

    pokedex = api.obtener_lista_pokemones(limite=1025)
    pokemones = pokedex.obtener_todos()

    if busqueda:
        pokemones = pokedex.buscar_por_nombre(busqueda)
    elif tipo:
        pokedex = api.obtener_por_tipo(tipo)
        pokemones = pokedex.obtener_todos()

    return render_template("index.html", pokemones=pokemones, tipo=tipo, busqueda=busqueda)

@application.route("/pokemon/<nombre>")
def detalle(nombre):
    pokemon = api.obtener_pokemon(nombre)
    return render_template("detalle.html", pokemon=pokemon)

if __name__ == "__main__":
    application.run(debug=True)