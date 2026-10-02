import sqlite3
from pathlib import Path

ROOT_PATH = Path(__file__).parent

conexao = sqlite3.connect(ROOT_PATH / "danilo_bank.db")
cursor = conexao.cursor()


def criar_tabela(conexao, cursor):
    tabelas_unica = "CREATE TABLE clientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nome VARCHAR(100), idade int(10))"

    try:
        cursor.execute(tabelas_unica)
        conexao.commit()
        print("Criação da tabela: clientes foi executada com sucesso com os parâmetros: nome e idade")
    except Exception as err:
        conexao.rollback()
        print(f"Não foi possível adicionar os itens: nome e idade na nova tabela: cliente. {err}")


def add_coluna_tabelas_existentes(conexao, cursor):
    sql = "ALTER TABLE clientes ADD idade INT;"

    try:
        cursor.execute(sql)
        conexao.commit()
        print("Alteração realizada com sucesso.")
    except Exception as err:
        conexao.rollback()
        print(f"Não foi possível alterar a tabela: clientes para inserir a nova coluna. {err}")


def inserir_registro(conexao, cursor, nome, idade):
    data = (nome, idade)

    try:
        cursor.execute("INSERT INTO clientes (nome, idade) VALUES (?, ?);", data)
        conexao.commit()
    except Exception as err:
        conexao.rollback()
        print(f"Não foi possível inserir o nome: {nome} e idade: {idade} no banco de dados. {err}")


def atualizar_registro(conexao, cursor, nome, idade, id):
    sql = "UPDATE clientes SET nome=?, idade=? WHERE id=?;"

    try:
        cursor.execute(sql, (nome, idade, id))
        conexao.commit()
        print(f"Atualização realizada com sucesso, dados adicionados ao banco de dados: {nome}, {idade}")
    except Exception as err:
        print(f"Atualização não realizada no banco de dados, valide os dados e tente novamente: {err}")


def deletar_registro(conexao, cursor, id):
    usuario = "SELECT nome, idade FROM clientes Where id=?"
    delete = "DELETE FROM clientes WHERE id=?"

    try:
        cursor.execute(usuario, (id,))
        confirm = cursor.fetchone()
        if confirm:
            nome, idade = confirm
        else:
            return

        print(f"Tem certeza que deseja excluir os dados: {nome}, {idade}")
        resp = input("1: Sim, 2: Não\n")
        if resp.lower() in ("1", "sim"):
            cursor.execute(delete, (id,))
            conexao.commit()
            print("Usuário deletado com sucesso")
        else:
            return

    except Exception as err:
        print(f"Não foi possível apagar o registro: {usuario}. {err}")
