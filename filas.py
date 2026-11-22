from collections import deque
from datetime import datetime


class ErroFila(Exception):
    pass


class Senha:
    def __init__(self, codigo, especialidade, categoria, hora):
        self.codigo = codigo
        self.especialidade = especialidade
        self.categoria = categoria
        self.hora = hora

    def __str__(self):
        return f"[{self.codigo}] {self.especialidade} - {self.categoria} ({self.hora})"


class GerenciadorFilas:
    ESPECIALIDADES = {
        "Clínica Geral": "CG",
        "Cardiologia": "CA",
        "Ortopedia": "OR",
    }
    MINUTOS_POR_PACIENTE = 30

    def __init__(self):
        self.filas_preferenciais = {}
        self.filas_normais = {}
        self.contadores = {}

        for nome_esp in self.ESPECIALIDADES:
            self.filas_preferenciais[nome_esp] = deque()
            self.filas_normais[nome_esp] = deque()
            self.contadores[nome_esp] = {"Preferencial": 0, "Normal": 0}

        self.historico = []
        self.ultima_chamada = None

    def _checar_entradas(self, especialidade, categoria=None):
        if especialidade not in self.ESPECIALIDADES:
            raise ErroFila(f"Especialidade inválida: {especialidade}")

        if categoria is not None and categoria not in ("Preferencial", "Normal"):
            raise ErroFila(f"Categoria inválida: {categoria}")

    def _montar_codigo(self, especialidade, categoria):
        self.contadores[especialidade][categoria] += 1
        seq = self.contadores[especialidade][categoria]

        sigla = self.ESPECIALIDADES[especialidade]
        tipo = "P" if categoria == "Preferencial" else "N"
        return f"{sigla}-{tipo}{seq:03d}"

    def tempo_espera(self, especialidade, categoria):
        self._checar_entradas(especialidade, categoria)

        qtd_pref = len(self.filas_preferenciais[especialidade])
        qtd_norm = len(self.filas_normais[especialidade])

        # Preferenciais têm prioridade sobre normais; dentro de cada categoria vale FIFO
        if categoria == "Preferencial":
            pessoas_antes = qtd_pref
        else:
            pessoas_antes = qtd_pref + qtd_norm

        return pessoas_antes * self.MINUTOS_POR_PACIENTE

    def emitir_senha(self, especialidade, categoria):
        self._checar_entradas(especialidade, categoria)

        estimativa = self.tempo_espera(especialidade, categoria)
        codigo = self._montar_codigo(especialidade, categoria)
        agora = datetime.now().strftime("%H:%M:%S")

        senha = Senha(codigo, especialidade, categoria, agora)

        if categoria == "Preferencial":
            self.filas_preferenciais[especialidade].append(senha)
        else:
            self.filas_normais[especialidade].append(senha)

        return senha, estimativa

    def chamar_proxima(self, especialidade):
        self._checar_entradas(especialidade)

        fila_p = self.filas_preferenciais[especialidade]
        fila_n = self.filas_normais[especialidade]

        if fila_p:
            proxima = fila_p.popleft()
        elif fila_n:
            proxima = fila_n.popleft()
        else:
            raise ErroFila(f"Fila vazia para {especialidade}. Nenhum paciente aguardando.")

        self.ultima_chamada = proxima
        self.historico.append(proxima)
        return proxima

    def ver_fila(self, especialidade):
        self._checar_entradas(especialidade)

        lista_p = list(self.filas_preferenciais[especialidade])
        lista_n = list(self.filas_normais[especialidade])
        ordem_chamada = lista_p + lista_n

        return {
            "total": len(ordem_chamada),
            "preferenciais": len(lista_p),
            "normais": len(lista_n),
            "senhas": ordem_chamada,
        }

    def ver_historico(self):
        return list(self.historico)


if __name__ == "__main__":
    gf = GerenciadorFilas()

    n1, e1 = gf.emitir_senha("Cardiologia", "Normal")
    n2, e2 = gf.emitir_senha("Cardiologia", "Normal")
    p1, e3 = gf.emitir_senha("Cardiologia", "Preferencial")

    print(f"Emitida: {n1} | Espera: {e1} min")
    print(f"Emitida: {n2} | Espera: {e2} min")
    print(f"Emitida: {p1} | Espera: {e3} min")

    print("1ª chamada (esperado CA-P001):", gf.chamar_proxima("Cardiologia"))
    print("2ª chamada (esperado CA-N001):", gf.chamar_proxima("Cardiologia"))
    print("3ª chamada (esperado CA-N002):", gf.chamar_proxima("Cardiologia"))

    try:
        gf.chamar_proxima("Cardiologia")
    except ErroFila as erro:
        print("Teste fila vazia OK:", erro)
