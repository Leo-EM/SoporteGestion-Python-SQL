def cliente_existe(connection, id_servicio):
    cursor = connection.cursor()
    cursor.execute("SELECT 1 FROM servicios WHERE id_servicio = %s", (id_servicio,))
    resultado = cursor.fetchone()
    cursor.close()
    return resultado is not None


def obtener_servicios(connection):
    try:
        cursor = connection.cursor()

        query = "SELECT * FROM servicios ORDER BY id_servicio ASC"
        cursor.execute(query)

        servicios = cursor.fetchall()  # Trae todos los registros

        return servicios

    except Exception as e:
        print("❌ Error al obtener los servicios:", e)
        return []

    finally:
        cursor.close()