from db import criar_conexao
from datetime import datetime


# Serviço de torneios
def listar_torneios():
    conn = criar_conexao()
    cursor = conn.cursor()
    sql = "SELECT id_torneio, nome, data_inicio, data_fim, minimo_jogadores_equipe, maximo_jogadores_equipe, numero_equipes, organizador_id FROM torneios"
    cursor.execute(sql)
    torneios = cursor.fetchall()
    cursor.close()
    conn.close()
    return torneios


def _existe_torneio(id_torneio):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM torneios WHERE id_torneio=%s", (id_torneio,))
    res = cursor.fetchone()
    cursor.close()
    conn.close()
    return res is not None


def _torneio_iniciado(id_torneio):
    # Retorna True se data_inicio <= now()
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT estado FROM torneios WHERE id_torneio=%s", (id_torneio,))
    res = cursor.fetchone()
    cursor.close()
    conn.close()
    if res is None:
        return None
    return res[0] != 'aberto'


def _usuario_eh_organizador(organizador_id):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT tipo_usuario FROM usuarios WHERE id_usuario=%s", (organizador_id,))
    res = cursor.fetchone()
    cursor.close()
    conn.close()
    if res is None:
        return False
    return res[0] == 'organizador do torneio'


def criar_torneio(nome, data_inicio, data_fim, minimo_jogadores, maximo_jogadores, numero_equipes, organizador_id):
    # validações básicas
    if numero_equipes not in (8, 16, 32):
        print('Erro: numero_equipes deve ser 8, 16 ou 32')
        return False
    if minimo_jogadores <= 5:
        print('Erro: minimo_jogadores deve ser maior que 5')
        return False
    if maximo_jogadores > 10:
        print('Erro: maximo_jogadores deve ser menor ou igual a 10')
        return False
    if minimo_jogadores > maximo_jogadores:
        print('Erro: minimo_jogadores não pode ser maior que maximo_jogadores')
        return False

    if not _usuario_eh_organizador(organizador_id):
        print('Erro: somente usuários do tipo "organizador do torneio" podem criar torneios')
        return False

    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        # data_inicio e data_fim podem ser strings ou datetime; deixar o adaptador do driver cuidar
        sql = ("INSERT INTO torneios (nome, data_inicio, data_fim, minimo_jogadores_equipe, maximo_jogadores_equipe, numero_equipes, organizador_id) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s)")
        cursor.execute(sql, (nome, data_inicio, data_fim, minimo_jogadores, maximo_jogadores, numero_equipes, organizador_id))
        conn.commit()
        print('Torneio criado com sucesso!')
        return True
    except Exception as e:
        if conn:
            conn.rollback()
        print(f'Erro ao criar torneio: {e}')
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def atualizar_torneio_campos(id_torneio, numero_equipes=None, minimo_jogadores=None, maximo_jogadores=None):
    if not _existe_torneio(id_torneio):
        print('Torneio não encontrado.')
        return False
    iniciado = _torneio_iniciado(id_torneio)
    if iniciado is None:
        print('Torneio não encontrado.')
        return False
    if iniciado:
        print('Não é possível alterar campos de um torneio já iniciado.')
        return False

    updates = []
    params = []
    if numero_equipes is not None:
        if numero_equipes not in (8, 16, 32):
            print('Erro: numero_equipes deve ser 8, 16 ou 32')
            return False
        updates.append('numero_equipes=%s')
        params.append(numero_equipes)
    if minimo_jogadores is not None:
        if minimo_jogadores <= 5:
            print('Erro: minimo_jogadores deve ser maior que 5')
            return False
        updates.append('minimo_jogadores_equipe=%s')
        params.append(minimo_jogadores)
    if maximo_jogadores is not None:
        if maximo_jogadores > 10:
            print('Erro: maximo_jogadores deve ser menor ou igual a 10')
            return False
        updates.append('maximo_jogadores_equipe=%s')
        params.append(maximo_jogadores)

    if not updates:
        print('Nenhum campo para atualizar.')
        return False

    params.append(id_torneio)
    sql = f'UPDATE torneios SET {", ".join(updates)} WHERE id_torneio=%s'
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        cursor.execute(sql, tuple(params))
        conn.commit()
        print('Torneio atualizado com sucesso.')
        return True
    except Exception as e:
        if conn:
            conn.rollback()
        print(f'Erro ao atualizar torneio: {e}')
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def deletar_torneio(id_torneio):
    if not _existe_torneio(id_torneio):
        print('Torneio não encontrado.')
        return False
    iniciado = _torneio_iniciado(id_torneio)
    if iniciado is None:
        print('Torneio não encontrado.')
        return False
    if iniciado:
        print('Não é possível deletar um torneio já iniciado.')
        return False

    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM torneios WHERE id_torneio=%s', (id_torneio,))
        conn.commit()
        print('Torneio deletado com sucesso.')
        return True
    except Exception as e:
        if conn:
            conn.rollback()
        print(f'Erro ao deletar torneio: {e}')
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def start_torneio(id_torneio, quant_equipes):
    if not _existe_torneio(id_torneio):
        print('Torneio não encontrado.')
        return False
    iniciado = _torneio_iniciado(id_torneio)
    if iniciado is None:
        print('Torneio não encontrado.')
        return False
    if iniciado:
        print('Torneio já foi iniciado.')
        return False

    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        equipes_inscritas = _count_equipes_inscritas(id_torneio)
        if equipes_inscritas != quant_equipes:
            print(f'Número de equipes inscritas ({equipes_inscritas}) não é o esperado ({quant_equipes}).')
            return False
        cursor.execute("UPDATE torneios SET estado = 'em andamento' WHERE id_torneio=%s", (id_torneio,))
        conn.commit()
        print('Torneio iniciado com sucesso.')
        return True
    except Exception as e:
        if conn:
            conn.rollback()
        print(f'Erro ao iniciar torneio: {e}')
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# TODO: Criar tabela de relacionamento entre torneios e equipes (torneio_equipe)
# A tabela deve mapear quais equipes estão inscritas em cada torneio e
# permitir gerar chaves e confrontos quando o torneio for iniciado.


