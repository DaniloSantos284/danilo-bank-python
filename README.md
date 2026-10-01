# Danilo Bank

Aplicação bancária de terminal desenvolvida em Python como projeto de estudo. O sistema cadastra um usuário, cria uma conta em memória e permite realizar operações bancárias, consultar movimentações, atualizar dados cadastrais e exportar o extrato para CSV.

> **Aviso:** este é um projeto educacional. Ele não possui os controles de segurança, persistência e precisão monetária necessários para uso bancário real.

## Funcionalidades

- Cadastro de usuário com idade mínima de 16 anos.
- Geração automática de um identificador numérico de seis dígitos para o usuário e a conta.
- Depósitos e saques com validação de valores.
- Consulta de saldo e do extrato da sessão atual.
- Registro das movimentações com data e hora em UTC.
- Exibição dos horários do extrato no fuso `America/Sao_Paulo`, quando a base de fusos está disponível.
- Alteração de nome e idade mediante confirmação.
- Exportação das movimentações para o arquivo `extrato_danilo_bank.csv`.
- Registro de eventos da aplicação em `logs/danilo_bank.log`.

## Requisitos

- Python 3.10 ou superior, devido ao uso de `match`/`case`.
- Nenhuma dependência externa obrigatória.

## Como executar

No terminal, acesse a pasta do projeto e execute:

```bash
python sistema_principal.py
```

Informe o nome e a idade para criar o usuário. O saldo inicial da conta é `R$ 0,00`.

## Opções do menu

| Opção | Ação | Comportamento |
| --- | --- | --- |
| 1 | Depositar | Aceita somente valores numéricos finitos maiores que zero. |
| 2 | Sacar | Aceita somente valores numéricos finitos maiores que zero e não permite sacar acima do saldo. |
| 3 | Ver extrato bancário | Exibe as movimentações da sessão e o saldo atual. |
| 4 | Informações da minha conta | Exibe o nome e a idade do usuário. |
| 5 | Mudar nome cadastrado | Solicita confirmação antes de alterar o nome. |
| 6 | Mudar idade cadastrada | Solicita confirmação, exige idade mínima de 16 anos e armazena a idade como número inteiro. |
| 7 | Exportar movimentação (CSV) | Exporta as movimentações da sessão para `extrato_danilo_bank.csv`. |
| 10 | Sair do banco | Registra o encerramento da sessão e finaliza o programa. |

Valores iguais a zero, negativos, `nan` ou infinitos são rejeitados em depósitos e saques e não geram movimentações no extrato.

## Arquivos gerados

### Extrato CSV

A opção 7 cria o arquivo `extrato_danilo_bank.csv` no diretório em que o programa foi iniciado. O documento contém o tipo, o valor e o horário em UTC de cada movimentação realizada na sessão atual.

O arquivo é recriado a cada exportação. Portanto, uma nova exportação substitui o conteúdo exportado anteriormente.

### Logs

Ao iniciar, a aplicação cria a pasta `logs` quando necessário e grava eventos em `logs/danilo_bank.log`. São registrados o início e o fim da sessão, depósitos, saques e alterações de perfil. Os timestamps usam UTC no formato ISO 8601, por exemplo: `2026-09-25T15:49:08.685Z`.

## Persistência e horários

O usuário, o saldo e o extrato permanecem somente na memória durante a execução atual. Ao encerrar o programa, esses dados são perdidos. Apenas o arquivo de log e os extratos CSV já exportados permanecem no disco.

Cada movimentação é armazenada em UTC. Na consulta pelo terminal, o horário é convertido para `America/Sao_Paulo`; se a base de fusos não estiver disponível no ambiente, o sistema mantém a exibição em UTC. No CSV, os horários são sempre exportados em UTC.

## Estrutura do projeto

```text
.
├── .gitignore
├── README.md
├── sistema_principal.py       # Inicialização e fluxo principal
├── models/
│   ├── __init__.py
│   ├── Conta.py               # Saldo, depósitos, saques e extrato
│   └── User.py                # Cadastro e dados do usuário
├── utils/
│   ├── __init__.py
│   ├── boas_vindas.py         # Apresentação, menu e operações
│   ├── gerador_arquivos.py    # Exportação do extrato para CSV
│   └── logging_config.py      # Configuração e formatação dos logs
└── logs/                      # Diretório de logs criado pela aplicação
```

## Limitações atuais

- Não há banco de dados nem recuperação de sessões anteriores.
- Os valores monetários usam `float`, que não é indicado para cálculos financeiros reais.
- O CSV contém as movimentações, mas não inclui os dados do titular nem o saldo final.
- Não há autenticação, testes automatizados ou interface gráfica/web.
