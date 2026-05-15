from flask import Flask, render_template, request, session, redirect, url_for, flash
from services.poke_api import PokeAPI
from models.database import init_db
from models.usuario import Usuario
from models.equipo import Equipo

application = Flask(__name__)
application.secret_key = "pokesecretkey123"

api = PokeAPI()

# inicializar la base ed datos al arrancar
with application.app_context():
    init_db()


# rutas principales
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


# rutas del usuario
@application.route("/registro", methods=["GET","POST"])
def registro():
    if request.method == "POST":
        username = request.form["Username"]
        password = request.form["password"]
        exito = Usuario.crear(username,password)
        if exito:
            flash("registro exitoso, ya puedes iniciar sesion","success")
            return redirect(url_for("login"))
        else:
            flash("El usuario ya existe","Error")

    return render_template("registro.html")

@application.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        usuario = Usuario.login(username, password)
        if usuario:
            session["usuario_id"] = usuario.id
            session["username"] = usuario.username
            return redirect(url_for("index"))
        else:
            flash("Usuario o contraseña incorrectos", "error")
    return render_template("login.html")

@application.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# rutas del equipo

@application.route("/equipo")
def equipo():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    pokemones = Equipo.obtener_equipo(session["usuario_id"])
    return render_template("equipo.html", pokemones=pokemones)

@application.route("/equipo/agregar/<int:pokemon_id>/<nombre>/<path:imagen>")
def agregar_al_equipo(pokemon_id, nombre, imagen):
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    exito, mensaje = Equipo.agregar_pokemon(session["usuario_id"], pokemon_id, nombre, imagen)
    flash(mensaje, "success" if exito else "Error")
    return redirect(url_for("detalle", nombre=nombre))

@application.route("/equipo/eliminar/<int:pokemon_id>")
def eliminar_del_equipo(pokemon_id):
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    exito, mensaje = Equipo.eliminar_pokemon(session["usuario_id"], pokemon_id)
    flash(mensaje, "success" if exito else "Error")
    return redirect(url_for("equipo"))

if __name__ == "__main__":
    application.run(debug=True)