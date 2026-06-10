import re
from io import StringIO

# Função auxilixar para agruprar os tokens de acordo com suas linhas lógicas
def separar_por_linhas(tokens):
    linhas = []
    atual = []
    for tipo, valor in tokens:
        if tipo == 'NEWLINE':
            if atual: 
                linhas.append(atual)
                atual = []
        else:
            atual.append((tipo, valor))
    if atual: linhas.append(atual)
    return linhas

# 1. ANÁLISE LÉXICA (LEXER)
# Teoria: linguagens regulares (tipo 3 da hierarquia de chomsky) e autômatos finitos

# A análise léxica é fundamentada na teoria dos Autômatos Finitos
# Cada padrão de token (número, identificador, operador) corresponde
# uma Expressão Regular, que por sua vez é equivalente a um AFD.

def lexer(codigo):
    tokens = []
    # Expressões regulares são a representação algébrica das linguagens regulares
    # O módulo 're' compila essa string em um autômato finito (AFD/AFN)
    regex = r'(?P<PRINT>print)|(?P<ID>[a-zA-Z_]\w*)|(?P<NUM>\d+)|(?P<PLUS>\+)|(?P<MINUS>-)|(?P<MULT>\*)|(?P<DIV>/)|(?P<ASSIGN>=)|(?P<LPAREN>\()|(?P<RPAREN>\))|(?P<NEWLINE>\n)|(?P<SKIP>[ \t]+)'

    # O autômato finito "consome" a string caractere por caractere
    # Quando atinge um estado de aceitação, ele gera a saida conrespondente (um token)
    for match in re.finditer(regex, codigo):
        tipo = match.lastgroup
        valor = match.group()
        if tipo == 'SKIP': continue
        tokens.append((tipo, valor))
    return tokens

# 2. ANÁLISE SINTÁTICA (PARSER)
# Teoria: linguagens livres de contexto (tipo 2) e autômatos com pilha (PDA)
def parser(tokens):
    linhas = separar_por_linhas(tokens)
    for linha in linhas:
        if not linha: continue
        primeiro_token = linha[0][0]

        # O parser valida a "gramatica" da linguagem
        # Embora esta implementação seja linear (sem criar uma AST complexa com pilhas explicitas
        # Ele compre o papel, garantir que a sequência de simbolos (tokens)
        # Obedece as regras de formação da nossa linguagem
        if primeiro_token == 'ID':
            if len(linha) < 3: return False
            if linha[1][0] != 'ASSIGN': return False 
            
            for i in range(2, len(linha)):
                if i % 2 == 0: 
                    if linha[i][0] not in ('ID', 'NUM'): return False
                else:
                    if linha[i][0] not in ('PLUS', 'MINUS', 'MULT', 'DIV'): return False
                    
        elif primeiro_token == 'PRINT':
            if len(linha) != 4: return False
            if linha[1][0] != 'LPAREN' or linha[2][0] != 'ID' or linha[3][0] != 'RPAREN': 
                return False
        else:
            return False 
    return True

# 3. ANÁLISE SEMÂNTICA
# Teoria: linguagens sensiveis ao contexto (tipo 1) / contexto hisótico
def semantico(tokens):
    # Gramáticas livres de contexto (do parser) não têm "memória" para saber 
    # se uma variável foi declarada antes do uso. Contornamos essa limitação teórica 
    # usando uma Tabela de Símbolos, que armazena o estado e o contexto histórico do programa.
    tabela_simbolos = set()
    linhas = separar_por_linhas(tokens)
    for linha in linhas:
        if linha[0][0] == 'ID':
            var_destino = linha[0][1]
            tabela_simbolos.add(var_destino) # Registra a variável na Tabela de Símbolos
            for i in range(2, len(linha)):
                if linha[i][0] == 'ID':
                    var_uso = linha[i][1]
                    if var_uso not in tabela_simbolos:
                        raise ValueError(f"Erro Semântico: Variável '{var_uso}' não definida antes do uso.")
        elif linha[0][0] == 'PRINT':
            var_uso = linha[2][1]
            if var_uso not in tabela_simbolos:
                raise ValueError(f"Erro Semântico: Variável '{var_uso}' não definida para o print.")

