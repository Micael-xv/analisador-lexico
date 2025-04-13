# Analisador Léxico - Mini Compilador

## Descrição do Projeto

Este projeto é um **Analisador Léxico** simples, implementado em **Python** com uma interface gráfica utilizando o **Tkinter**. Ele é capaz de analisar código-fonte escrito em uma linguagem fictícia e identificar os **tokens** (como palavras-chave, identificadores, números inteiros, números de ponto flutuante, operadores e símbolos). O projeto também gera uma **tabela de símbolos** e um **relatório de erros léxicos**.

### Funcionalidades:
- **Análise léxica** do código-fonte.
- Identificação de **tokens** como palavras-chave, operadores, identificadores, números inteiros e flutuantes.
- **Tabela de símbolos**: lista de lexemas válidos encontrados no código.
- **Relatório de erros léxicos**: lista de lexemas inválidos ou desconhecidos encontrados no código.
- **Carregamento de código-fonte** de arquivos de texto.
- **Limpeza de todos os campos** da interface gráfica.

---

## Requisitos

Para rodar este projeto, você precisa de um ambiente Python com as bibliotecas necessárias instaladas.

### 1. Python

Este projeto foi desenvolvido em Python **3.x**. Você pode fazer o download do Python aqui:  
[https://www.python.org/downloads/](https://www.python.org/downloads/)

### 2. Bibliotecas Python

As bibliotecas principais utilizadas são:
- **Tkinter**: Biblioteca para criação de interfaces gráficas (geralmente já instalada com o Python).
- **re**: Biblioteca para manipulação de expressões regulares (também já incluída no Python).

### Instalação das Bibliotecas

Caso você precise instalar o **Tkinter** (em sistemas que não o possuem por padrão), você pode usar o seguinte comando:

```bash
pip install tk