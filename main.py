import tkinter as tk
from tkinter import messagebox, ttk


class ClinicaApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Sistema de Gerenciamento de Senhas - Clínica")
    self.root.geometry("600x400")

    # Configuração inicial da interface
    self.criar_componentes()

  def criar_componentes(self):
    # Título
    titulo = tk.Label(
        self.root, text="Clínica Médica - Controle de Senhas", font=("Arial", 14, "bold")
    )
    titulo.pack(pady=20)

    # Botão de teste / exemplo
    btn_acao = tk.Button(
        self.root,
        text="Emitir Senha (Exemplo)",
        font=("Arial", 11),
        command=self.acao_exemplo,
    )
    btn_acao.pack(pady=10)

  def acao_exemplo(self):
    # Aqui será implementado a lógica das filas e emissão nos próximos passos
    messagebox.showinfo("Aviso", "Funcionalidade em desenvolvimento!")


if __name__ == "__main__":
  root = tk.Tk()
  app = ClinicaApp(root)
  root.mainloop()
