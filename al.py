import tkinter as tk
from tkinter import filedialog, ttk
import re

# EXPRESSÕES REGULARES DOS TOKENS
TOKENS = {
    'KEYWORD': r'\b(if|else|while|int|float|return)\b',
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
                erros.append((num_linha, linha[pos]))
                pos += 1
    return resultado, tabela_simbolos, erros

# FUNÇÕES DE INTERFACE
def abrir_arquivo():
    caminho = filedialog.askopenfilename(filetypes=[("Arquivos de Texto", "*.txt")])
    if caminho:
        with open(caminho, "r", encoding="utf-8") as f:
            entrada.delete("1.0", tk.END)
            entrada.insert(tk.END, f.read())

def analisar():
    codigo = entrada.get("1.0", tk.END)
    tokens, simbolos, erros = analisar_codigo(codigo)

    tree.delete(*tree.get_children())
    for token in tokens:
        tree.insert("", "end", values=token)

    simbolos_box.config(state=tk.NORMAL)
    simbolos_box.delete("1.0", tk.END)
    for s in simbolos:
        simbolos_box.insert(tk.END, f"{s[0]} ({s[1]}) na linha {s[2]}\n")
    simbolos_box.config(state=tk.DISABLED)

    erros_box.config(state=tk.NORMAL)
    erros_box.delete("1.0", tk.END)
    for e in erros:
        erros_box.insert(tk.END, f"Erro '{e[1]}' na linha {e[0]}\n")
    erros_box.config(state=tk.DISABLED)

def limpar_campos():
    entrada.delete("1.0", tk.END)
    tree.delete(*tree.get_children())
    simbolos_box.config(state=tk.NORMAL)
    simbolos_box.delete("1.0", tk.END)
    simbolos_box.config(state=tk.DISABLED)
    erros_box.config(state=tk.NORMAL)
    erros_box.delete("1.0", tk.END)
    erros_box.config(state=tk.DISABLED)

# JANELA PRINCIPAL
root = tk.Tk()
root.title("Analisador Léxico - Mini Compilador")
root.geometry("850x750")

# Área de entrada com Scroll
entrada_frame = tk.Frame(root)
entrada_scroll = tk.Scrollbar(entrada_frame)
entrada = tk.Text(entrada_frame, height=10, width=100, yscrollcommand=entrada_scroll.set)
entrada_scroll.config(command=entrada.yview)
entrada.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
entrada_scroll.pack(side=tk.RIGHT, fill=tk.Y)
entrada_frame.pack(pady=10)

# Botões
btns = tk.Frame(root)
tk.Button(btns, text="Abrir Arquivo", command=abrir_arquivo).pack(side=tk.LEFT, padx=5)
tk.Button(btns, text="Analisar", command=analisar).pack(side=tk.LEFT, padx=5)
tk.Button(btns, text="Limpar Tudo", command=limpar_campos).pack(side=tk.LEFT, padx=5)
btns.pack(pady=5)

# Tabela de Tokens com Scroll
tk.Label(root, text="Tokens Reconhecidos", font=("Arial", 12, "bold")).pack()
tree_frame = tk.Frame(root)
tree_scroll = tk.Scrollbar(tree_frame)
tree = ttk.Treeview(tree_frame, columns=("Token", "Lexema", "Linha"), show="headings", height=10, yscrollcommand=tree_scroll.set)
tree_scroll.config(command=tree.yview)
tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
for col in tree["columns"]:
    tree.heading(col, text=col)
    tree.column(col, width=150)
tree_frame.pack(pady=5)

# Tabela de Símbolos com Scroll
tk.Label(root, text="Tabela de Símbolos", font=("Arial", 12, "bold")).pack()
simbolos_frame = tk.Frame(root)
simbolos_scroll = tk.Scrollbar(simbolos_frame)
simbolos_box = tk.Text(simbolos_frame, height=10, width=100, yscrollcommand=simbolos_scroll.set)
simbolos_scroll.config(command=simbolos_box.yview)
simbolos_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
simbolos_scroll.pack(side=tk.RIGHT, fill=tk.Y)
simbolos_box.config(state=tk.DISABLED)
simbolos_frame.pack(pady=5)

# Relatório de Erros com Scroll
tk.Label(root, text="Relatório de Erros Léxicos", font=("Arial", 12, "bold")).pack()
erros_frame = tk.Frame(root)
erros_scroll = tk.Scrollbar(erros_frame)
erros_box = tk.Text(erros_frame, height=10, width=100, yscrollcommand=erros_scroll.set, fg="red")
erros_scroll.config(command=erros_box.yview)
erros_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
erros_scroll.pack(side=tk.RIGHT, fill=tk.Y)
erros_box.config(state=tk.DISABLED)
erros_frame.pack(pady=5)

# Executar
root.mainloop()
