import csv

from models.Conta import exportar_extrato as extrato

def gerar_extrato():

    with open("extrato_danilo_bank.csv", "w", newline="", encoding="utf-8") as arquivo
    escritor = csv.writer(arquivo)

    escritor.writerow("\n===== EXTRATO DANILO BANK =====")

    escritor.writelines(extrato)

    escritor.writerow("====================================\n")