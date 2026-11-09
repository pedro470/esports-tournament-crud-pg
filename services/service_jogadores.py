from db import criar_conexao


def inserir_jogador(nome, regiao, id_equipe):

    conn = criar_conexao()
    try:
        cursor = conn.cursor()
        query = 'INSERT INTO jogadores(nome, regiao, id_equipe) VALUES (%s, %s, %s)'
        cursor.execute(query, (nome, regiao, id_equipe))
        conn.commit()
        print('Jogador inserido com sucesso!')
    except Exception as e:
        print(f'Erro ao inserir: {e}')
    finally:
        cursor.close()
        conn.close()


def atualizar_jogador(id_jogador, nome, regiao):
    conn = criar_conexao()
    cursor = conn.cursor()

    try:
        query = "UPDATE jogadores SET nome=%s, regiao=%s WHERE id_jogador=%s"
        cursor.execute(query, [nome, regiao, id_jogador])
        conn.commit()
        print('Jogador Atualizado com Sucesso!')
    except Exception as e:
        conn.rollback()
        print(f'Erro ao atualizar jogador: {e}')
    finally:
        cursor.close()
        conn.close()


# Atualizar a EQUIPE do jogador
def atualizar_equipe_jogador(id_jogador, novo_id_equipe):
    conn = criar_conexao()
    cursor = conn.cursor()

    try:
        query = 'UPDATE jogadores SET id_equipe=%s WHERE id_jogador=%s'
        cursor.execute(query, (novo_id_equipe, id_jogador))
        conn.commit()
        print('Equipe do jogador atualizada!')
    except Exception as e:
        conn.rollback()
        print(f'Erro ao atualizar equipe: {e}')
    finally:
        cursor.close()
        conn.close()


# Listar os jogadores e suas equipes
def ler_jogadores(id_jogador=None):
    conn = criar_conexao()
    cursor = conn.cursor()

    try:
        if id_jogador is not None:
            query = 'SELECT * FROM jogadores j WHERE j.id_jogador=%s'
            cursor.execute(query, (id_jogador))
        else:
            query = 'SELECT * FROM jogadores j'
            cursor.execute(query)

        resultado = cursor.fetchall()
        return resultado
    except Exception as e:
        print(f'Erro ao ler jogadores: {e}')
        return []
    finally:
        cursor.close()
        conn.close()


def deletar_jogador(id_jogador):
    conn = criar_conexao()
    cursor = conn.cursor()
    query = 'DELETE FROM jogadores WHERE id_jogador=%s'
    try:
        cursor.execute(query, [id_jogador])
        conn.commit()
        print(f'Jogador com ID {id_jogador} removido com sucesso!')
        resultado = True
    except Exception as e:
        conn.rollback()
        print(f'Erro ao deletar jogador: {e}')
        resultado = False
    finally:
        cursor.close()
        conn.close()
    return resultado