from conexion_base_de_datos import ConexionGestionEvento

class Asiento(ConexionGestionEvento):
    def __init__(self, nombre_bd, asiento_id, numero, ocupado, salon_id):
        super().__init__(nombre_bd)
        self.asiento_id = asiento_id
        self.numero = numero
        self.ocupado = ocupado
        self.salon_id = salon_id
    
    # Método para verificar si la tabla existe
    def existe_tabla(self,nombre_tabla):
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute('''
        SELECT name FROM sqlite_master WHERE type='table' AND name=?
        ''', (nombre_tabla,))
        if cursor.fetchone():
            return True
        return False

    # Método heredado que crea la tabla asientos.
    def crear_tabla(self):
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute('''
        -- Tabla de asientos
        CREATE TABLE IF NOT EXISTS asientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_asiento INTEGER NOT NULL,
            salon_id INTEGER NOT NULL,
            ocupado INTEGER DEFAULT 0, -- 0: Libre, 1: Ocupado
            evento_id INTEGER NOT NULL,
            FOREIGN KEY (salon_id) REFERENCES salones(id) ON DELETE CASCADE
            FOREIGN KEY (evento_id) REFERENCES eventos(id) ON DELETE CASCADE
        );
                            ''')
        conexion.commit()
        conexion.close()
        print("Tabla 'asientos' creado con exito.")

    # Método heredado que inserta datos a la base de datos.
    def insertar(self, asientos):
        conexion = self.conectar()
        cursor = conexion.cursor()
        # Inserción de los datos por defecto.
        cursor.executemany("""
            INSERT INTO asientos (id, numero_asiento, ocupado, salon_id, evento_id)
            VALUES (?,?,?,?,?); """, (asientos))
        conexion.commit()
        conexion.close()

def creacion_asientos():

    nombre_bd = "eventos.db"
    asiento = Asiento(nombre_bd, None, None, None, None)

    # Creación de la tabla asientos.
    if not asiento.existe_tabla('asientos'):
        asiento.crear_tabla()
    else:
        print("La tabla 'asientos' ya esta creada.")

creacion_asientos()