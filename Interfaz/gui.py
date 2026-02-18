# Dependencias necesarias para la interfaz gráfica
import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox

# Funciones para manejar la conexión a la base de datos y la logica de las operaciones CRUD
from Database.config_privada import get_connection
from Funciones.cliente import *

# Vistas específicas para cada sección (clientes, servicios, órdenes)
from Interfaz.Vistas.clientes_view import ClientesView
# from Interfaz.Vistas.servicios_view import ServiciosView
# from Interfaz.Vistas.ordenes_view import OrdenesView

# Configuración el tema visual de la aplicación
ctk.set_appearance_mode("System")  # Modos: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue") # Temas: "blue" (standard), "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión")
        self.geometry("400x300")

        # Intentar establecer conexión
        try:
            self.connection = get_connection()
        except Exception as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos: {e}")
            self.connection = None

        self.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

        self.vista_clientes = ClientesView(self, self.connection)

        # Menú Principal
        self.label = ctk.CTkLabel(self, text="Menú Principal", font=("Roboto", 24, "bold"))
        self.label.pack(pady=20)

        # Botones principales
        self.btn_clientes = ctk.CTkButton(self, text="Gestion de Clientes", width=250, height=40, command=self.vista_clientes.abrir_gestion)
        self.btn_clientes.pack(pady=20)

        self.btn_clientes = ctk.CTkButton(self, text="Gestion deServicios", width=250, height=40, fg_color="gray")
        self.btn_clientes.pack(pady=10)

        self.btn_clientes = ctk.CTkButton(self, text="Órdenes de Trabajo", width=250, height=40, fg_color="gray")
        self.btn_clientes.pack(pady=10)

    def cerrar_aplicacion(self):
        if self.connection:
            self.connection.close()
        self.destroy()