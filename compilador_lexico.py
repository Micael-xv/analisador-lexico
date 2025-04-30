import tkinter as tk
from tkinter import ttk
import re

# EXPRESSÕES REGULARES DOS TOKENS
TOKENS = {
    'KEYWORD': r'\b(if|else|while|for|return|break|class|function|bool|int|float|char|void|switch|case|do)\b',
    'STRING': r'"[^"\n]*"|\'[^\'\n]*\'',
    'ID': r'\b[a-zA-Z_][a-zA-Z0-9_]*\b',
    'NUM_FLOAT': r'\b\d+\.\d+\b',
    'NUM_INT': r'\b\d+\b',
    'OP': r'(==|!=|<=|>=|[+\-*/=<>])',
    'SYMBOL': r'[();{},]',
    'WHITESPACE': r'\s+',
    'UNKNOWN': r'.'
}

# FUNÇÃO DE ANÁLISE LÉXICA
def analisar_codigo(codigo):
    linhas = codigo.split('\n')
    resultado = []
    tabela_simbolos = []
    erros = []

    for num_linha, linha in enumerate(linhas, 1):
        pos = 0
        while pos < len(linha):
            match = None
            for token_nome, padrao in TOKENS.items():
                regex = re.compile(padrao)
                match = regex.match(linha, pos)
                if match:
                    lexema = match.group(0)
                    if token_nome == 'WHITESPACE':
                        pass
                    elif token_nome == 'UNKNOWN':
                        erros.append((num_linha, lexema))
                    else:
                        resultado.append((token_nome, lexema, num_linha))
                        if token_nome in ['ID', 'NUM_INT', 'NUM_FLOAT']:
                            tabela_simbolos.append((lexema, token_nome, num_linha))
                    pos = match.end(0)
                    break
            if not match:
                erros.append((num_linha, linha[pos]))  # Adiciona um erro quando nada é encontrado
                pos += 1
    return resultado, tabela_simbolos, erros

def analisar():
    codigo = entrada.get("1.0", tk.END)
    tokens, simbolos, erros = analisar_codigo(codigo)

    tree.delete(*tree.get_children())
    for token in tokens:
        tree.insert("", "end", values=token)

    erros_box.config(state=tk.NORMAL)
    erros_box.delete("1.0", tk.END)
    for e in erros:
        erros_box.insert(tk.END, f"Erro '{e[1]}' na linha {e[0]}\n")
    erros_box.config(state=tk.DISABLED)

def limpar_campos():
    entrada.delete("1.0", tk.END)
    tree.delete(*tree.get_children())
    erros_box.delete("1.0", tk.END)
    erros_box.config(state=tk.DISABLED)

# JANELA PRINCIPAL
root = tk.Tk()
root.title("Analisador Léxico - Mini Compilador")
root.geometry("950x750")

# Entrada de Código
tk.Label(root, text="Código de Entrada", font=("Arial", 12, "bold")).pack(anchor="center", padx=10)

entrada_frame = tk.Frame(root)
entrada_scroll = tk.Scrollbar(entrada_frame)
entrada = tk.Text(entrada_frame, height=10, width=110, yscrollcommand=entrada_scroll.set, font=("Consolas", 10))
entrada_scroll.config(command=entrada.yview)
entrada.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
entrada_scroll.pack(side=tk.RIGHT, fill=tk.Y)
entrada_frame.pack(padx=10, pady=5)

# Botões
btns = tk.Frame(root)
tk.Button(btns, text="Analisar", width=15, command=analisar).pack(side=tk.LEFT, padx=10)
tk.Button(btns, text="Limpar Tudo", width=15, command=limpar_campos).pack(side=tk.LEFT, padx=10)
btns.pack(pady=10)

tk.Label(root, text="Tokens Reconhecidos", font=("Arial", 12, "bold")).pack(anchor="w", padx=180)

# Frame conjunto para Tokens + Erros
tokens_erros_frame = tk.Frame(root)
tokens_erros_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# Tokens
tree_frame = tk.Frame(tokens_erros_frame)
tree_scroll = tk.Scrollbar(tree_frame)
tree = ttk.Treeview(tree_frame, columns=("Token", "Lexema", "Linha"), show="headings", height=15, yscrollcommand=tree_scroll.set)
tree_scroll.config(command=tree.yview)
tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
for col in tree["columns"]:
    tree.heading(col, text=col)
    tree.column(col, width=130)
tree_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

# Erros Léxicos
erros_frame = tk.Frame(tokens_erros_frame)
erros_scroll = tk.Scrollbar(erros_frame)

# Título do relatório de erros dentro do frame
erros_title = tk.Label(erros_frame, text="Relatório de Erros Léxicos", font=("Arial", 12, "bold"))
erros_title.pack(anchor="center", padx=5)

erros_box = tk.Text(erros_frame, height=15, width=40, yscrollcommand=erros_scroll.set, fg="red", font=("Consolas", 10))
erros_scroll.config(command=erros_box.yview)
erros_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
erros_scroll.pack(side=tk.RIGHT, fill=tk.Y)
erros_box.config(state=tk.DISABLED)
erros_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

# Tabela de Símbolos
tk.Label(root, text="Tabela de Símbolos", font=("Arial", 12, "bold")).pack(anchor="center", padx=10)

# Executar
root.mainloop()