# 4. GERAÇÃO DE CÓDIGO INTERMEDIÁRIO
# Teoria: redução de programas / universalidade
def gerar_codigo(tokens):
    linhas = separar_por_linhas(tokens)
    instrucoes = []

    
    # O código intermediário é uma representação abstrata do programa,
    # independente da linguagem fonte e da máquina alvo. Serve como ponte
    # entre a análise e a execução/geração de código nativo.
    for linha in linhas:
        if linha[0][0] == 'ID':
            var_destino = linha[0][1]
            primeiro_op = linha[2][1]
            instrucoes.append(f"LOAD {primeiro_op}")
            
            # TRADUZ O SÍMBOLO PARA A INSTRUÇÃO CORRETA
            for i in range(3, len(linha), 2):
                operador = linha[i][0]
                prox_op = linha[i+1][1]
                
                if operador == 'PLUS': instrucoes.append(f"ADD {prox_op}")
                elif operador == 'MINUS': instrucoes.append(f"SUB {prox_op}")
                elif operador == 'MULT': instrucoes.append(f"MUL {prox_op}")
                elif operador == 'DIV': instrucoes.append(f"DIV {prox_op}")
                
            instrucoes.append(f"STORE {var_destino}")
            
        elif linha[0][0] == 'PRINT':
            var_alvo = linha[2][1]
            instrucoes.append(f"PRINT {var_alvo}")
    return instrucoes

# 5. EXECUÇÃO
# Teoria máquina de turing (tipo 0)
def executar(codigo_intermediario) -> str:
    """Executa o código intermediário e retorna o output como string."""
    saida = StringIO()
    # O dicionário 'memoria' atua como a fita da Máquina de Turing, 
    # armazenando os valores e estados temporários ou permanentes.
    memoria = {}
    # O 'acumulador' atua como a cabeça de leitura/escrita e a unidade 
    # de processamento, manipulando os dados da "fita" baseando-se nas instruções.
    acumulador = 0

    for instrucao in codigo_intermediario:
        partes = instrucao.split()
        comando = partes[0]
        argumento = partes[1] if len(partes) > 1 else None

        if argumento:
            valor = int(argumento) if argumento.isdigit() else memoria.get(argumento, 0)

        if comando == 'LOAD':   acumulador = valor
        elif comando == 'ADD':  acumulador += valor
        elif comando == 'SUB':  acumulador -= valor
        elif comando == 'MUL':  acumulador *= valor
        elif comando == 'DIV':  acumulador //= valor
        elif comando == 'STORE': memoria[argumento] = acumulador
        elif comando == 'PRINT': saida.write(str(memoria.get(argumento, 0)) + "\n")

    return saida.getvalue()


# INTEGRAÇÃO DO COMPILADOR
def compilar(codigo: str) -> dict:
    """
    Compila o código e retorna um dicionário com os resultados de cada etapa.
    Em vez de imprimir, retorna tudo para a UI exibir.
    """
    resultado = {
        "tokens": [],
        "erro_sintatico": False,
        "erro_semantico": None,
        "codigo_intermediario": [],
        "output": "",
        "sucesso": False,
    }

    tokens = lexer(codigo)
    resultado["tokens"] = [
        f"{t[0]}({t[1]})" if t[0] in ('ID', 'NUM') else t[1]
        for t in tokens if t[0] != 'NEWLINE'
    ]

    if not parser(tokens):
        resultado["erro_sintatico"] = True
        return resultado

    try:
        semantico(tokens)
    except ValueError as e:
        resultado["erro_semantico"] = str(e)
        return resultado

    asm = gerar_codigo(tokens)
    resultado["codigo_intermediario"] = asm
    resultado["output"] = executar(asm)
    resultado["sucesso"] = True
    return resultado

# TESTE DO COMPILADOR
codigo_minilang = """
x = 10
y = 2
z = x * y
w = z - 5
res = w / 3
print(res)
"""

compilar(codigo_minilang)
