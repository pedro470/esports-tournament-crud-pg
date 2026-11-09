# Esports Tournament Management CRUD — Python & PostgreSQL

Sistema de gerenciamento de campeonatos e partidas de e-Sports desenvolvido em **Python** com persistência relacional em **PostgreSQL (`psycopg2`)**, arquitetura separada em camadas (`interfaces/` e `services/`), autenticação criptografada com `bcrypt`, máquina de estados de negócio e suíte de testes funcionais ponta a ponta com suporte a `--dry-run` transacional.

---

## Principais Funcionalidades & Regras de Negócio

1. **Arquitetura em Camadas (`interfaces/` + `services/` + `db.py`):**
   - Separação clara entre a interface de interação CLI (`interfaces/*_interface.py`), a camada de regras de negócio e validações cruzadas (`services/service_*.py`) e o módulo de conexão parametrizada ao PostgreSQL (`db.py`).
2. **Controle de Acesso e Segurança (`service_usuario.py`):**
   - Cadastro e autenticação de usuários com *hashing* seguro de senhas via `bcrypt` e controle de permissões por papel (`organizador do torneio`, `chefe de equipe`, `jogador`).
3. **Máquina de Estados de Campeonatos (`service_torneio.py`, `service_jogo.py`, `service_resultado.py`):**
   - **Fase `aberto` (Organização):** Permite inscrição de equipes respeitando limites de vagas ($8$, $16$ ou $32$ equipes) e limites mínimo/máximo de jogadores por equipe ($6$ a $10$ integrantes).
   - **Fase `em andamento`:** Bloqueia novas inscrições ou edições estruturais no torneio; habilita o agendamento de confrontos (`jogos`), impedindo que equipes com partidas pendentes (sem resultado) agendem novos jogos.
   - **Fase `finalizado`:** Imutabilidade de resultados lançados e encerramento automático do torneio quando o campeão atinge o número de vitórias da chave ($\log_2 N$).
4. **Testes Automatizados de Fluxo com Proxy Transacional (`tests/test_flow.py`):**
   - Script de teste ponta a ponta que valida criação de organizador, abertura de torneio, inscrição de 8 equipes, bloqueio de partidas concorrentes, registro de placares e transição automática para `finalizado`.
   - Suporta flag `--dry-run` através de um *Connection Proxy* (`_ProxyConn`) que intercepta `.commit()` e `.close()` nos serviços e executa `rollback` completo ao término do teste sem sujar o banco de dados.

---

## Stack Tecnológica

- **Linguagem:** Python 3.10+
- **Banco de Dados:** PostgreSQL (`psycopg2-binary`) — Consultas SQL parametrizadas (prevenção contra *SQL Injection*) e controle transacional (`commit` / `rollback`)
- **Segurança & Configuração:** `bcrypt` (hash de senhas), `python-dotenv`

---

## Estrutura do Projeto

```text
├── interfaces/                # Camada de apresentação (Menus CLI por domínio)
│   ├── usuarios_interface.py
│   ├── equipes_interface.py
│   ├── jogador_interface.py
│   ├── torneios_interface.py
│   ├── torneio_equipes_interface.py
│   ├── jogos_interface.py
│   └── resultados_interface.py
├── services/                  # Camada de regras de negócio, validações e SQL
│   ├── service_usuario.py
│   ├── service_equipe.py
│   ├── service_jogadores.py
│   ├── service_torneio.py
│   ├── service_jogo.py
│   └── service_resultado.py
├── scripts/
│   └── BD_Jogos.sql           # Script DDL de criação das tabelas relacionais
├── tests/
│   └── test_flow.py           # Teste funcional automatizado (com modo --dry-run)
├── db.py                      # Fábrica de conexões PostgreSQL via variáveis de ambiente
├── main.py                    # Ponto de entrada da aplicação
├── .env.example               # Template de configuração do banco
└── requirements.txt
```

---

## Como Executar

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar banco PostgreSQL
copy .env.example .env
# Crie o banco no PostgreSQL e execute o script DDL: scripts/BD_Jogos.sql

# 3. Rodar a suíte de testes ponta a ponta (em modo dry-run, sem sujar o banco)
python tests/test_flow.py --dry-run

# 4. Iniciar a aplicação interativa
python main.py
```
