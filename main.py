import tkinter as tk

from filas import GerenciadorFilas
from tela import TelaClinica


def main():
    root = tk.Tk()
    gerenciador = GerenciadorFilas()
    TelaClinica(root, gerenciador=gerenciador)
    root.mainloop()


if _name_ == "_main_":
    main()
