import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('esslog_voluntarios.db')
c = conn.cursor()

# Criar tabela para voluntários
c.execute('''
    CREATE TABLE IF NOT EXISTS voluntarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL
    )
''')
conn.commit()

# Função para adicionar voluntário
def adicionar_voluntario():
    nome = entry_nome.get()
    email = entry_email.get()
    if nome and email:
        c.execute('INSERT INTO voluntarios (nome, email) VALUES (?, ?)', (nome, email))
        conn.commit()
        messagebox.showinfo("Sucesso", "Voluntário adicionado!")
        listar_voluntarios()
        entry_nome.delete(0, tk.END)
        entry_email.delete(0, tk.END)
    else:
        messagebox.showwarning("Erro", "Por favor, preencha todos os campos.")

# Função para remover voluntário
def remover_voluntario():
    id_voluntario = entry_id.get()
    if id_voluntario:
        c.execute('DELETE FROM voluntarios WHERE id = ?', (id_voluntario,))
        conn.commit()
        messagebox.showinfo("Sucesso", "Voluntário removido!")
        listar_voluntarios()
        entry_id.delete(0, tk.END)
    else:
        messagebox.showwarning("Erro", "Por favor, insira o ID do voluntário.")

# Função para listar voluntários
def listar_voluntarios():
    lista.delete(0, tk.END)
    c.execute('SELECT * FROM voluntarios')
    for voluntario in c.fetchall():
        lista.insert(tk.END, f"ID: {voluntario[0]}, Nome: {voluntario[1]}, Email: {voluntario[2]}")

# Função para salvar a lista de voluntários em um arquivo
def salvar_lista():
    voluntarios = c.execute('SELECT * FROM voluntarios').fetchall()
    if voluntarios:
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filepath:
            with open(filepath, 'w') as file:
                for voluntario in voluntarios:
                    file.write(f"ID: {voluntario[0]}, Nome: {voluntario[1]}, Email: {voluntario[2]}\n")
            messagebox.showinfo("Sucesso", "Lista de voluntários salva!")
    else:
        messagebox.showwarning("Aviso", "Nenhum voluntário para salvar!")

# Interface gráfica usando Tkinter
janela = tk.Tk()
janela.title("Gerenciamento de Voluntários ESSLOG")

# Maximizar a janela
janela.state('zoomed')  # Funciona para maximizar a janela no Windows

# Configurações de layout (usando grid)
frame_principal = tk.Frame(janela, padx=20, pady=20)
frame_principal.pack(expand=True)

# Campos de entrada para nome e email
tk.Label(frame_principal, text="Nome", font=('Arial', 12)).grid(row=0, column=0, sticky=tk.W, pady=10)
entry_nome = tk.Entry(frame_principal, width=40, font=('Arial', 12))
entry_nome.grid(row=0, column=1, pady=10)

tk.Label(frame_principal, text="Email", font=('Arial', 12)).grid(row=1, column=0, sticky=tk.W, pady=10)
entry_email = tk.Entry(frame_principal, width=40, font=('Arial', 12))
entry_email.grid(row=1, column=1, pady=10)

# Botão para adicionar voluntário
botao_adicionar = tk.Button(frame_principal, text="Adicionar Voluntário", font=('Arial', 12), command=adicionar_voluntario)
botao_adicionar.grid(row=2, column=0, columnspan=2, pady=10)

# Campo de entrada para ID e botão para remover voluntário
tk.Label(frame_principal, text="ID para remover", font=('Arial', 12)).grid(row=3, column=0, sticky=tk.W, pady=10)
entry_id = tk.Entry(frame_principal, width=40, font=('Arial', 12))
entry_id.grid(row=3, column=1, pady=10)

botao_remover = tk.Button(frame_principal, text="Remover Voluntário", font=('Arial', 12), command=remover_voluntario)
botao_remover.grid(row=4, column=0, columnspan=2, pady=10)

# Lista para exibir voluntários
lista = tk.Listbox(frame_principal, width=80, height=10, font=('Arial', 12))
lista.grid(row=5, column=0, columnspan=2, pady=10)

# Botão para listar voluntários
botao_listar = tk.Button(frame_principal, text="Listar Voluntários", font=('Arial', 12), command=listar_voluntarios)
botao_listar.grid(row=6, column=0, columnspan=2, pady=10)

# Botão para salvar a lista de voluntários
botao_salvar = tk.Button(frame_principal, text="Salvar Lista de Voluntários", font=('Arial', 12), command=salvar_lista)
botao_salvar.grid(row=7, column=0, columnspan=2, pady=10)

# Exibir voluntários ao iniciar
listar_voluntarios()

# Executar o loop da interface
janela.mainloop()

# Fechar conexão com o banco de dados
conn.close()
