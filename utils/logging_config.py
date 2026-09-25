"""Configuração centralizada dos logs da aplicação."""

import logging
from datetime import datetime, timezone
from pathlib import Path


class FormatadorUTC(logging.Formatter):
    """Formata datas de log como ISO 8601 em UTC, sem ambiguidade de fuso."""

    def formatTime(self, record, datefmt=None):
        instante = datetime.fromtimestamp(record.created, tz=timezone.utc)
        return instante.isoformat(timespec="milliseconds").replace("+00:00", "Z")


def obter_logger() -> logging.Logger:
    """Retorna o logger do banco, evitando handlers duplicados em novos imports."""
    logger = logging.getLogger("danilo_bank")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if logger.handlers:
        return logger

    diretorio_logs = Path(__file__).resolve().parent.parent / "logs"
    diretorio_logs.mkdir(exist_ok=True)

    handler = logging.FileHandler(diretorio_logs / "danilo_bank.log", encoding="utf-8")
    handler.setFormatter(
        FormatadorUTC("%(asctime)s %(levelname)s %(name)s: %(message)s")
    )
    logger.addHandler(handler)
    return logger
