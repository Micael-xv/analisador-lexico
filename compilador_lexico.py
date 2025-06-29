import tkinter as tk
from tkinter import filedialog, ttk
import re

TOKEN_PATTERNS = [
    ('T_PALAVRA_RESERVADA', r'\b(main|if|else|while|for|return|int|float|char|bool|void)\b'),
    ('T_LITERAL_STRING', r'"[^"]*"'),
    ('T_LITERAL_CHAR', r'\'[^\']\''),
    ('T_ID', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
    ('T_NUM_FLOAT', r'\b\d+\.\d+\b'),
    ('T_NUM_INT', r'\b\d+\b'),
    ('T_OP_REL_IGUAL',      r'=='),
    ('T_OP_REL_DIF',        r'!='),
    ('T_OP_REL_MENOR_IGUAL',r'<='),
    ('T_OP_REL_MAIOR_IGUAL',r'>='),
    ('T_OP_ATRIBUICAO',     r'='),
    ('T_OP_REL_MENOR',      r'<'),
    ('T_OP_REL_MAIOR',      r'>'),
    ('T_OP_SOMA',           r'\+'),
    ('T_OP_SUB',            r'-'),
    ('T_OP_MULT',           r'\*'),
    ('T_OP_DIV',            r'/'),

    # Delimitadores
    ('T_DELIM_ABRE_PARENTESES',  r'\('),
    ('T_DELIM_FECHA_PARENTESES', r'\)'),
    ('T_DELIM_ABRE_CHAVES',      r'\{'),
    ('T_DELIM_FECHA_CHAVES',     r'\}'),
    ('T_DELIM_PONTO_VIRGULA',    r';'),
    ('T_DELIM_VIRGULA',          r','),

    ('WHITESPACE', r'\s+'),
    ('T_ERRO', r'.')
]

def analisar_codigo(codigo):
    linhas = codigo.split('\n')
    resultado = []
    tabela_simbolos = []
    erros = []

    for num_linha, linha in enumerate(linhas, 1):
        pos = 0
        while pos < len(linha):
            match = None
            for token_nome, padrao in TOKEN_PATTERNS:
                regex = re.compile(padrao)
                match = regex.match(linha, pos)
                if match:
                    lexema = match.group(0)
                    if token_nome == 'WHITESPACE':
                        pass
                    elif token_nome == 'T_ERRO':
                        erros.append((num_linha, lexema))
                    else:
                        resultado.append((token_nome, lexema, num_linha))
                        if token_nome in ['T_ID', 'T_NUM_INT', 'T_NUM_FLOAT']:
                            if not any(s[0] == lexema for s in tabela_simbolos):
                                tabela_simbolos.append((lexema, token_nome, num_linha))
                    pos = match.end(0)
                    break
            if not match:
                pos += 1
    return resultado, tabela_simbolos, erros

def analisar():
    codigo = entrada.get("1.0", tk.END)
    tokens, simbolos, erros = analisar_codigo(codigo)

    tree.delete(*tree.get_children())
    for token in tokens:
        tree.insert("", "end", values=token)
    simbolos_tree.delete(*simbolos_tree.get_children())
    for simbolo in simbolos:
        simbolos_tree.insert("", "end", values=simbolo)

    erros_box.config(state=tk.NORMAL)
    erros_box.delete("1.0", tk.END)
    if not erros:
        erros_box.insert(tk.END, "Nenhum erro léxico encontrado.")
    else:
        for e in erros:
            erros_box.insert(tk.END, f"Erro: Caractere não reconhecido '{e[1]}' na linha {e[0]}\n")
    erros_box.config(state=tk.DISABLED)

def limpar_campos():
    entrada.delete("1.0", tk.END)
    tree.delete(*tree.get_children())
    simbolos_tree.delete(*simbolos_tree.get_children())
    erros_box.config(state=tk.NORMAL)
    erros_box.delete("1.0", tk.END)
    erros_box.insert(tk.END, "Aguardando análise...")
    erros_box.config(state=tk.DISABLED)

root = tk.Tk()
root.title("Analisador Léxico - Mini Compilador")
root.geometry("1100x750")

main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

left_column = tk.Frame(main_frame)
left_column.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

tk.Label(left_column, text="Código Fonte", font=("Arial", 14, "bold")).pack(pady=(0,5))
entrada_frame = tk.Frame(left_column, borderwidth=2, relief="groove")
entrada_scroll = tk.Scrollbar(entrada_frame)
entrada = tk.Text(entrada_frame, height=20, width=60, yscrollcommand=entrada_scroll.set, font=("Consolas", 11))
entrada_scroll.config(command=entrada.yview)
entrada.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
entrada_scroll.pack(side=tk.RIGHT, fill=tk.Y)
entrada_frame.pack(fill=tk.BOTH, expand=True)

btns_frame = tk.Frame(left_column)
tk.Button(btns_frame, text="Analisar Código", font=("Arial", 12), command=analisar).pack(fill=tk.X, pady=(10,5))
tk.Button(btns_frame, text="Limpar Tudo", font=("Arial", 12), command=limpar_campos).pack(fill=tk.X)
btns_frame.pack(pady=10, fill=tk.X)

right_column = tk.Frame(main_frame)
right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

notebook = ttk.Notebook(right_column)
notebook.pack(fill=tk.BOTH, expand=True)

tokens_tab = tk.Frame(notebook)
notebook.add(tokens_tab, text='Tokens Reconhecidos')
tk.Label(tokens_tab, text="Tabela de Tokens", font=("Arial", 14, "bold")).pack(pady=(0,5))
tree_frame = tk.Frame(tokens_tab, borderwidth=2, relief="groove")
tree_scroll = tk.Scrollbar(tree_frame)
tree = ttk.Treeview(tree_frame, columns=("Token", "Lexema", "Linha"), show="headings", yscrollcommand=tree_scroll.set)
tree_scroll.config(command=tree.yview)
tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
for col in tree["columns"]:
    tree.heading(col, text=col)
    tree.column(col, width=150, anchor="w")
tree_frame.pack(fill=tk.BOTH, expand=True)

simbolos_tab = tk.Frame(notebook)
notebook.add(simbolos_tab, text='Tabela de Símbolos')
tk.Label(simbolos_tab, text="Tabela de Símbolos", font=("Arial", 14, "bold")).pack(pady=(0,5))
simbolos_tree_frame = tk.Frame(simbolos_tab, borderwidth=2, relief="groove")
simbolos_scroll = tk.Scrollbar(simbolos_tree_frame)
simbolos_tree = ttk.Treeview(simbolos_tree_frame, columns=("Lexema", "Token", "Linha Def."), show="headings", yscrollcommand=simbolos_scroll.set)
simbolos_scroll.config(command=simbolos_tree.yview)
simbolos_scroll.pack(side=tk.RIGHT, fill=tk.Y)
simbolos_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
for col in simbolos_tree["columns"]:
    simbolos_tree.heading(col, text=col)
    simbolos_tree.column(col, width=150, anchor="w")
simbolos_tree_frame.pack(fill=tk.BOTH, expand=True)

tk.Label(right_column, text="Relatório de Erros", font=("Arial", 14, "bold")).pack(pady=(10,5))
erros_frame = tk.Frame(right_column, borderwidth=2, relief="groove")
erros_scroll = tk.Scrollbar(erros_frame)
erros_box = tk.Text(erros_frame, height=10, yscrollcommand=erros_scroll.set, fg="red", font=("Consolas", 10))
erros_scroll.config(command=erros_box.yview)
erros_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
erros_scroll.pack(side=tk.RIGHT, fill=tk.Y)
erros_box.insert(tk.END, "Aguardando análise...")
erros_box.config(state=tk.DISABLED)
erros_frame.pack(fill=tk.X, expand=True)

root.mainloop()
