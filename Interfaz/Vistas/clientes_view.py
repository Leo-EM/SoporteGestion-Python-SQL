import customtkinter as ctk
from tkinter import messagebox, ttk
from Funciones.cliente import *

class ClientesView:
    def __init__(self, parent, connection):
        self.parent = parent
        self.connection = connection

    def abrir_gestion(self):
        ventana = ctk.CTkToplevel(self.parent)
        ventana.title("Gestión de Clientes")
        ventana.geometry("400x300")
        ventana.after(100, ventana.lift)
        ventana.attributes("-topmost", True)

        ctk.CTkButton(ventana, text="Mostrar Clientes", command=self.mostrar_todos).pack(pady=10)
        ctk.CTkButton(ventana, text="Agregar Cliente", command=self.agregar_nuevo).pack(pady=10)
        # Aquí irán los futuros botones de eliminar/actualizar

    def mostrar_todos(self):
        self.configurar_estilo_tabla() # Aplicamos el estilo
            
        ventana = ctk.CTkToplevel(self.parent)
        ventana.title("Base de Datos de Clientes")
        ventana.geometry("700x450")
        ventana.after(100, ventana.lift)
        ventana.attributes("-topmost", True)

        # Contenedor principal
        frame = ctk.CTkFrame(ventana)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Registros Actuales", font=("Roboto", 20, "bold")).pack(pady=10)

        # Crear el Treeview
        columnas = ("ID", "Nombre", "Contacto")
        tree = ttk.Treeview(frame, columns=columnas, show="headings", style="Treeview")
            
        # Definir encabezados
        tree.heading("ID", text="ID Cliente")
        tree.heading("Nombre", text="Nombre y Apellido")
        tree.heading("Contacto", text="Teléfono / Email")

        # Ajustar ancho de columnas
        tree.column("ID", width=80, anchor="center")
        tree.column("Nombre", width=250)
        tree.column("Contacto", width=200)

        # Scrollbar moderna
        scrollbar = ctk.CTkScrollbar(frame, orientation="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        # Empaquetado de tabla y scroll
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Cargar datos desde PostgreSQL
        try:
            clientes = obtener_clientes(self.connection) # Tu función en cliente.py
            for cliente in clientes:
                # cliente es una tupla: (id_cliente, nombre, contacto)
                tree.insert("", "end", values=cliente)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {e}")

        # Botón para cerrar
        ctk.CTkButton(ventana, text="Cerrar Vista", command=ventana.destroy).pack(pady=10)
        

    def agregar_nuevo(self):
        # CTkToplevel para ventanas emergentes
        ventana = ctk.CTkToplevel(self.parent)
        ventana.title("Nuevo Registro de Cliente")
        ventana.geometry("350x300")
            
        # Aseguramos que la ventana esté por encima de la principal
        ventana.after(100, ventana.lift) 
        ventana.attributes("-topmost", True)

        # Contenedor con padding
        frame = ctk.CTkFrame(ventana)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Nombre Completo:", font=("Roboto", 12)).pack(pady=(10, 0))
        entry_nombre = ctk.CTkEntry(frame, width=200, placeholder_text="Ej: Leonardo Corales")
        entry_nombre.pack(pady=5)

        ctk.CTkLabel(frame, text="Teléfono / Contacto:", font=("Roboto", 12)).pack(pady=(10, 0))
        entry_telefono = ctk.CTkEntry(frame, width=200, placeholder_text="Ej: 1123456789")
        entry_telefono.pack(pady=5)

        def guardar():
            nombre = entry_nombre.get().strip()
            telefono = entry_telefono.get().strip()

            if nombre and telefono:
                try:
                    insertar_cliente(self.connection, nombre, telefono)
                    messagebox.showinfo("Éxito", f"Cliente {nombre} guardado.")
                    ventana.destroy() # Cerramos al terminar
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo guardar en la base de datos: {e}")
                else:
                    messagebox.showwarning("Atención", "Todos los campos son obligatorios.")

            ctk.CTkButton(frame, text="Confirmar Registro", command=guardar).pack(pady=20)
        

    def configurar_estilo_tabla(self):
            style = ttk.Style()
            style.theme_use("default") # Base para poder personalizar
            
            # Configuración de colores para modo oscuro
            style.configure("Treeview",
                background="#2b2b2b",
                foreground="white",
                rowheight=25,
                fieldbackground="#2b2b2b",
                bordercolor="#2b2b2b",
                borderwidth=0)
            
            style.map('Treeview', background=[('selected', '#1f538d')]) # Color al seleccionar fila
            
            style.configure("Treeview.Heading",
                background="#333333",
                foreground="white",
                relief="flat",
                font=("Roboto", 10, "bold"))