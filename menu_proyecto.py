import time
from gestion_asiento import *
from gestion_asistentes import *
from gestion_evento import *
from gestion_salon import *
from gestion_salon import *
from gestion_tickets import *

def menu_principal():
    bandera = True

    while bandera:
        print("\tBienvenido a OCASO EVENTOS")
        print("\nQué acción desea hacer?")
        print("\t1.- Opciones de Evento")
        print("\t2.- Opciones de Asistente")
        print("\tIngrese Q para salir.\n")

        eleccion_usuario = input("> ")

        if eleccion_usuario == "1":
            print("Entrando al menú de eventos\n")
            time.sleep(1)
            menu_evento(evento)
        elif eleccion_usuario == "2":
            print("Entrando al menú de asistente\n")
            time.sleep(1)
            menu_asistente()
        elif eleccion_usuario == "q" or eleccion_usuario == "Q":
            print("Saliendo del programa\n")
            time.sleep(1)
            bandera = False
        else:
            print("El valor ingresado es incorrecto")
            print("Volviendo al menu principal\n")
            time.sleep(1)

if __name__ == "__main__":
    menu_principal()