DO $$
BEGIN
    -- Verifica se o tipo 'tipo_usuario_enum' já não existe
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'tipo_usuario_enum') THEN
        -- Se não existir, ele cria
        CREATE TYPE tipo_usuario_enum AS ENUM (
            'chefe de equipe',
            'organizador do torneio',
            'usuário comum'
        );
    END IF;
END
$$;

DO $$
BEGIN
    -- Verifica se o tipo 'tipo_usuario_enum' já não existe
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'estado_torneio') THEN
        -- Se não existir, ele cria
        CREATE TYPE estado_torneio AS ENUM (
            'aberto',
            'em andamento',
            'finalizado'
        );
    END IF;
END
$$;
-- Tabela de Usuários
CREATE TABLE IF NOT EXISTS usuarios (
	id_usuario SERIAL PRIMARY KEY,
	nome VARCHAR(150) NOT NULL,
	email VARCHAR(255) UNIQUE NOT NULL,
	senha VARCHAR(255) NOT NULL,
	tipo_usuario tipo_usuario_enum NOT NULL,
	data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Torneios
CREATE TABLE IF NOT EXISTS torneios (
	id_torneio SERIAL PRIMARY KEY,
	nome VARCHAR(250) NOT NULL,
	data_inicio TIMESTAMP WITH TIME ZONE NOT NULL,
	data_fim TIMESTAMP WITH TIME ZONE NOT NULL,
	minimo_jogadores_equipe INTEGER CHECK (minimo_jogadores_equipe > 5),
	maximo_jogadores_equipe INTEGER CHECK (maximo_jogadores_equipe <= 10),
	-- Os torneios tem apenas um grupo de equipes, devendo ser uma potência de 2 entre 8 e 32
	numero_equipes INTEGER CHECK (numero_equipes = 8 OR numero_equipes = 16 OR numero_equipes = 32),
    estado estado_torneio NOT NULL DEFAULT 'aberto',
    organizador_id INTEGER NOT NULL,
    CONSTRAINT fk_organizador_torneio FOREIGN KEY (organizador_id)
        REFERENCES usuarios (id_usuario)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Tabela de Equipes (já com os campos de liderança)
CREATE TABLE IF NOT EXISTS equipes (
    id_equipe SERIAL PRIMARY KEY,
    nome VARCHAR(250) NOT NULL,
    regiao VARCHAR(100),
    quant_integrantes INTEGER CHECK (quant_integrantes >= 0),
    nome_lider VARCHAR(255), 
    lider BOOLEAN NOT NULL  
);

-- Tabela de Jogadores
CREATE TABLE IF NOT EXISTS jogadores (
    id_jogador SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    regiao VARCHAR(100),
    id_equipe INTEGER NOT NULL,
    CONSTRAINT fk_equipe_jogador FOREIGN KEY (id_equipe)
        REFERENCES equipes (id_equipe)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Tabela de Jogos
CREATE TABLE IF NOT EXISTS jogos (
    id_jogos SERIAL PRIMARY KEY,
    id_torneio INTEGER NOT NULL,
    id_equipe1 INTEGER NOT NULL,
    id_equipe2 INTEGER NOT NULL,
    data_hora TIMESTAMP WITH TIME ZONE NOT NULL,
    CONSTRAINT fk_jogos_equipes FOREIGN KEY (id_equipe1)
        REFERENCES equipes (id_equipe)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_jogos_equipes2 FOREIGN KEY (id_equipe2)
        REFERENCES equipes (id_equipe)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_jogos_torneio FOREIGN KEY (id_torneio)
        REFERENCES torneios (id_torneio)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Tabela de Resultados
CREATE TABLE IF NOT EXISTS resultado (
    id_resultado SERIAL PRIMARY KEY,
    id_jogo INTEGER UNIQUE NOT NULL,
    duracao_partida INTERVAL,
    pontos_equipe1 INTEGER,
    pontos_equipe2 INTEGER,
    CONSTRAINT fk_resultado_jogo FOREIGN KEY (id_jogo)
        REFERENCES jogos (id_jogos)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Tabela de relacionamento entre torneios e equipes
CREATE TABLE IF NOT EXISTS torneio_equipe (
    id_torneio_equipe SERIAL PRIMARY KEY,
    torneio_id INTEGER NOT NULL,
    equipe_id INTEGER NOT NULL,
    CONSTRAINT fk_torneio FOREIGN KEY (torneio_id)
        REFERENCES torneios (id_torneio)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_equipe FOREIGN KEY (equipe_id)
        REFERENCES equipes (id_equipe)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT uq_torneio_equipe UNIQUE (torneio_id, equipe_id)
);