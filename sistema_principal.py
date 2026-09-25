from models.Conta import Conta
from models.User import User
from utils.boas_vindas import escolha_operacao, exibir_menu, hello_world
from utils.logging_config import obter_logger


LOGGER = obter_logger()

def executar_sistema():
    hello_world()

    while True:
        try:
            print("Insira seu nome e idade:")
            nome = str(input("Nome: "))
            idade = int(input("idade: "))
            user = User(nome, idade)
            break
        except ValueError as erro:
            print(f"\nErro: {erro}\n")

    conta = Conta(user)
    LOGGER.info("sessao_iniciada conta=%s", conta.identificador)

    while True:
        try:
            opcao_escolhida = exibir_menu()

            if opcao_escolhida == 10:
                LOGGER.info("sessao_encerrada conta=%s", conta.identificador)
                print("Até Mais!")
                break

            escolha_operacao(conta, user, opcao_escolhida)
        except ValueError as erro:
            print(f"Erro: {erro}")


if __name__ == "__main__":
    executar_sistema()
