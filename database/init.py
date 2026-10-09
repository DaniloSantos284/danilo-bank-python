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

    indice_nome = """
    CREATE INDEX IF NOT EXISTS idx_clientes_nome_nocase
    ON clientes(nome COLLATE NOCASE)
    """

    try:
        cursor.execute(tabela_unica)
        cursor.execute(indice_nome)
        conexao.commit()
        print(
            "Banco inicializado com sucesso"
        )
    except sqlite3.Error as err:
        conexao.rollback()
        raise RuntimeError(
            f"Não foi possível inicializar o banco: {err}"
        ) from err


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
        conexao.execute("""
            CREATE INDEX IF NOT EXISTS idx_clientes_nome_nocase
            ON clientes(nome COLLATE NOCASE)
        """)

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
    if not isinstance(id, int) or id <= 0:
        raise ValueError("ID inválido.")
    if not isinstance(nome, str):
        raise ValueError("Nome deve ser uma string válida.")
    nome = nome.strip()
    if not nome:
        raise ValueError("Nome não pode ficar vazio.")
    if not isinstance(idade, int) or not 15 < idade < 100:
        raise ValueError("Idade inválida")

    try:
        cursor.execute(
            "UPDATE clientes SET nome = ?, idade = ? WHERE id = ?",
            (nome, idade, id),
        )

        if cursor.rowcount != 1:
            conexao.rollback()
            raise ValueError("Nenhum registro foi atualizado, tente novamente.")

        conexao.commit()
    except Exception:
        conexao.rollback()
        raise


def deletar_registro(conexao, cursor, id):
    if not isinstance(id, int) or isinstance(id, bool) or id <= 0:
        raise ValueError("ID incorreto.")
    if conexao.in_transaction:
        raise RuntimeError(
            "Não é possível excluir um cliente enquanto há outras transações abertas."
        )

    try:
        cursor.execute(
            "SELECT nome, idade FROM clientes WHERE id = ?",
            (id,),
        )
        cliente = cursor.fetchone()
    except sqlite3.Error as err:
        raise RuntimeError(
            f"Não foi possível consultar o cliente para exclusão: {err}"
        ) from err

    if cliente is None:
        print("Cliente não encontrado.")
        return False

    nome, idade = cliente
    print(f"Tem certeza que deseja excluir os dados: {nome}, {idade}")
    resposta = input("1: Sim, 2: Não\n").strip().casefold()

    if resposta not in ("1", "sim"):
        print("Exclusão cancelada.")
        return False

    try:
        cursor.execute(
            """
            DELETE FROM clientes
            WHERE id = ? AND nome = ? AND idade = ?
            """,
            (id, nome, idade)
        )

        if cursor.rowcount != 1:
            conexao.rollback()
            print(
                "O cliente foi alterado ou removido antes da confirmação. "
                "Consulte-o novamente e tente outra vez."
            )
            return False

        conexao.commit()
    except sqlite3.Error as err:
        conexao.rollback()
        raise RuntimeError(
            f"Não foi possível apagar o cliente: {err}"
        ) from err

    print("Usuário deletado com sucesso.")
    return True


def buscar_usuario(conexao, cursor, nome):
    if not isinstance(nome, str):
        raise ValueError("Nome deve ser uma string válida.")

    nome = nome.strip()
    if not nome:
        raise ValueError("Nome não pode ficar vazio.")

    try:
        cursor.execute(
            """
            SELECT id, nome, idade
            FROM clientes
            WHERE nome = ? COLLATE NOCASE
            ORDER BY nome COLLATE NOCASE, id
            """,
            (nome,),
        )
        return cursor.fetchall()
    except sqlite3.Error as err:
        raise RuntimeError(f"Não foi possível buscar o cliente: {err}") from err
