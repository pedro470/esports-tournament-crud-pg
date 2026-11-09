from db import criar_conexao        

#Deletar "FEITO"
def deletar_equipe(id_equipe):
    conn = criar_conexao()
    cursor = conn.cursor()
    query = 'DELETE FROM equipes WHERE id_equipe=%s'
    try:
       cursor.execute(query, [id_equipe])
       conn.commit()
       print(f'Equipe com ID {id_equipe} removida com sucesso!')
       resultado = True
    except Exception as e:
        conn.rollback()
        print(f'Erro ao deletar: {e}')
        resultado = False
    finally:
        cursor.close()
        conn.close()
    return resultado


#update "FAZER"
def update_equipe(nome, id_equipe, regiao) :
    conn = criar_conexao()
    cursor = conn.cursor()
    query = 'UPDATE equipes SET nome=%s, regiao=%s WHERE id_equipe=%s'
    cursor.execute(query, [nome, regiao, id_equipe])
    conn.commit()
    conn.close()


#inserir "FEITO"
def inserir_equipe(nome, regiao, quantidade_integrantes, lider, nome_lider):

    conn = criar_conexao()
    try:
        cursor = conn.cursor()
        query = 'INSERT INTO equipes(nome, regiao, quant_integrantes, lider, nome_lider) VALUES (%s, %s, %s, %s, %s)'
        cursor.execute(query, (nome, regiao, quantidade_integrantes, lider, nome_lider))
        conn.commit()
        print('Dados de equipes inserido com sucesso!')
    except Exception as e:
        print(f'Erro ao inserir equipe: {e}')
    finally:
        cursor.close()
        conn.close()


#Tabela mostrar "FEITO"
def ler_equipes(id_equipe=None):
    conn = criar_conexao()
    cursor = conn.cursor()
    if id_equipe:
        query = 'SELECT * FROM equipes e WHERE e.id_equipe=%s'
        cursor.execute(query, [id_equipe])
        conn.commit()
        resultado = cursor.fetchall()
    else:
        query = 'SELECT * FROM equipes e'
        cursor.execute(query)
        conn.commit()
        resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultado


def listar_torneios_da_equipe(id_equipe):
    conn = criar_conexao()
    cursor = conn.cursor()
    query = '''
        SELECT t.id_torneio, t.nome, t.data_inicio, t.data_fim
        FROM torneios t
        JOIN torneio_equipe te ON t.id_torneio = te.torneio_id
        JOIN equipes i ON te.equipe_id = i.id_equipe
        WHERE i.id_equipe = %s  
    '''
    cursor.execute(query, [id_equipe])
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados