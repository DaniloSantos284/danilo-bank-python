def hello_world():
    print("\n")
    print("╔══════════════════════════════════════════════════════╗")
    print("║                                                      ║")
    print("║           Seja bem vindo ao Danilo Bank              ║")
    print("║       Desenvolvido como prática do curso DIO         ║")
    print("║                                                      ║")
    print("╚══════════════════════════════════════════════════════╝")
    print("")


def exibir_menu():
    print("\n📋 MENU PRINCIPAL")
    print("╔══════════════════════════════════════════════════════╗")
    print("║           Oque gostaria de fazer agora ?             ║")
    print("║                                                      ║")
    print("║   1. Depositar                                       ║")
    print("║   2. Sacar                                           ║")
    print("║   3. Ver extrato bancário                            ║")
    print("║   4. Informações da minha conta                      ║")
    print("║   5. Mudar Nome cadastrado                           ║")
    print("║   6. Mudar idade cadastrada                          ║")
    print("║   10. Sair do banco                                  ║")
    print("║                                                      ║")
    print("╚══════════════════════════════════════════════════════╝")
    print("")
    opcao_escolhida = int(input())
    return opcao_escolhida

def escolha_operacao(conta, user, opcao_escolhida):
    match opcao_escolhida:
        case 1:
            print("Digite o valor que deseja depositar: ")
            valor = float(input())
            conta.depositar(valor)
        case 2:
            print("Digite o valor que deseja sacar: ")
            valor = float(input())
            conta.sacar(valor)
        case 3:
            conta.exibir_extrato()
        case 4:
            user.informacoes_usuario()
        case 5:
            print(f"Nome atual: {user.nome}")
            novo_nome = str(input("Digite o novo nome: "))
            user.renomear_usuario(novo_nome)
        case 6:
            print(f"Idade atual: {user.idade}")
            nova_idade = str(input("Digite a idade correta: "))
            user.mudar_idade(nova_idade)
        case 10:
            print("Até mais")
        case _:
            print("Opção inválida, tente novamente com um número válido")