def listar_equipes_inscritas(id_torneio):
    if not _existe_torneio(id_torneio):
        print('Torneio não encontrado.')
        return []
    conn = criar_conexao()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT e.id_equipe, e.nome, e.regiao FROM torneio_equipe te JOIN equipes e ON te.equipe_id = e.id_equipe WHERE te.torneio_id=%s', (id_torneio,))
        equipes = cursor.fetchall()
        return equipes
    except Exception as e:
        print(f'Erro ao listar equipes inscritas: {e}')
        return []
    finally:
        cursor.close()
        conn.close()


def _equipe_existe(id_equipe):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM equipes WHERE id_equipe=%s', (id_equipe,))
    res = cursor.fetchone()
    cursor.close()
    conn.close()
    return res is not None


def _count_equipes_inscritas(id_torneio):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM torneio_equipe WHERE torneio_id=%s', (id_torneio,))
    res = cursor.fetchone()
    cursor.close()
    conn.close()
    return res[0] if res else 0


def inscrever_equipe(id_torneio, id_equipe):
    if not _existe_torneio(id_torneio):
        print('Torneio não encontrado.')
        return False
    if not _equipe_existe(id_equipe):
        print('Equipe não encontrada.')
        return False
    iniciado = _torneio_iniciado(id_torneio)
    if iniciado is None:
        print('Torneio não encontrado.')
        return False
    if iniciado:
        print('Não é possível inscrever equipe em torneio já iniciado.')
        return False

    conn = criar_conexao()
    cursor = conn.cursor()
    try:
        # verifica se já inscrita
        cursor.execute('SELECT 1 FROM torneio_equipe WHERE torneio_id=%s AND equipe_id=%s', (id_torneio, id_equipe))
        if cursor.fetchone():
            print('Equipe já está inscrita nesse torneio.')
            return False

        # verifica limite de equipes do torneio
        cursor.execute('SELECT numero_equipes FROM torneios WHERE id_torneio=%s', (id_torneio,))
        numero = cursor.fetchone()
        if not numero:
            print('Torneio não encontrado (checagem interna).')
            return False
        numero = numero[0]
        cursor.execute('SELECT COUNT(*) FROM torneio_equipe WHERE torneio_id=%s', (id_torneio,))
        atual = cursor.fetchone()[0]
        if atual >= numero:
            print('Torneio já atingiu o número máximo de equipes inscritas.')
            return False

        cursor.execute('INSERT INTO torneio_equipe (torneio_id, equipe_id) VALUES (%s, %s)', (id_torneio, id_equipe))
        conn.commit()
        print('Equipe inscrita com sucesso no torneio.')
        return True
    except Exception as e:
        if conn:
            conn.rollback()
        print(f'Erro ao inscrever equipe: {e}')
        return False
    finally:
        cursor.close()
        conn.close()


def remover_inscricao(id_torneio, id_equipe):
    if not _existe_torneio(id_torneio):
        print('Torneio não encontrado.')
        return False
    iniciado = _torneio_iniciado(id_torneio)
    if iniciado is None:
        print('Torneio não encontrado.')
        return False
    if iniciado:
        print('Não é possível remover inscrição de torneio já iniciado.')
        return False

    conn = criar_conexao()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM torneio_equipe WHERE torneio_id=%s AND equipe_id=%s', (id_torneio, id_equipe))
        if cursor.rowcount == 0:
            print('Inscrição não encontrada.')
            return False
        conn.commit()
        print('Inscrição removida com sucesso.')
        return True
    except Exception as e:
        if conn:
            conn.rollback()
        print(f'Erro ao remover inscrição: {e}')
        return False
    finally:
        cursor.close()
        conn.close()

