# estoque.py
# Gerencia dois vetores:
#   - _produtos: lista não ordenada (inserção rápida, busca linear por nome)
#   - _ordenado: lista ordenada por código (busca binária)
#
# Complexidade:
#   Inserção no vetor não ordenado → O(1) amortizado
#   Inserção no vetor ordenado     → O(n) para manter ordem
#   Busca linear por nome          → O(n)
#   Busca binária por código       → O(log n)
#   Remoção                        → O(n) em ambos os vetores

from produto import Produto


class Estoque:
    def __init__(self) -> None:
        # Vetor não ordenado — ordem de cadastro
        self._produtos: list[Produto] = []
        # Vetor ordenado por código — mantido sempre ordenado
        self._ordenado: list[Produto] = []

    # ------------------------------------------------------------------
    # Cadastro
    # ------------------------------------------------------------------

    def cadastrar(self, produto: Produto) -> None:
        """
        Adiciona produto ao sistema.
        - Vetor não ordenado: append → O(1)
        - Vetor ordenado: inserção na posição correta → O(n)
        Lança ValueError se código já existir.
        """
        if self._buscar_indice_ordenado(produto.codigo) >= 0:
            raise ValueError(f"Código '{produto.codigo}' já cadastrado.")
        self._produtos.append(produto)
        self._inserir_ordenado(produto)

    def _inserir_ordenado(self, produto: Produto) -> None:
        """Insere mantendo o vetor ordenado por código (O(n))."""
        posicao = 0
        for i, p in enumerate(self._ordenado):
            if produto.codigo < p.codigo:
                posicao = i
                break
            posicao = i + 1
        self._ordenado.insert(posicao, produto)

    # ------------------------------------------------------------------
    # Remoção
    # ------------------------------------------------------------------

    def remover(self, codigo: str) -> Produto:
        """
        Remove produto pelo código dos dois vetores → O(n).
        Lança ValueError se não encontrado.
        """
        # Remove do vetor não ordenado
        for i, p in enumerate(self._produtos):
            if p.codigo == codigo:
                self._produtos.pop(i)
                break
        else:
            raise ValueError(f"Produto '{codigo}' não encontrado.")

        # Remove do vetor ordenado
        idx = self._buscar_indice_ordenado(codigo)
        if idx >= 0:
            self._ordenado.pop(idx)

        return self._produtos  # retorna estado atualizado

    # ------------------------------------------------------------------
    # Getters
    # ------------------------------------------------------------------

    def listar_nao_ordenado(self) -> list[Produto]:
        return list(self._produtos)

    def listar_ordenado(self) -> list[Produto]:
        return list(self._ordenado)

    def total(self) -> int:
        return len(self._produtos)
    

    # ------------------------------------------------------------------
    # Busca binária por código — O(log n)
    # ------------------------------------------------------------------

    def _buscar_indice_ordenado(self, codigo: str) -> int:
        """
        Busca binária no vetor ordenado por código.
        Retorna o índice se encontrado, -1 caso contrário.
        Complexidade: O(log n)
        """
        esquerda, direita = 0, len(self._ordenado) - 1
        while esquerda <= direita:
            meio = (esquerda + direita) // 2
            codigo_meio = self._ordenado[meio].codigo
            if codigo_meio == codigo:
                return meio
            if codigo_meio < codigo:
                esquerda = meio + 1
            else:
                direita = meio - 1
        return -1

    def buscar_por_codigo(self, codigo: str) -> Produto:
        """
        Busca produto pelo código usando busca binária → O(log n).
        Lança ValueError se não encontrado.
        """
        idx = self._buscar_indice_ordenado(codigo)
        if idx < 0:
            raise ValueError(f"Produto '{codigo}' não encontrado.")
        return self._ordenado[idx]
    

    # ------------------------------------------------------------------
    # Busca linear por nome — O(n)
    # ------------------------------------------------------------------

    def buscar_por_nome(self, termo: str) -> list[Produto]:
        """
        Busca linear no vetor não ordenado por nome (parcial, case-insensitive).
        Complexidade: O(n) — necessário pois o vetor não está ordenado por nome.
        """
        termo = termo.strip().lower()
        return [p for p in self._produtos if termo in p.nome.lower()]

        # ------------------------------------------------------------------
    # Edição
    # ------------------------------------------------------------------

    def editar(
        self,
        codigo: str,
        nome: str | None = None,
        categoria: str | None = None,
        preco: float | None = None,
        quantidade: int | None = None,
    ) -> Produto:
        """
        Edita campos do produto localizado por código.
        Usa busca binária para encontrar o produto → O(log n).
        """
        produto = self.buscar_por_codigo(codigo)

        if nome is not None:
            produto.nome = Produto.validar_nome(nome)
        if categoria is not None:
            produto.categoria = Produto.validar_categoria(categoria)
        if preco is not None:
            produto.preco = Produto.validar_preco(preco)
        if quantidade is not None:
            produto.quantidade = Produto.validar_quantidade(quantidade)

        return produto
    
    # ------------------------------------------------------------------
    # Vendas
    # ------------------------------------------------------------------

    def registrar_venda(self, codigo: str, quantidade: int) -> dict:
        """
        Reduz o estoque ao registrar uma venda.
        Valida disponibilidade antes de confirmar.
        Complexidade: O(log n) pela busca binária.
        """
        if quantidade <= 0:
            raise ValueError("Quantidade vendida deve ser maior que zero.")

        produto = self.buscar_por_codigo(codigo)

        if produto.quantidade < quantidade:
            raise ValueError(
                f"Estoque insuficiente. Disponível: {produto.quantidade}."
            )

        produto.quantidade -= quantidade

        return {
            "codigo": produto.codigo,
            "nome": produto.nome,
            "quantidade_vendida": quantidade,
            "estoque_restante": produto.quantidade,
            "total": round(produto.preco * quantidade, 2),
        }
    
    # ------------------------------------------------------------------
    # Relatórios
    # ------------------------------------------------------------------

    def listar_por_categoria(self, categoria: str) -> list[Produto]:
        """Filtra produtos pela categoria (case-insensitive) → O(n)."""
        categoria = categoria.strip().lower()
        return [p for p in self._produtos if p.categoria.lower() == categoria]

    def estoque_baixo(self, limite: int = 5) -> list[Produto]:
        """Retorna produtos com quantidade abaixo do limite → O(n)."""
        return [p for p in self._produtos if p.quantidade < limite]

    def categorias(self) -> list[str]:
        """Retorna lista de categorias únicas cadastradas."""
        return sorted({p.categoria for p in self._produtos})

    def carregar_lista(self, produtos: list[Produto]) -> None:
        """Popula os dois vetores a partir de uma lista (usado no carregamento do JSON)."""
        self._produtos.clear()
        self._ordenado.clear()
        for p in produtos:
            self._produtos.append(p)
            self._inserir_ordenado(p)

            # ------------------------------------------------------------------
    # Vendas
    # ------------------------------------------------------------------

    def registrar_venda(self, codigo: str, quantidade: int) -> dict:
        """
        Reduz o estoque ao registrar uma venda.
        Valida disponibilidade antes de confirmar.
        Complexidade: O(log n) pela busca binária.
        """
        if quantidade <= 0:
            raise ValueError("Quantidade vendida deve ser maior que zero.")

        produto = self.buscar_por_codigo(codigo)

        if produto.quantidade < quantidade:
            raise ValueError(
                f"Estoque insuficiente. Disponível: {produto.quantidade}."
            )

        produto.quantidade -= quantidade

        return {
            "codigo": produto.codigo,
            "nome": produto.nome,
            "quantidade_vendida": quantidade,
            "estoque_restante": produto.quantidade,
            "total": round(produto.preco * quantidade, 2),
        }