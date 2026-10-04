import sqlite3
from pathlib import Path

ROOT_PATH = Path(__file__).parent

conexao = sqlite3.connect(ROOT_PATH / "danilo_bank.db")
cursor = conexao.cursor()


def criar_tabela(conexao, cursor):
    tabela_unica = """
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER NOT NULL CHECK (idade > 15 AND idade < 100)
        )
    """

    try:
        cursor.execute(tabela_unica)
        conexao.commit()
        print(
            "Criação da tabela: clientes foi executada com sucesso com os parâmetros: nome e idade"
        )
    except Exception as err:
        conexao.rollback()
        print(
            f"Não foi possível adicionar os itens: nome e idade na nova tabela: cliente. {err}"
        )


def migrar_clientes(conexao):
    if conexao.in_transaction:
        raise RuntimeError("Execute esta migração sem outra transação aberta.")

    try:
        conexao.execute("BEGIN IMMEDIATE")

        if conexao.execute("SELECT 1 FROM clientes LIMIT 1").fetchone():
            raise ValueError(
                "A tabela possui clientes; É preciso migrar os dados existentes."
            )

        conexao.execute("""
            CREATE TABLE clientes_nova (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                idade INTEGER NOT NULL CHECK(idade > 15 AND idade < 100)
            )
        """)

        conexao.execute("DROP TABLE clientes")
        conexao.execute("ALTER TABLE clientes_nova RENAME TO clientes")

        conexao.commit()
        print("migração realizada com sucesso.")
    except Exception as err:
        conexao.rollback()
        raise RuntimeError(
            f"Não foi possível alterar a tabela clientes: {err}"
        ) from err


def inserir_registro(conexao, cursor, nome, idade):
    if not isinstance(idade, int) or isinstance(idade, bool) or not 15 < idade < 100:
        raise ValueError(
            "A idade deve ser um número inteiro maior que 15 e menor que 100."
        )
    if not isinstance(nome, str):
        raise ValueError(
            "Insira um nome correto para inserir no banco"
        )
    nome = nome.strip()
    if not nome:
        raise ValueError(
            "Insira um nome correto para inserir no banco"
        )

    data = (nome, idade)

    try:
        cursor.execute("INSERT INTO clientes (nome, idade) VALUES (?, ?);", data)
        if cursor.rowcount != 1:
            raise sqlite3.DatabaseError("A inserção não gravou exatamente um registro.")
        conexao.commit()
    except sqlite3.Error as err:
        conexao.rollback()
        raise RuntimeError(
            f"Não foi possível salvar o usuário no banco de dados: {err}"
        ) from err


def atualizar_registro(conexao, cursor, nome, idade, id):
    sql = "UPDATE clientes SET nome=?, idade=? WHERE id=?;"

    try:
        cursor.execute(sql, (nome, idade, id))
        conexao.commit()
        print(
            f"Atualização realizada com sucesso, dados adicionados ao banco de dados: {nome}, {idade}"
        )
    except Exception as err:
        print(
            f"Atualização não realizada no banco de dados, valide os dados e tente novamente: {err}"
        )


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
