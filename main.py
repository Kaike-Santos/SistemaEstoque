# main.py
# Ponto de entrada: menu principal e fluxo de navegação.

import sys

import arquivos
import logs
import ui
from estoque import Estoque
from produto import Produto

estoque = Estoque()


# ======================================================================
# Inicialização
# ======================================================================

def inicializar() -> None:
    """Carrega dados do JSON ao iniciar."""
    produtos = arquivos.carregar_produtos()
    estoque.carregar_lista(produtos)
    logs.registrar("SISTEMA", "Inicializado")


# ======================================================================
# Ações de produto
# ======================================================================

def acao_cadastrar() -> None:
    ui.cabecalho("Cadastrar Produto")
    try:
        codigo = Produto.validar_codigo(ui.ler_texto("Código"))
        nome = Produto.validar_nome(ui.ler_texto("Nome"))
        categoria = Produto.validar_categoria(ui.ler_texto("Categoria"))
        preco = Produto.validar_preco(ui.ler_float("Preço (R$)"))
        quantidade = Produto.validar_quantidade(ui.ler_int("Quantidade"))

        produto = Produto(codigo, nome, categoria, preco, quantidade)
        estoque.cadastrar(produto)
        arquivos.salvar_produtos(estoque.listar_nao_ordenado())
        logs.registrar("CADASTRO", f"Produto {codigo} - {nome}")
        ui.sucesso(f"Produto '{nome}' cadastrado com sucesso!")
    except ValueError as e:
        ui.erro(str(e))
    ui.pausar()


def acao_editar() -> None:
    ui.cabecalho("Editar Produto")
    try:
        codigo = ui.ler_texto("Código do produto")
        ui.info("Deixe em branco para manter o valor atual.")

        nome = ui.ler_texto("Novo nome", obrigatorio=False) or None
        categoria = ui.ler_texto("Nova categoria", obrigatorio=False) or None

        preco_str = ui.ler_texto("Novo preço", obrigatorio=False)
        preco = Produto.validar_preco(preco_str) if preco_str else None

        qtd_str = ui.ler_texto("Nova quantidade", obrigatorio=False)
        quantidade = Produto.validar_quantidade(qtd_str) if qtd_str else None

        produto = estoque.editar(codigo, nome, categoria, preco, quantidade)
        arquivos.salvar_produtos(estoque.listar_nao_ordenado())
        logs.registrar("EDICAO", f"Produto {codigo}")
        ui.sucesso(f"Produto '{produto.nome}' atualizado!")
    except ValueError as e:
        ui.erro(str(e))
    ui.pausar()


def acao_remover() -> None:
    ui.cabecalho("Remover Produto")
    try:
        codigo = ui.ler_texto("Código do produto")
        estoque.remover(codigo)
        arquivos.salvar_produtos(estoque.listar_nao_ordenado())
        logs.registrar("REMOCAO", f"Produto {codigo}")
        ui.sucesso(f"Produto '{codigo}' removido.")
    except ValueError as e:
        ui.erro(str(e))
    ui.pausar()