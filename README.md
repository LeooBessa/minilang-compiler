# MiniLang Compiler

Compilador didático para uma linguagem matemática simples, com interface gráfica feita em Python + Flet. O projeto foi criado para demonstrar as etapas clássicas de um compilador: análise léxica, sintática, semântica, geração de código intermediário e execução.

---

## O que é a MiniLang?

MiniLang é uma linguagem minimalista que suporta atribuição de variáveis, operações matemáticas e impressão de resultados. Exemplo:

```
x = 10
y = 2
z = x * y
w = z - 5
res = w / 3
print(res)
```

**Operadores suportados:** `+` `-` `*` `/`

---

## Como o compilador funciona

O código passa por 5 etapas:

```
Código fonte → Lexer → Parser → Semântico → Código intermediário → Execução
```

| Etapa | O que faz |
|---|---|
| Lexer | Quebra o código em tokens (palavras, números, operadores) |
| Parser | Verifica se a estrutura das linhas é válida |
| Semântico | Garante que variáveis são declaradas antes de serem usadas |
| Código intermediário | Gera instruções simples (LOAD, ADD, STORE...) |
| Execução | Roda as instruções e produz o resultado |

---

## Pré-requisitos

Escolha uma das duas formas de rodar: com Docker ou com Python local.

### Com Docker (recomendado)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado

### Com Python local
- Python 3.11 ou superior
- pip

---

## Rodando com Docker

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/compilador.git
cd compilador

# 2. Suba o container
docker compose up --build
```

Acesse no navegador:
```
http://localhost:8080
```

Para parar:
```bash
docker compose down
```

---

## Rodando localmente (sem Docker)

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/compilador.git
cd compilador

# 2. Crie e ative o ambiente virtual
python -m venv .venv

# Linux/Mac:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Rode o projeto
python app.py
```

Uma janela desktop vai abrir com a interface do compilador.

---

## Como testar

Com a interface aberta, você pode usar o código de exemplo já preenchido ou escrever o seu próprio. Clique em **Compilar** e veja:

- **Tokens** gerados pelo léxer
- **Código intermediário** (assembly simplificado)
- **Resultado** da execução
- **Erros** sintáticos ou semânticos, caso existam

### Exemplos para testar

**Operações básicas:**
```
x = 10
y = 3
z = x + y
print(z)
```

**Erro semântico (variável não declarada):**
```
print(w)
```

**Múltiplas operações:**
```
a = 100
b = 4
c = a / b
d = c - 5
print(d)
```

---

## Estrutura do projeto

```
compilador/
├── compilador.py        # Pipeline do compilador (lexer, parser, semântico, execução)
├── app.py               # Interface gráfica com Flet
├── requirements.txt     # Dependências Python
├── Dockerfile           # Imagem Docker
├── docker-compose.yml   # Orquestração do container
└── images/
    └── afd_lexer.png    # Autômato finito do lexer (gerado no JFLAP)
```

---

## Tecnologias usadas

- **Python 3.11**
- **Flet** — interface gráfica multiplataforma (Flutter + Python)
- **Docker** — containerização para rodar em qualquer plataforma
- **JFLAP** — modelagem do autômato finito do lexer

---

## Autômato do Lexer (AFD)

O lexer foi modelado como um Autômato Finito Determinístico. Cada token da linguagem corresponde a um estado final do autômato.


---

## Licença

Este projeto foi desenvolvido para fins educacionais.
