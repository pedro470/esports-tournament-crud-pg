from db import criar_conexao
import services.service_torneio as service_torneio


def listar_jogos(id_torneio):
	conn = criar_conexao()
	cursor = conn.cursor()
	try:
		cursor.execute('SELECT id_jogos, id_equipe1, id_equipe2, data_hora FROM jogos WHERE id_torneio=%s ORDER BY id_jogos', (id_torneio,))
		jogos = cursor.fetchall()
		return jogos
	except Exception as e:
		print(f'Erro ao listar jogos: {e}')
		return []
	finally:
		cursor.close()
		conn.close()


def _existe_jogo(id_jogo):
	conn = criar_conexao()
	cursor = conn.cursor()
	cursor.execute('SELECT 1 FROM jogos WHERE id_jogos=%s', (id_jogo,))
	res = cursor.fetchone()
	cursor.close()
	conn.close()
	return res is not None


def _jogo_possui_resultado(id_jogo):
	conn = criar_conexao()
	cursor = conn.cursor()
	cursor.execute('SELECT 1 FROM resultado WHERE id_jogo=%s', (id_jogo,))
	res = cursor.fetchone()
	cursor.close()
	conn.close()
	return res is not None


def _torneio_estado(id_torneio):
	conn = criar_conexao()
	cursor = conn.cursor()
	cursor.execute('SELECT estado FROM torneios WHERE id_torneio=%s', (id_torneio,))
	res = cursor.fetchone()
	cursor.close()
	conn.close()
	if not res:
		return None
	return res[0]


def _equipe_inscrita_no_torneio(id_torneio, id_equipe):
	conn = criar_conexao()
	cursor = conn.cursor()
	cursor.execute('SELECT 1 FROM torneio_equipe WHERE torneio_id=%s AND equipe_id=%s', (id_torneio, id_equipe))
	res = cursor.fetchone()
	cursor.close()
	conn.close()
	return res is not None


def _equipe_foi_derrotada(id_torneio, id_equipe):
	# Verifica se a equipe já perdeu algum jogo nesse torneio
	conn = criar_conexao()
	cursor = conn.cursor()
	sql = (
		"SELECT 1 FROM jogos j JOIN resultado r ON j.id_jogos = r.id_jogo "
		"WHERE j.id_torneio=%s AND ( (j.id_equipe1=%s AND r.pontos_equipe1 < r.pontos_equipe2) "
		"OR (j.id_equipe2=%s AND r.pontos_equipe2 < r.pontos_equipe1) ) LIMIT 1"
	)
	cursor.execute(sql, (id_torneio, id_equipe, id_equipe))
	res = cursor.fetchone()
	cursor.close()
	conn.close()
	return res is not None


def _ultimo_jogo_da_equipe(id_torneio, id_equipe):
	conn = criar_conexao()
	cursor = conn.cursor()
	cursor.execute('SELECT id_jogos FROM jogos WHERE id_torneio=%s AND (id_equipe1=%s OR id_equipe2=%s) ORDER BY id_jogos DESC LIMIT 1', (id_torneio, id_equipe, id_equipe))
	res = cursor.fetchone()
	cursor.close()
	conn.close()
	return res[0] if res else None


def criar_jogo(id_torneio, id_equipe1, id_equipe2, data_hora):
	# Validações
	estado = _torneio_estado(id_torneio)
	if estado is None:
		print('Torneio não encontrado.')
		return False
	if estado != 'em andamento':
		print('Só é possível criar jogos em torneios em andamento.')
		return False

	if id_equipe1 == id_equipe2:
		print('As equipes devem ser diferentes.')
		return False

	if not _equipe_inscrita_no_torneio(id_torneio, id_equipe1) or not _equipe_inscrita_no_torneio(id_torneio, id_equipe2):
		print('Uma ou ambas as equipes não estão inscritas nesse torneio.')
		return False

	ultimo1 = _ultimo_jogo_da_equipe(id_torneio, id_equipe1)
	ultimo2 = _ultimo_jogo_da_equipe(id_torneio, id_equipe2)
	if (ultimo1 is not None and not _jogo_possui_resultado(ultimo1)) or (ultimo2 is not None and not _jogo_possui_resultado(ultimo2)    ):
		print('Não é possível criar um novo jogo antes de anexar o resultado do jogo anterior das equipes.')
		return False

	# Equipes que já foram derrotadas não podem ter novo jogo
	if _equipe_foi_derrotada(id_torneio, id_equipe1) or _equipe_foi_derrotada(id_torneio, id_equipe2):
		print('Uma das equipes já foi derrotada nesse torneio e não pode mais jogar.')
		return False

	try:
		conn = criar_conexao()
		cursor = conn.cursor()
		cursor.execute('INSERT INTO jogos (id_torneio, id_equipe1, id_equipe2, data_hora) VALUES (%s, %s, %s, %s)',
					   (id_torneio, id_equipe1, id_equipe2, data_hora))
		conn.commit()
		print('Jogo criado com sucesso.')
		return True
	except Exception as e:
		if conn:
			conn.rollback()
		print(f'Erro ao criar jogo: {e}')
		return False
	finally:
		if 'cursor' in locals():
			cursor.close()
		if 'conn' in locals():
			conn.close()


def atualizar_jogo(id_jogo, id_equipe1=None, id_equipe2=None, data_hora=None):
	if not _existe_jogo(id_jogo):
		print('Jogo não encontrado.')
		return False
	if _jogo_possui_resultado(id_jogo):
		print('Não é possível atualizar um jogo que já possui resultado.')
		return False

	updates = []
	params = []
	if id_equipe1 is not None:
		updates.append('id_equipe1=%s')
		params.append(id_equipe1)
	if id_equipe2 is not None:
		updates.append('id_equipe2=%s')
		params.append(id_equipe2)
	if data_hora is not None:
		updates.append('data_hora=%s')
		params.append(data_hora)

	if not updates:
		print('Nenhum campo para atualizar.')
		return False

	params.append(id_jogo)
	sql = f"UPDATE jogos SET {', '.join(updates)} WHERE id_jogos=%s"
	try:
		conn = criar_conexao()
		cursor = conn.cursor()
		cursor.execute(sql, tuple(params))
		conn.commit()
		print('Jogo atualizado com sucesso.')
		return True
	except Exception as e:
		if conn:
			conn.rollback()
		print(f'Erro ao atualizar jogo: {e}')
		return False
	finally:
		if 'cursor' in locals():
			cursor.close()
		if 'conn' in locals():
			conn.close()


def deletar_jogo(id_jogo):
	if not _existe_jogo(id_jogo):
		print('Jogo não encontrado.')
		return False
	if _jogo_possui_resultado(id_jogo):
		print('Não é possível deletar um jogo que já possui resultado.')
		return False

	try:
		conn = criar_conexao()
		cursor = conn.cursor()
		cursor.execute('DELETE FROM jogos WHERE id_jogos=%s', (id_jogo,))
		if cursor.rowcount == 0:
			print('Jogo não encontrado.')
			return False
		conn.commit()
		print('Jogo deletado com sucesso.')
		return True
	except Exception as e:
		if conn:
			conn.rollback()
		print(f'Erro ao deletar jogo: {e}')
		return False
	finally:
		if 'cursor' in locals():
			cursor.close()
		if 'conn' in locals():
			conn.close()

