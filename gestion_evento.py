from conexion_base_de_datos import *
from gestion_salon import *
from datetime import datetime

# Clase que gestiona las acciones a realizar de los eventos.
class Evento(ConexionGestionEvento):
    def __init__(self, nombre_bd, evento_id, nombre, fecha, hora_inicio, hora_termino, salon_id):
        super().__init__(nombre_bd)
        self.evento_id = evento_id
        self.nombre = nombre
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_termino = hora_termino
        self.salon_id = salon_id

    # Método para verificar si la tabla existe
    def existe_tabla(self,nombre_tabla):
        conexion = self.conectar()
        cursor = conexion.cursor()
        # Consulta que verifica si una tabla especifica existe o no.
        # Tabla especial que almacena el esquema de la base de datos.
        cursor.execute('''
        SELECT name FROM sqlite_master WHERE type='table' AND name=? 
        ''', (nombre_tabla,))
        if cursor.fetchone():
            return True
        return False
    
    # Método heredado que crea la tabla eventos.
    def crear_tabla(self):
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute('''
        -- Tabla de eventos
        CREATE TABLE IF NOT EXISTS eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            fecha DATE NOT NULL,
            hora_inicio TIME NOT NULL,
            hora_termino TIME NOT NULL,
            salon_id INTEGER NOT NULL,
            FOREIGN KEY (salon_id) REFERENCES salones(id) ON DELETE CASCADE
        );
                            ''')
        conexion.commit()
        conexion.close()
        #sprint("Tabla 'eventos' creada con exito")

    # Método para registrar los asientos automaticamente.
    def registrar_asientos(self, evento_id, salon_id, capacidad):
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT MAX(id) FROM eventos")
        evento_id = cursor.fetchone()[0] # Busca el id del ultimo evento creado.
        # Crear asientos basados en la capacidad del salón
        for i in range(1, capacidad + 1):
            # Insertar asientos con evento_id
            cursor.execute(
                "INSERT INTO asientos (numero_asiento, salon_id, ocupado, evento_id) VALUES (?, ?, ?, ?)",
                (i, salon_id, 0, evento_id)
            )
        conexion.commit()
        conexion.close()
    
    # Método heredado para insertar datos.
    def insertar(self, nombre_evento, fecha, hora_inicio, hora_termino, salon_id):
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO eventos (nombre, fecha, hora_inicio, hora_termino, salon_id) VALUES (?, ?, ?, ?, ?)""",
            (nombre_evento, fecha, hora_inicio, hora_termino, salon_id))
        conexion.commit()
        conexion.close()
    
    # Método heredado para eliminar datos.
    def eliminar(self, evento_id):
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute("""
            DELETE FROM eventos WHERE id = ? """, (evento_id,))
        conexion.commit()
        conexion.close()

    # Método heredado para leer datos.
    def leer(self):
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM eventos")
        eventos = cursor.fetchall()
        conexion.close()
        return eventos

# Función para verificar que la hora ingresada por el usuario es correcta.
def validar_hora(hora):
    try:
        # Intenta la conversión de la hora ingresada al formato HH:MM:SS
        hora_valida = datetime.strptime(hora, "%H:%M:%S")
        return True
    except ValueError:
        return False
    
# Función para agregar eventos a la base de datos con sus asientos correspondientes.         
def agregar_evento(evento):
    print("Salones disponibles: ")
    for salon in salon_1.leer():
        print(f"{salon[0]}: {salon[1]} (Capacidad: {salon[2]})")
    
    ids_salones = [salon[0] for salon in salon_1.leer()] # Lista de IDs de los salones creados.

    # Solicita los datos al usuario.
    try: 
        salon_id = int(input("Seleccione un salón por su ID: "))
    except ValueError: # Verifica si se ingresó un numero o no.
        print("Ingrese un numero, por favor.")
        return

    if salon_id not in ids_salones:
        print("Ingrese un ID mostrado anteriormente.")
        return
    else: # Verifica si el id ingresado se encuentra en todos los id disponibles.
        pass

    fecha = input("Ingrese una fecha (DD/MM/AAAA): ")
    # Convertir fecha al formato 'YYYY-MM-DD'
    try:
        dia, mes, año = fecha.split('/')
        fecha = f"{año}-{mes.zfill(2)}-{dia.zfill(2)}"
    except ValueError: # Verifica si se ingreso bien el formato elegido.
        print("Formato de fecha incorrecto. Use DD/MM/AAAA.")
        return
    
    hora_inicio = input("Ingrese la hora de inicio (HH:MM:SS): ")

    # Verifica si la hora de inicio ingresada es valida.
    if not validar_hora(hora_inicio):
        print("Hora de inicio no valida.")
        return
    else: 
        pass

    hora_termino = input("Ingrese la hora de termino (HH:MM:SS): ")

    # Verifica si la hora de termino ingresada es valida.
    if not validar_hora(hora_termino):
        print("Hora de termino no valida.")
        return
    else:
        pass

    nombre_evento = input("Nombre del evento: ")

    # Insertar el evento en la base de datos
    evento.insertar(nombre_evento, fecha, hora_inicio, hora_termino, salon_id)
    
    # Obtener el ID del evento recién creado
    evento_id = evento.obtener_ultimo_id()

    # Obtener la capacidad del salón seleccionado
    capacidad = next(s[2] for s in salon_1.leer() if s[0] == salon_id)
    
    # Registrar automáticamente los asientos.
    evento.registrar_asientos(evento_id, salon_id, capacidad)

    print("Evento y asientos agregados con éxito")

# Función que elimina un evento de la base de datos.
def eliminar_evento(evento):
    evento = evento.leer()

    if not evento:
        print("No existen eventos para eliminar.")
        return
    else: # Verifica si existen eventos agregados.
        print("Eventos: ")
        for eventos in evento:
            print(f"ID: {eventos[0]} - Nombre: {eventos[1]}")
    
    try:
        id_evento = int(input("Seleccione un evento para eliminar por su ID: "))
    except ValueError: # Verifica si se ingresó un numero o no.
        print("Ingrese un numero, por favor.")
        return

    ids_eventos = [eventos[0] for eventos in evento] # Lista de IDs de los eventos creados.

    if id_evento not in ids_eventos:
        print("Ingrese un ID mostrado anteriormente.")
        return
    else: # Verifica si el id ingresado se encuentra en todos los id disponibles.
        evento.eliminar(id_evento) 
        print(f"Evento {eventos[1]} eliminado con exito")

# Menú principal de la gestión de eventos.
def menu_evento(evento):
    bandera = True

    while bandera:
        print("\n--- Menú de Gestión de Eventos---")
        print("1.- Agregar Evento")
        print("2.- Eliminar Evento")
        print("Ingrese Q para regresar al menu principal.")

        eleccion_usuario = input("> ")

        if eleccion_usuario == "1":
            agregar_evento(evento)
        elif eleccion_usuario == "2":
            eliminar_evento(evento)
        elif eleccion_usuario == "q" or eleccion_usuario == "Q":
            #print("salir\n")
            print("Saliendo del programa\n")
            bandera = False
        else:
            print("El valor ingresado es incorrecto")
            print("Volviendo al menu principal\n")

# Creación del objeto Evento y nombre de la base de datos.
nombre_bd = "eventos.db"
evento = Evento(nombre_bd, None, None, None, None, None, None)

# Creación de la tabla evento.
if not evento.existe_tabla('eventos'):
    evento.crear_tabla()
else:
    pass
    #print("La tabla 'eventos' ya esta creada.")

# Inicio del menú de eventos.
#menu_evento(evento)