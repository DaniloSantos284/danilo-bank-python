import random
from utils.logging_config import obter_logger
from database.init import conexao, cursor, inserir_registro

LOGGER = obter_logger()


class User:
    def __init__(self, nome, idade, identificador=None):
        if idade < 16:
            raise ValueError("Infelizmente você não tem idade para utilizar os serviços da Danilo Bank")
        self.nome = nome
        self.idade = idade
        self.identificador = identificador if identificador is not None else random.randint(100000, 999999)
        inserir_registro(conexao, cursor, self.nome, self.idade)

    def __str__(self):
        return f"Usuário: {self.nome} e idade: {self.idade} anos"

    def informacoes_usuario(self):
        print(f"{self.__str__()}")

    def renomear_usuario(self, nome):
        print(f"Confirme o ajuste do seu nome: {nome}")
        print("1-Sim 2-Não")
        confirmacao = str(input())
        if confirmacao == "1" or confirmacao == "Sim" or confirmacao == "sim":
            self.nome = nome
            LOGGER.info(
                "perfil_atualizado campo=nome user=%s",
                self.identificador,
            )
            print(f"Seu nome agora é: {self.nome}")
        else:
            print(f"Alteração não realizada, seu nome ainda é: {self.nome}, obrigado!")

    def mudar_idade(self, idade):
        if int(idade) < 16:
            raise ValueError(
                "Infelizmente você não tem idade para utilizar os serviços da Danilo Bank"
            )

        print(f"Confirme o ajuste da sua idade: {idade}")
        print("1-Sim 2-Não")
        confirmacao = str(input())
        if confirmacao == "1" or confirmacao == "Sim" or confirmacao == "sim":
            self.idade = int(idade)
            LOGGER.info(
                "perfil_atualizado campo=idade user=%s nova_idade=%s",
                self.identificador,
                idade,
            )
            print(f"Sua idade agora é: {self.idade}")
        else:
            print(f"Alteração não realizada, sua idade ainda é: {self.idade}, obrigado!")
