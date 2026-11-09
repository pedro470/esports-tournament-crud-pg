
import os
import services.service_resultado as service_resultado
import services.service_jogo as service_jogo
import services.service_torneio as service_torneio


def interface_resultados():
	os.system('cls')
	while True:
		print('---Gerenciar Resultados---')
		print('1 - Inserir resultado para um jogo')
		print('2 - Listar resultados de um torneio')
		print('3 - Voltar')

		opcao = input('Escolha uma opção: ')
		if opcao == '1':
			inserir_resultado_interface()
		elif opcao == '2':
			listar_resultados_interface()
		elif opcao == '3':
			break
		else:
			print('Opção inválida. Tente novamente.')


def _selecionar_torneio():
	torneios = service_torneio.listar_torneios()
	if not torneios:
		print('Nenhum torneio cadastrado.')
		return None
	ids = []
	print('Torneios disponíveis:')
	for t in torneios:
		ids.append(t[0])
		print(f'id: {t[0]}\t | \t Nome: {t[1]}')

	escolha = input('Digite o id do torneio (ou "sair" para voltar): ')
	if escolha.lower() in ('sair', 'exit'):
		return None
	try:
		id_int = int(escolha)
	except ValueError:
		print('ID inválido.')
		return None
	if id_int not in ids:
		print('ID não encontrado.')
		return None
	return id_int


def _selecionar_jogo_do_torneio(id_torneio):
	jogos = service_jogo.listar_jogos(id_torneio)
	if not jogos:
		print('Nenhum jogo nesse torneio.')
		return None
	ids = []
	for j in jogos:
		ids.append(j[0])
		print(f'id: {j[0]}\tEquipe1: {j[1]}\tEquipe2: {j[2]}\tData: {j[3]}')

	escolha = input('Digite o id do jogo (ou "sair" para voltar): ')
	if escolha.lower() in ('sair', 'exit'):
		return None
	try:
		id_int = int(escolha)
	except ValueError:
		print('ID inválido.')
		return None
	if id_int not in ids:
		print('ID não encontrado.')
		return None
	return id_int


def inserir_resultado_interface():
	id_torneio = _selecionar_torneio()
	if id_torneio is None:
		return
	id_jogo = _selecionar_jogo_do_torneio(id_torneio)
	if id_jogo is None:
		return

	duracao = input('Duração da partida (ex: 00:45:00): ')
	try:
		pontos1 = int(input('Pontos equipe 1: '))
		pontos2 = int(input('Pontos equipe 2: '))
	except ValueError:
		print('Pontos devem ser números inteiros.')
		return

	service_resultado.criar_resultado(id_jogo, duracao, pontos1, pontos2)


def listar_resultados_interface():
	id_torneio = _selecionar_torneio()
	if id_torneio is None:
		return
	resultados = service_resultado.listar_resultados_por_torneio(id_torneio)
	if not resultados:
		print('Nenhum resultado encontrado para esse torneio.')
		return
	for r in resultados:
		print(f'id_resultado: {r[0]}\tJogo: {r[1]}\tDuracao: {r[2]}\tP1: {r[3]}\tP2: {r[4]}')

