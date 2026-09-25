from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from utils.logging_config import obter_logger

from math import isfinite

LOGGER = obter_logger()


class Conta:
    def __init__(self, titular, agencia="0800"):
        self.titular = titular
        self.identificador = titular.identificador
        self.saldo = 0.0
        self.extrato = []

    def _registrar_movimentacao(self, tipo, valor):
        """Mantém o instante em UTC; a conversão para horário local é só de exibição."""
        horario_utc = datetime.now(timezone.utc)
        self.extrato.append(
            {"tipo": tipo, "valor": valor, "horario_utc": horario_utc}
        )
        LOGGER.info(
            "movimentacao=%s conta=%s valor=%.2f horario_utc=%s",
            tipo.lower(),
            self.identificador,
            valor,
            horario_utc.isoformat().replace("+00:00", "Z"),
        )

    @staticmethod
    def _formatar_horario_extrato(horario_utc):
        try:
            horario_local = horario_utc.astimezone(ZoneInfo("America/Sao_Paulo"))
            return horario_local.strftime("%d/%m/%Y %H:%M:%S %Z")
        except ZoneInfoNotFoundError:
            # Em instalações sem a base de fusos, mantém a informação correta em UTC.
            return horario_utc.strftime("%d/%m/%Y %H:%M:%S UTC")

    def depositar(self, valor):
        valor = float(valor)

        if self.titular is None:
            print(
                "Não foi possível realizar o depósito, você não tem uma seção válida."
            )
        elif not isfinite(valor) or valor <= 0:
            print("Insira um valor válido para depósito")
            return None
        else:
            self.saldo += valor
            self._registrar_movimentacao("Depósito", valor)
            print(f"Seu novo saldo é de: R$ {self.saldo:.2f}")

    def sacar(self, valor):
        valor = float(valor)

        if valor > self.saldo:
            raise ValueError(
                "Valor de saque maior que limite, tente novamente com um valor válido"
            )
        elif not isfinite(valor) or valor <= 0:
            raise ValueError(
                "Adicione um valor válido para saque"
            )
        elif self.titular is None:
            print(
                "Não foi possível realizar o depósito, você não tem uma seção válida."
            )
        else:
            self.saldo -= valor
            self._registrar_movimentacao("Saque", valor)
            print(f"Seu novo saldo é de: {self.saldo}")

    def exibir_extrato(self):
        print("\n===== EXTRATO DANILO BANK =====")

        if not self.extrato:
            print("Não foram realizadas movimentações.")
        else:
            for operacao in self.extrato:
                horario = self._formatar_horario_extrato(operacao["horario_utc"])
                print(
                    f"{horario} | {operacao['tipo']}: "
                    f"R$ {operacao['valor']:.2f}"
                )

        print(f"Saldo atual: R$ {self.saldo:.2f}")

        print("====================================\n")
