import sqlite3
from pathlib import Path

ROOT_PATH = Path(__file__).parent

conexao = sqlite3.connect(ROOT_PATH / "danilo_bank.db")
cursor = conexao.cursor()


def criar_tabela(conexao, cursor, table, item1, item2):
    sql = f"CREATE TABLE {table} (id INTEGER PRIMARY KEY AUTOINCREMENT, {item1} VARCHAR(100), {item2} int(10))"

    try:
        cursor.execute(sql)
        conexao.commit()
        print(f"Criação da tabela: {table} foi executada com sucesso com os parâmetros: {item1} e {item2}")
    except Exception as err:
        print(f"Não foi possível adicionar os itens: {item1} e {item2} na nova tabela: {table}. {err}")


def add_coluna_tabelas_existentes(conexao, cursor, table, nova_coluna):
    sql = f"ALTER TABLE {table} ADD {nova_coluna} INT;"

    try:
        cursor.execute(sql)
        conexao.commit()
        print("Alteração realizada com sucesso.")
    except Exception as err:
        print(f"Não foi possível alterar a tabela: {table} para inserir a coluna: {nova_coluna}. {err}")


def inserir_registro(conexao, cursor, nome, idade):
    data = (nome, idade)

    try:
        cursor.execute("INSERT INTO clientes (nome, idade) VALUES (?, ?);", data)
        conexao.commit()
    except Exception as err:
        print(f"Não foi possível inserir o nome: {nome} e idade: {idade} no banco de dados. {err}")


def atualizar_registro(conexao, cursor, nome, idade, id):
    sql = "UPDATE clientes SET nome=?, idade=? WHERE id=?;"

    try:
        cursor.execute(sql, (nome, idade, id))
        conexao.commit()
        print(f"Atualização realizada com sucesso, dados adicionados ao banco de dados: {nome}, {idade}")
    except Exception as err:
        print(f"Atualização não realizada no banco de dados, valide os dados e tente novamente: {err}")


# criar_tabela(conexao, cursor)
atualizar_registro(conexao, cursor, "Jessica machadinho", 20, 3)
# alterar_tabela(conexao, cursor, "clientes", "idade")
