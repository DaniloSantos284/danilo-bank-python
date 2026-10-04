import sqlite3

import pytest

from database.init import inserir_registro
from models.User import User


def test_inserir_registro_commits_saved_user():
    conexao = sqlite3.connect(":memory:")
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE clientes (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            idade INTEGER NOT NULL
        )
    """)
    conexao.commit()

    inserir_registro(conexao, cursor, "Ana", 25)

    assert cursor.execute(
        "SELECT nome, idade FROM clientes"
    ).fetchone() == ("Ana", 25)
    assert not conexao.in_transaction
    conexao.close()


def test_inserir_registro_raises_when_database_write_fails():
    conexao = sqlite3.connect(":memory:")
    cursor = conexao.cursor()

    with pytest.raises(RuntimeError, match="Não foi possível salvar"):
        inserir_registro(conexao, cursor, "Ana", 25)

    assert not conexao.in_transaction
    conexao.close()


def test_user_creation_fails_when_database_write_fails(monkeypatch):
    def falhar_insercao(*args):
        raise RuntimeError("Falha simulada ao salvar.")

    monkeypatch.setattr("models.User.inserir_registro", falhar_insercao)

    with pytest.raises(RuntimeError, match="Falha simulada"):
        User("Ana", 25)
