from Funciones.cliente import *

def pedir_datos_cliente():
        nombre = input("Ingrese el nombre del cliente: ").strip()
        telefono = input("Ingrese el telefono del cliente: ").strip()

        if not nombre or not telefono:
            print("❌ Error: Los campos no pueden estar vacíos.")
            return None, None

        return nombre, telefono


def mostrar_clientes(connection):
    clientes = obtener_clientes(connection)
    for cliente in clientes:
        id_cliente, nombre, telefono = cliente
        print(f"ID: {id_cliente} | Nombre: {nombre} | Teléfono: {telefono}")


def actualizar_datos_cliente(connection):
    id_cliente = input("Ingrese el ID del cliente a actualizar: ").strip()
    nuevo_nombre = input("Nuevo nombre: ").strip()
    nuevo_telefono = input("Nuevo telefono: ").strip()

    if not id_cliente.isdigit():
        print("❌ El ID debe ser un número.")
        return
    if id_cliente and nuevo_nombre and nuevo_telefono:
        actualizar_cliente(connection, int(id_cliente), nuevo_nombre, nuevo_telefono)
    else:
        print("❌ Todos los campos son obligatorios.")


def eliminar_datos_cliente(connection):
    id_cliente = input("Ingrese el ID del cliente a eliminar: ").strip()

    if not id_cliente.isdigit():
        print("❌ El ID debe ser numérico.")
    else:
        id_cliente = int(id_cliente)
        

        if not cliente_existe(connection, id_cliente):
            print("❌ No existe un cliente con ese ID.")
        else:
            confirmacion = input("❗ ¿Está seguro que desea eliminar este cliente? (s/n): ").lower()
        
            if confirmacion == "s":
                eliminar_cliente(connection, int(id_cliente))
                print("✅ Cliente eliminado correctamente.")
            else:
                print("❌ Operación cancelada.")
        
