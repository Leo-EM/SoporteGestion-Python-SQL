import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from Funciones.cliente import *
from Database.config_privada import get_connection


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión")
        self.root.geometry("400x300")

        self.connection = get_connection()

        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

        # Botones principales
        tk.Label(root, text="Menú Principal", font=("Arial", 16)).pack(pady=20)

        tk.Button(root, text="Clientes", width=20, command=self.abrir_clientes).pack(pady=10)
        tk.Button(root, text="Servicios", width=20).pack(pady=10)
        tk.Button(root, text="Órdenes de Trabajo", width=20).pack(pady=10)

    def cerrar_aplicacion(self):
        if self.connection:
            self.connection.close()
        self.root.destroy()

    def abrir_clientes(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Gestión de Clientes")
        ventana.geometry("600x400")

        tk.Label(ventana, text="Clientes", font=("Arial", 14)).pack(pady=10)

        # ---- TABLA ----
        columnas = ("id", "nombre", "telefono")

        tree = ttk.Treeview(ventana, columns=columnas, show="headings")

        tree.heading("id", text="ID")
        tree.heading("nombre", text="Nombre")
        tree.heading("telefono", text="Teléfono")

        tree.pack(fill="both", expand=True, pady=10)

        # ---- FUNCION PARA CARGAR DATOS ----
        def cargar_clientes():
            # Limpiar tabla
            for fila in tree.get_children():
                tree.delete(fila)

            clientes = obtener_clientes(self.connection)

            for cliente in clientes:
                tree.insert("", tk.END, values=cliente)

        # ---- BOTONES ----
        tk.Button(
            ventana,
            text="Agregar Cliente",
            command=lambda: self.agregar_cliente(tree)
        ).pack(pady=5)

        tk.Button(
            ventana,
            text="Actualizar Seleccionado",
            command=lambda: self.actualizar_cliente(tree)
        ).pack(pady=5)

        tk.Button(
            ventana,
            text="Eliminar Seleccionado",
            command=lambda: self.eliminar_cliente(tree)
        ).pack(pady=5)

        # Cargar al abrir
        cargar_clientes()

    def mostrar_clientes(self):
        clientes = obtener_clientes(self.connection)

        texto = ""
        for cliente in clientes:
            id_cliente, nombre, telefono = cliente
            texto += f"ID: {id_cliente} | {nombre} | {telefono}\n"

        messagebox.showinfo("Lista de Clientes", texto if texto else "No hay clientes.")

    def agregar_cliente(self, tree):
        ventana = tk.Toplevel(self.root)
        ventana.title("Agregar Cliente")
        ventana.geometry("300x250")

        tk.Label(ventana, text="Nombre:").pack(pady=5)
        entry_nombre = tk.Entry(ventana)
        entry_nombre.pack(pady=5)

        tk.Label(ventana, text="Teléfono:").pack(pady=5)
        entry_telefono = tk.Entry(ventana)
        entry_telefono.pack(pady=5)

        def guardar_cliente():
            nombre = entry_nombre.get().strip()
            telefono = entry_telefono.get().strip()

            if not nombre or not telefono:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            insertar_cliente(self.connection, nombre, telefono)
            messagebox.showinfo("Éxito", "Cliente agregado correctamente.")

            ventana.destroy()

            # 🔥 Recargar tabla automáticamente
            for fila in tree.get_children():
                tree.delete(fila)

            clientes = obtener_clientes(self.connection)
            for cliente in clientes:
                tree.insert("", tk.END, values=cliente)

        tk.Button(ventana, text="Guardar", command=guardar_cliente).pack(pady=15)

    def actualizar_cliente(self, tree):
        seleccion = tree.selection()

        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un cliente.")
            return

        valores = tree.item(seleccion[0], "values")
        id_cliente, nombre_actual, telefono_actual = valores

        ventana = tk.Toplevel(self.root)
        ventana.title("Actualizar Cliente")
        ventana.geometry("300x250")

        tk.Label(ventana, text="Nombre:").pack(pady=5)
        entry_nombre = tk.Entry(ventana)
        entry_nombre.insert(0, nombre_actual)
        entry_nombre.pack(pady=5)

        tk.Label(ventana, text="Teléfono:").pack(pady=5)
        entry_telefono = tk.Entry(ventana)
        entry_telefono.insert(0, telefono_actual)
        entry_telefono.pack(pady=5)

        def guardar_cambios():
            nuevo_nombre = entry_nombre.get().strip()
            nuevo_telefono = entry_telefono.get().strip()

            if not nuevo_nombre or not nuevo_telefono:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            actualizar_cliente(self.connection, int(id_cliente), nuevo_nombre, nuevo_telefono)

            ventana.destroy()

            # Recargar tabla
            for fila in tree.get_children():
                tree.delete(fila)

            clientes = obtener_clientes(self.connection)
            for cliente in clientes:
                tree.insert("", tk.END, values=cliente)

            messagebox.showinfo("Éxito", "Cliente actualizado.")

        tk.Button(ventana, text="Guardar Cambios", command=guardar_cambios).pack(pady=15)

    def eliminar_cliente(self, tree):
        seleccion = tree.selection()

        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un cliente.")
            return

        valores = tree.item(seleccion[0], "values")
        id_cliente = valores[0]

        confirmacion = messagebox.askyesno(
            "Confirmar",
            f"¿Eliminar cliente ID {id_cliente}?"
        )

        if confirmacion:
            eliminar_cliente(self.connection, int(id_cliente))

            # Recargar tabla
            for fila in tree.get_children():
                tree.delete(fila)

            clientes = obtener_clientes(self.connection)
            for cliente in clientes:
                tree.insert("", tk.END, values=cliente)

            messagebox.showinfo("Éxito", "Cliente eliminado.")