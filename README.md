# Sistema de Estoque e Vendas

Sistema de linha de comando para controle de produtos, vendas e relatórios,
desenvolvido em Python puro como projeto acadêmico.

## Autores 

Kaike Machado 
Esther Santos
Maria Eduarda Gobira
João Nelson 
Gabriel dos Anjos 
Henrique Silva 

## Requisitos

- Python 3.10+
- Sem dependências externas

## Como executar

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/sistema-estoque.git
cd sistema-estoque

# Execute
python main.py

# Para carregar os dados de exemplo, copie o arquivo:
cp dados/exemplo.json dados/estoque.json
python main.py
```

## Funcionalidades

| # | Funcionalidade |
|---|---|
| 1 | Cadastrar produto (código único) |
| 2 | Editar produto |
| 3 | Remover produto |
| 4 | Buscar por código (busca binária) |
| 5 | Buscar por nome (busca linear) |
| 6 | Registrar venda com validação de estoque |
| 7 | Listar todos ordenados por código |
| 8 | Listar por categoria |
| 9 | Relatório de estoque baixo |
| 10 | Ver log de operações |

## Estrutura de arquivos

```
sistema-estoque/
├── main.py       # Menu e fluxo principal
├── produto.py    # Classe Produto e validações
├── estoque.py    # Dois vetores + buscas
├── arquivos.py   # Persistência JSON
├── logs.py       # Log de operações
├── ui.py         # Terminal e paginação
└── dados/
    ├── estoque.json      # Dados (gerado automaticamente)
    ├── operacoes.log     # Log (gerado automaticamente)
    └── exemplo.json      # Dados de exemplo
```

## Relatório de complexidade

### Estrutura de dados

O sistema mantém **dois vetores simultâneos** do mesmo conjunto de produtos:

| Vetor | Ordem | Finalidade |
|---|---|---|
| `_produtos` | Não ordenado | Cadastro rápido O(1), busca por nome |
| `_ordenado` | Ordenado por código | Busca binária O(log n) |

### Análise de complexidade

| Operação | Complexidade | Justificativa |
|---|---|---|
| Cadastrar | O(n) | Inserção ordenada percorre o vetor |
| Remover | O(n) | Percorre ambos os vetores |
| Busca por código | **O(log n)** | Busca binária no vetor ordenado |
| Busca por nome | O(n) | Busca linear — vetor não ordenado por nome |
| Listar ordenado | O(1) | Vetor já mantido ordenado |
| Relatório categoria | O(n) | Filtro linear |
| Estoque baixo | O(n) | Filtro linear |

### Por que busca binária para código?

Códigos são identificadores únicos e o vetor é mantido ordenado por eles
a cada inserção/remoção. Isso permite usar busca binária, reduzindo de
O(n) para O(log n) — em um estoque com 1000 produtos, são no máximo
10 comparações em vez de 1000.

### Por que busca linear para nome?

Nomes não são únicos e o vetor não está ordenado por nome. Seria necessário
um segundo índice ordenado por nome para usar busca binária, o que aumentaria
o custo de memória e manutenção. Para o escopo deste sistema, O(n) é aceitável.