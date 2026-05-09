

class Pokemon:
    def __init__(self, id, nombre, tipos, altura, peso, imagen, stats):
        self.id = id
        self.nombre = nombre
        self.tipos = tipos
        self.altura = altura
        self.peso = peso
        self.imagen = imagen
        self.stats = stats

    def get_tipo_principal(self):
        return self.tipos[0] if self.tipos else "Normal"
    
    def __str__(self):
        return f"Pokemon({self.id}: {self.nombre} - {self.tipos})"