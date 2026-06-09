# logs.py
# Registra operações com data/hora em arquivo de texto.

import os
from datetime import datetime

CAMINHO_LOG = os.path.join("dados", "operacoes.log")


def _agora() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def registrar(operacao: str, detalhe: str = "") -> None:
    """Grava uma linha de log no arquivo."""
    os.makedirs("dados", exist_ok=True)
    linha = f"[{_agora()}] {operacao}"
    if detalhe:
        linha += f" | {detalhe}"
    with open(CAMINHO_LOG, "a", encoding="utf-8") as arquivo:
        arquivo.write(linha + "\n")


def exibir_ultimos(n: int = 10) -> None:
    """Imprime as últimas n linhas do log no terminal."""
    if not os.path.exists(CAMINHO_LOG):
        print("Nenhum log registrado ainda.")
        return
    with open(CAMINHO_LOG, "r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()
    ultimas = linhas[-n:]
    print(f"\n--- Últimas {len(ultimas)} operações ---")
    for linha in ultimas:
        print(linha, end="")
    print()