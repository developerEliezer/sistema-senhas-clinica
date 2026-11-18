from collections import deque


class GerenciadorFilas:

  def __init__(self):
    self.especialidades = ["Clínica Geral", "Cardiologia", "Ortopedia"]

    # Estrutura inicial das filas FIFO vazias
    self.filas = {
        "Clínica Geral": {"Normal": deque(), "Preferencial": deque()},
        "Cardiologia": {"Normal": deque(), "Preferencial": deque()},
        "Ortopedia": {"Normal": deque(), "Preferencial": deque()},
    }

  def emitir_senha(self, especialidade, categoria):
    # A implementar: gerar código (N001/P001) e dar append na fila
    pass

  def chamar_proxima_senha(self, especialidade):
    # A implementar: verificar fila Preferencial primeiro, depois Normal (popleft)
    pass
