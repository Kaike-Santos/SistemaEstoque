# arquivos.py
# Responsável por persistir e carregar dados em JSON.

import json
import os
from produto import Produto

CAMINHO_DADOS = os.path.join("dados", "estoque.json")


def salvar_produtos(produtos: list[Produto]) -> None:
    """Serializa a lista de produtos e salva no arquivo JSON."""
    os.makedirs("dados", exist_ok=True)
    with open(CAMINHO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(
            [p.para_dict() for p in produtos],
            arquivo,
            ensure_ascii=False,
            indent=2,
        )


def carregar_produtos() -> list[Produto]:
    """Lê o arquivo JSON e retorna lista de Produtos. Retorna [] se não existir."""
    if not os.path.exists(CAMINHO_DADOS):
        return []
    with open(CAMINHO_DADOS, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    return [Produto.de_dict(d) for d in dados]