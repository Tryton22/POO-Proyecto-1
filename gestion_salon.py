from conexion_base_de_datos import ConexionGestionEvento

# Clase que carga los salones pre-existentes a la base de datos.
class Salon(ConexionGestionEvento):
    def __init__(self, nombre_bd, salon_id, nombre, capacidad):
        super().__init__(nombre_bd)
        self.salon_id = salon_id
        self.nombre = nombre
        self.capacidad = capacidad

    # Método para verificar si la tabla existe
    def existe_tabla(self,nombre_tabla):
        # Conexión a la base de datos.
        conexion = self.conectar()
        cursor = conexion.cursor()
        # Consulta que verifica si una tabla especifica existe o no.
        cursor.execute('''
        SELECT name FROM sqlite_master WHERE type='table' AND name=?
        ''', (nombre_tabla,))
        if cursor.fetchone():
            return True
        return False

    # Método heredado que crea la tabla salones.
    def crear_tabla(self):
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute('''
            -- Tabla de salones
            CREATE TABLE IF NOT EXISTS salones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                capacidad INTEGER NOT NULL
            );
                            ''')
        conexion.commit()
        conexion.close()
        #print("Tabla 'salones' creada con exito.")
    
    # Método heredado que inserta datos a la base de datos.
    def insertar(self):
        conexion = self.conectar()
        cursor = conexion.cursor()
        # Inserción de los datos por defecto.
        cursor.execute("""
            INSERT INTO salones (id, nombre, capacidad)
            VALUES (?,?,?) """, (self.salon_id, self.nombre, self.capacidad))
        conexion.commit()
        conexion.close()

    # Método heredado para leer todos los salones de la base de datos.
    def leer(self):
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM salones")
        salones = cursor.fetchall()
        conexion.close()
        return salones

# Función que crea la tabla salones.    
def creacion_salones(salon_1, salon_2, salon_3):
    # Creación de la tabla salones.
    if not salon_1.existe_tabla('salones'):
        salon_1.crear_tabla()

        # Creación de los salones por defecto.
        salon_1.insertar()
        salon_2.insertar()
        salon_3.insertar()
        #print("Salones creados con exito.")

    else:
        pass
        #print("La tabla 'salones' ya esta creada")


# Variable que indica el nombre de la base de datos.
nombre_bd = "eventos.db"

# Creación del objeto Salon para crear tabla e insertar valores por defecto.
salon_1 = Salon(nombre_bd, 1, "Salon Principal", 25)
salon_2 = Salon(nombre_bd, 2, "Teatro", 16)
salon_3 = Salon(nombre_bd, 3, "Comedor", 16)

creacion_salones(salon_1, salon_2, salon_3)