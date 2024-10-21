import sqlite3

# Clase que hace la conexion a la base de datos con las operaciones crud.
class ConexionGestionEvento:
    def __init__(self, nombre_bd):
        # Conexion a la base de datos, si no existe la crea
        self.nombre_bd = nombre_bd
    
    # Método para conectar con la base de datos
    def conectar(self):
        return sqlite3.connect(self.nombre_bd)
    
    # Método para verificar si la tabla existe
    def existe_tabla(self,nombre_tabla):
        conexion = self.conectar()
        cursor = conexion.cursor()
        # Consulta que verifica si una tabla especifica existe o no.
        cursor.execute('''
        SELECT name FROM sqlite_master WHERE type='table' AND name=?
        ''', (nombre_tabla,))
        if cursor.fetchone():
            return True
        return False
    
    # Método abstracto para crear las tablas necesarias.
    def crear_tabla(self):
        pass

    # Método para obtener el ultimo id.    
    def obtener_ultimo_id(self):
        conexion = self.conectar()
        cursor = conexion.cursor()
        return cursor.lastrowid
    
    # Método abstracto para insertar datos.    
    def insertar(self):
        pass

    # Método abstracto para leer datos.    
    def leer(self):
        pass
    
    # Método abstracto actualizar datos.
    def actualizar(self):
        pass
    
    # Método abstracto para eliminar datos.
    def eliminar(self):
        pass