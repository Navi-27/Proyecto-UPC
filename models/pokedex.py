from models.pokemon import Pokemon

class Pokedex:
    def __init__(self):
        self.pokemones = []

    def agregar_pokemon(self,pokemon):
        self.pokemones.append(pokemon)

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