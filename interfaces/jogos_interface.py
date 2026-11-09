import os
import services.service_jogo as service_jogo
import services.service_torneio as service_torneio
import services.service_equipe as service_equipe
import interfaces.resultados_interface as resultados_interface


def interface_jogos():
	os.system('cls')
	while True:
		print('---Gerenciar Jogos do Torneio---')
		print('1 - Listar jogos de um torneio')
		print('2 - Inserir jogo (torneio em andamento)')
		print('3 - Atualizar jogo (antes do resultado)')
		print('4 - Deletar jogo (antes do resultado)')
		print('5 - Gerenciar resultados (submenu)')
		print('6 - Voltar')

		opcao = input('Escolha uma opção: ')
		if opcao == '1':
			listar_jogos_interface()
		elif opcao == '2':
			inserir_jogo_interface()
		elif opcao == '3':
			atualizar_jogo_interface()
		elif opcao == '4':
			deletar_jogo_interface()
		elif opcao == '5':
			resultados_interface.interface_resultados()
		elif opcao == '6':
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
		print(f'id: {t[0]}\t | \t Nome: {t[1]}\t | \t Inicio: {t[2]}\t | \t Fim: {t[3]}')

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


def _selecionar_equipe_do_torneio(id_torneio):
	equipes = service_torneio.listar_equipes_inscritas(id_torneio)
	if not equipes:
		print('Nenhuma equipe inscrita nesse torneio.')
		return None
	ids = []
	for e in equipes:
		ids.append(e[0])
		print(f'id: {e[0]}\t | \t Nome: {e[1]}')

	escolha = input('Digite o id da equipe (ou "sair" para voltar): ')
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


def listar_jogos_interface():
	id_torneio = _selecionar_torneio()
	if id_torneio is None:
		return
	jogos = service_jogo.listar_jogos(id_torneio)
	if not jogos:
		print('Nenhum jogo cadastrado para esse torneio.')
		return
	for j in jogos:
		print(f'id: {j[0]}\tEquipe1: {j[1]}\tEquipe2: {j[2]}\tData: {j[3]}')


def inserir_jogo_interface():
	id_torneio = _selecionar_torneio()
	if id_torneio is None:
		return
	estado = service_torneio._torneio_iniciado(id_torneio)
	if estado is None:
		print('Torneio não encontrado.')
		return
	if not estado:
		print('O torneio ainda não foi iniciado. Inicie-o para inserir jogos.')
		return

	print('Escolha equipe 1:')
	equipe1 = _selecionar_equipe_do_torneio(id_torneio)
	if equipe1 is None:
		return
	print('Escolha equipe 2:')
	equipe2 = _selecionar_equipe_do_torneio(id_torneio)
	if equipe2 is None:
		return
	data = input('Data e hora do jogo (YYYY-MM-DD HH:MM): ')

	service_jogo.criar_jogo(id_torneio, equipe1, equipe2, data)


def atualizar_jogo_interface():
	id_torneio = _selecionar_torneio()
	if id_torneio is None:
		return
	jogos = service_jogo.listar_jogos(id_torneio)
	if not jogos:
		print('Nenhum jogo para atualizar nesse torneio.')
		return
	ids = [j[0] for j in jogos]
	for j in jogos:
		print(f'id: {j[0]}\tEquipe1: {j[1]}\tEquipe2: {j[2]}\tData: {j[3]}')
	escolha = input('Digite o id do jogo que quer atualizar (ou "sair" para voltar): ')
	if escolha.lower() in ('sair', 'exit'):
		return
	try:
		id_int = int(escolha)
	except ValueError:
		print('ID inválido.')
		return
	if id_int not in ids:
		print('ID não encontrado.')
		return

	novo_data = input('Nova data e hora (YYYY-MM-DD HH:MM) ou deixe em branco: ')
	print('Se quiser trocar as equipes, escolha abaixo (ou deixe em branco)')
	print('Equipe 1:')
	nova_equipe1 = input('Digite novo id equipe 1 (ou deixe em branco): ')
	print('Equipe 2:')
	nova_equipe2 = input('Digite novo id equipe 2 (ou deixe em branco): ')

	eq1 = int(nova_equipe1) if nova_equipe1.strip() != '' else None
	eq2 = int(nova_equipe2) if nova_equipe2.strip() != '' else None
	data_final = novo_data if novo_data.strip() != '' else None

	service_jogo.atualizar_jogo(id_int, id_equipe1=eq1, id_equipe2=eq2, data_hora=data_final)


def deletar_jogo_interface():
	id_torneio = _selecionar_torneio()
	if id_torneio is None:
		return
	jogos = service_jogo.listar_jogos(id_torneio)
	if not jogos:
		print('Nenhum jogo para deletar nesse torneio.')
		return
	ids = [j[0] for j in jogos]
	for j in jogos:
		print(f'id: {j[0]}\tEquipe1: {j[1]}\tEquipe2: {j[2]}\tData: {j[3]}')
	escolha = input('Digite o id do jogo que quer deletar (ou "sair" para voltar): ')
	if escolha.lower() in ('sair', 'exit'):
		return
	try:
		id_int = int(escolha)
	except ValueError:
		print('ID inválido.')
		return
	if id_int not in ids:
		print('ID não encontrado.')
		return

	service_jogo.deletar_jogo(id_int)

