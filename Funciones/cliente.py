def cliente_existe(connection, id_cliente):
    cursor = connection.cursor()
    cursor.execute("SELECT 1 FROM clientes WHERE id_cliente = %s", (id_cliente,))
    resultado = cursor.fetchone()
    cursor.close()
    return resultado is not None


def insertar_cliente(connection, nombre, contacto):
        try:
            # Abrimos cursor para ejecutar comandos
            cursor = connection.cursor()
            
            # Usamos %s para prevenir inyecciones SQL (buena práctica profesional)
            query = "INSERT INTO clientes (nombre, contacto) VALUES (%s, %s);"
            cursor.execute(query, (nombre, contacto))
            
            # Confirmar el cambio en la base de datos
            connection.commit()
            print(f"✅ Cliente '{nombre}' registrado con éxito.")
            
        except Exception as e:  
            print(f"❌ Error al insertar: {e}")
            connection.rollback() # Deshace cambios si hubo error


def obtener_clientes(connection):
    try:
        cursor = connection.cursor()

        query = "SELECT * FROM clientes ORDER BY id_cliente ASC"
        cursor.execute(query)

        clientes = cursor.fetchall()  # Trae todos los registros

        return clientes

    except Exception as e:
        print("❌ Error al obtener clientes:", e)
        return []

    finally:
        cursor.close()


def actualizar_cliente(connection, id_cliente, nuevo_nombre, nuevo_telefono):
    try:
        cursor = connection.cursor()

        query = """
        UPDATE clientes
        SET nombre = %s,
            contacto = %s
        WHERE id_cliente = %s
        """

        cursor.execute(query, (nuevo_nombre, nuevo_telefono, id_cliente))
        connection.commit()

        if cursor.rowcount == 0:
            print("❌ No se encontró un cliente con ese ID.")
        else:
            print("✅ Cliente actualizado correctamente.")

    except Exception as e:
        print("❌ Error al actualizar cliente:", e)

    finally:
        cursor.close()


def eliminar_cliente(connection, id_cliente):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id_cliente,))
    connection.commit()
    cursor.close()