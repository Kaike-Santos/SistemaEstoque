# produto.py
# Classe Produto com validações de negócio.


class Produto:
    """Representa um produto no sistema de estoque."""

    def __init__(
        self,
        codigo: str,
        nome: str,
        categoria: str,
        preco: float,
        quantidade: int,
    ) -> None:
        self.codigo = codigo
        self.nome = nome
        self.categoria = categoria
        self.preco = preco
        self.quantidade = quantidade

    # Validações
    
    @staticmethod
    def validar_codigo(codigo: str) -> str:
        """Garante que o código não seja vazio."""
        codigo = codigo.strip()
        if not codigo:
            raise ValueError("Código não pode ser vazio.")
        return codigo

    @staticmethod
    def validar_nome(nome: str) -> str:
        nome = nome.strip()
        if not nome:
            raise ValueError("Nome não pode ser vazio.")
        return nome

    @staticmethod
    def validar_categoria(categoria: str) -> str:
        categoria = categoria.strip()
        if not categoria:
            raise ValueError("Categoria não pode ser vazia.")
        return categoria

    @staticmethod
    def validar_preco(valor: str | float) -> float:
        try:
            preco = float(valor)
        except (ValueError, TypeError):
            raise ValueError("Preço deve ser um número.")
        if preco <= 0:
            raise ValueError("Preço deve ser positivo.")
        return round(preco, 2)

    @staticmethod
    def validar_quantidade(valor: str | int) -> int:
        try:
            quantidade = int(valor)
        except (ValueError, TypeError):
            raise ValueError("Quantidade deve ser um número inteiro.")
        if quantidade < 0:
            raise ValueError("Quantidade não pode ser negativa.")
        return quantidade

    # Serialização
    
    def para_dict(self) -> dict:
        """Converte o produto para dicionário (usado na persistência JSON)."""
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "categoria": self.categoria,
            "preco": self.preco,
            "quantidade": self.quantidade,
        }

    @classmethod
    def de_dict(cls, dados: dict) -> "Produto":
        """Cria um Produto a partir de um dicionário."""
        return cls(
            codigo=dados["codigo"],
            nome=dados["nome"],
            categoria=dados["categoria"],
            preco=float(dados["preco"]),
            quantidade=int(dados["quantidade"]),
        )

    # Representação
    
    def __repr__(self) -> str:
        return (
            f"Produto(codigo={self.codigo!r}, nome={self.nome!r}, "
            f"categoria={self.categoria!r}, preco={self.preco}, "
            f"quantidade={self.quantidade})"
        )

    def __str__(self) -> str:
        return (
            f"[{self.codigo}] {self.nome} | {self.categoria} | "
            f"R$ {self.preco:.2f} | Qtd: {self.quantidade}"
        )