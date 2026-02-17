# Funciones para manejar la conexión a la base de datos y operaciones CRUD
from Interfaz.gui import *
from Interfaz.consola import *
from Funciones.cliente import *

# Para la interfaz gráfica
import tkinter as tk

# El bloque principal del programa
def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()