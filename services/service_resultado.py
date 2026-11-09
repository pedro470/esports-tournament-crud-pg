from db import criar_conexao
import math


def _existe_resultado_por_jogo(id_jogo):
	conn = criar_conexao()
	cursor = conn.cursor()
	cursor.execute('SELECT 1 FROM resultado WHERE id_jogo=%s', (id_jogo,))
	res = cursor.fetchone()
	cursor.close()
	conn.close()
	return res is not None


def criar_resultado(id_jogo, duracao_partida, pontos_equipe1, pontos_equipe2):
	conn = criar_conexao()
	cursor = conn.cursor()
	try:
		# Verifica existência do jogo
		cursor.execute('SELECT id_torneio, id_equipe1, id_equipe2 FROM jogos WHERE id_jogos=%s', (id_jogo,))
		jogo = cursor.fetchone()
		if not jogo:
			print('Jogo não encontrado.')
			return False
		id_torneio = jogo[0]

		# Verifica se já existe resultado
		if _existe_resultado_por_jogo(id_jogo):
			print('Já existe resultado para esse jogo.')
			return False

		# Não aceitar empates — regra de negócio definida para fim de campeonato
		if pontos_equipe1 == pontos_equipe2:
			print('Empates não são permitidos. Informe um vencedor.')
			return False

		cursor.execute('INSERT INTO resultado (id_jogo, duracao_partida, pontos_equipe1, pontos_equipe2) VALUES (%s, %s, %s, %s)',
					   (id_jogo, duracao_partida, pontos_equipe1, pontos_equipe2))
		conn.commit()

		# Determinar vencedor
		if pontos_equipe1 > pontos_equipe2:
			vencedor_col = 'id_equipe1'
			vencedor_id = jogo[1]
		else:
			vencedor_col = 'id_equipe2'
			vencedor_id = jogo[2]

		# Contabilizar vitórias do vencedor no torneio
		sql_vitorias = (
			"SELECT COUNT(*) FROM resultado r JOIN jogos j ON r.id_jogo = j.id_jogos "
			"WHERE j.id_torneio=%s AND ((r.pontos_equipe1 > r.pontos_equipe2 AND j.id_equipe1=%s) "
			"OR (r.pontos_equipe2 > r.pontos_equipe1 AND j.id_equipe2=%s))"
		)
		cursor.execute(sql_vitorias, (id_torneio, vencedor_id, vencedor_id))
		wins = cursor.fetchone()[0]

		# Buscar número de equipes do torneio e verificar condição de término
		cursor.execute('SELECT numero_equipes FROM torneios WHERE id_torneio=%s', (id_torneio,))
		num = cursor.fetchone()
		if num and num[0]:
			numero_equipes = num[0]
			required_wins = int(math.log2(numero_equipes))
			if wins >= required_wins:
				# Finaliza torneio
				cursor.execute("UPDATE torneios SET estado='finalizado' WHERE id_torneio=%s", (id_torneio,))
				conn.commit()
				print('Campeonato finalizado automaticamente: vencedor atingiu número de vitórias necessárias.')

		print('Resultado inserido com sucesso.')
		return True
	except Exception as e:
		if conn:
			conn.rollback()
		print(f'Erro ao inserir resultado: {e}')
		return False
	finally:
		if 'cursor' in locals():
			cursor.close()
		if 'conn' in locals():
			conn.close()


def listar_resultados_por_torneio(id_torneio):
	conn = criar_conexao()
	cursor = conn.cursor()
	try:
		sql = ('SELECT r.id_resultado, r.id_jogo, r.duracao_partida, r.pontos_equipe1, r.pontos_equipe2 '
			   'FROM resultado r JOIN jogos j ON r.id_jogo = j.id_jogos WHERE j.id_torneio=%s ORDER BY r.id_resultado')
		cursor.execute(sql, (id_torneio,))
		res = cursor.fetchall()
		return res
	except Exception as e:
		print(f'Erro ao listar resultados: {e}')
		return []
	finally:
		cursor.close()
		conn.close()

