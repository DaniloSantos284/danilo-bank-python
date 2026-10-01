from unittest.mock import Mock, patch
from utils.boas_vindas import exibir_menu, escolha_operacao

import pytest


# O @patch intercepta a função nativa input do Python e força ela a retornar 2
@patch("builtins.input", return_value="2")
def test_exibir_menu_retorna_inteiro_escolhido(mock_input, capsys):
    # Executa a função. O teste não vai travar porque o input() foi "mockado".
    resultado = exibir_menu()

    # 1. Verifica se a função converteu a string digitada para int corretamente
    assert resultado == 2

    # 2. Verifica se o menu foi desenhado corretamente na tela
    # capsys.readouterr() captura todos os prints disparados durante a execução
    terminal = capsys.readouterr()

    assert "📋 MENU PRINCIPAL" in terminal.out
    assert "2. Sacar" in terminal.out
    assert "10. Sair do banco" in terminal.out


@patch("builtins.input", return_value="a")
def test_exibir_menu_quebra_com_letra(mock_input):
    # Praticando a boa prática de testar quando o usuário insere itens errados.
    # Como o código faz int(input()), digitar 'a' deve gerar um ValueError.
    with pytest.raises(ValueError):
        exibir_menu()


def test_exibir_menu_retorna_opcao_digitada(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda: "3")

    resultado = exibir_menu()

    assert resultado == 3
    assert isinstance(resultado, int)


def test_opcao_1_deposita_valor_informado(monkeypatch):
    conta = Mock()
    user = Mock()
    monkeypatch.setattr("builtins.input", lambda: "25.50")

    resultado = escolha_operacao(conta, user, 1)

    conta.depositar.assert_called_once_with(25.5)
    assert resultado is None
