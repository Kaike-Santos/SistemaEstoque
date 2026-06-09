# ui.py
# Utilitários de terminal: menus, paginação e leitura de entradas.

from produto import Produto

LINHA = "─" * 60


def cabecalho(titulo: str) -> None:
    print(f"\n{LINHA}")
    print(f"  {titulo.upper()}")
    print(LINHA)


def sucesso(msg: str) -> None:
    print(f"\n  ✔  {msg}")


def erro(msg: str) -> None:
    print(f"\n  ✖  Erro: {msg}")


def info(msg: str) -> None:
    print(f"\n  ℹ  {msg}")


def pausar() -> None:
    input("\n  Pressione Enter para continuar...")


def ler_texto(prompt: str, obrigatorio: bool = True) -> str:
    """Lê string do terminal com validação de campo obrigatório."""
    while True:
        valor = input(f"  {prompt}: ").strip()
        if valor or not obrigatorio:
            return valor
        erro("Campo obrigatório.")


def ler_float(prompt: str) -> float:
    """Lê float do terminal com tratamento de erro."""
    while True:
        try:
            return float(input(f"  {prompt}: ").replace(",", "."))
        except ValueError:
            erro("Digite um número válido (ex: 19.90).")


def ler_int(prompt: str) -> int:
    """Lê inteiro do terminal com tratamento de erro."""
    while True:
        try:
            return int(input(f"  {prompt}: "))
        except ValueError:
            erro("Digite um número inteiro válido.")


def formatar_produto(p: Produto) -> str:
    return (
        f"  [{p.codigo}] {p.nome:<25} | {p.categoria:<15} | "
        f"R$ {p.preco:>8.2f} | Qtd: {p.quantidade}"
    )


def paginar(itens: list, tamanho: int = 10) -> None:
    """Exibe lista com paginação simples."""
    if not itens:
        info("Nenhum item para exibir.")
        return

    total = len(itens)
    inicio = 0

    while inicio < total:
        fim = min(inicio + tamanho, total)
        for item in itens[inicio:fim]:
            if isinstance(item, Produto):
                print(formatar_produto(item))
            else:
                print(f"  {item}")

        print(f"\n  Exibindo {fim} de {total}")

        if fim >= total:
            break

        opcao = input("  [Enter] próxima página | [s] sair: ").strip().lower()
        if opcao == "s":
            break
        inicio = fim