import csv

def gerar_extrato(conta):
    try:
        with open("extrato_danilo_bank.csv", "w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(["===== EXTRATO DANILO BANK ====="])

            escritor.writerow(["tipo", "valor", "horario_utc"])


            extrato = conta.exportar_extrato()

            for movimentacao in extrato:
                horario_formatado = movimentacao["horario_utc"].strftime("%d/%m/%Y %H:%M:%S UTC")
                escritor.writerow([
                    movimentacao["tipo"],
                    movimentacao["valor"],
                    horario_formatado
                ])

            print("Extrato exportado com sucesso.")
            escritor.writerow(["===================================="])
    except PermissionError as err:
        print(f"Você não tem as permissões necessárias. {err}")
    except FileNotFoundError as err:
        print(f"Arquivo não encontrado. {err}")
    except csv.Error as err:
        print(f"Erro ao gerar o arquivo CSV. {err}")
    except Exception as err:
        print(f"Erro ao gerar documento.{err}")
