# Danilo Bank

Aplicação bancária simples executada no terminal, desenvolvida como projeto de estudo em Python. O programa cadastra um usuário, cria uma conta em memória e oferece operações bancárias e atualização de dados do usuário.

## Requisitos

- Python 3.10 ou superior.
- Nenhuma dependência externa obrigatória.

## Execução

No terminal, acesse a pasta do projeto e execute:

```bash
python sistema_principal.py
```

Informe nome e idade para criar o usuário. O cadastro exige idade mínima de 16 anos. O usuário recebe um identificador numérico aleatório de seis dígitos, que também identifica sua conta. O saldo inicial é R$ 0,00.

## Opções do menu

| Opção mostrada | Comportamento atual |
| --- | --- |
| 1. Depositar | Aceita apenas valores finitos maiores que zero. |
| 2. Sacar | Aceita apenas valores finitos maiores que zero e recusa valores acima do saldo. |
| 3. Ver extrato bancário | Exibe as movimentações e o saldo atual. |
| 4. Informações da minha conta | Exibe nome e idade do usuário. |
| 5. Mudar Nome cadastrado | Altera o nome após confirmação. |
| 6. Mudar idade cadastrada | Altera a idade após confirmação; exige idade mínima de 16 anos e salva a idade como inteiro. |
| 10. Sair do banco | Encerra o programa. |

Depósitos e saques com valor zero, negativo, `nan` ou infinito são rejeitados e não geram movimentações no extrato.

## Logs e horários

Ao iniciar, o programa cria a pasta `logs` e grava eventos em `logs/danilo_bank.log`. São registrados início e fim da sessão, depósitos, saques e alterações de perfil. Os registros incluem timestamps em UTC no formato ISO 8601, por exemplo `2026-09-25T15:49:08.685Z`.

O extrato guarda as movimentações apenas durante a execução atual. Cada movimento recebe um horário consciente de fuso armazenado em UTC. Na exibição, o horário é convertido para `America/Sao_Paulo` se a base de fusos estiver disponível; caso contrário, aparece em UTC. O arquivo de log permanece entre execuções, mas o saldo, o usuário e o extrato não são persistidos em arquivo ou banco de dados.

## Estrutura do projeto

```text
.
├── README.md
├── sistema_principal.py       # Inicialização e fluxo principal
├── models/
│   ├── __init__.py
│   ├── Conta.py               # Saldo, depósitos, saques e extrato
│   └── User.py                # Cadastro e dados do usuário
├── utils/
│   ├── __init__.py
│   ├── boas_vindas.py         # Apresentação, menu e operações
│   └── logging_config.py      # Logger e formatação dos horários UTC
└── logs/                      # Criada automaticamente; contém danilo_bank.log
```
