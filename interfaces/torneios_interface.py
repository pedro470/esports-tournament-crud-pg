import os
from datetime import datetime

import services.service_torneio as service_torneio
import services.service_usuario as service_usuario
import interfaces.torneio_equipes_interface as interface_torneio_equipes
import interfaces.jogos_interface as jogos_interface


def interface_torneios():
    os.system('cls')
    while True:
        print('---Interface de Torneios---')
        print('1 - Inserir torneio')
        print('2 - Atualizar torneio (antes do start)')
        print('3 - Deletar torneio (antes do start)')
        print('4 - Iniciar torneio')
        print('5 - Listar torneios')
        print('6 - Gerenciar equipes do torneio')
        print('7 - Gerenciar jogos do torneio')
        print('8 - Voltar ao menu principal')

        opcao = input('Escolha uma opção: ')

        if opcao == '1':
            interface_inserir_torneio()
        elif opcao == '2':
            interface_update_torneio()
        elif opcao == '3':
            interface_deletar_torneio()
        elif opcao == '4':
            interface_start_torneio()
        elif opcao == '5':
            interface_listar_torneios()
        elif opcao == '6':
            interface_torneio_equipes.interface_torneio_equipes()
        elif opcao == '7':
            jogos_interface.interface_jogos()
        elif opcao == '8':
            break
        else:
            print('Opção inválida. Tente novamente.')


def interface_inserir_torneio():
    os.system('cls')
    print('---Inserir Torneio---')
    nome = input('Nome do torneio: ')

    # Datas: esperar formato YYYY-MM-DD HH:MM
    while True:
        inicio_str = input('Data de início (YYYY-MM-DD HH:MM): ')
        try:
            data_inicio = datetime.strptime(inicio_str, '%Y-%m-%d %H:%M')
            break
        except ValueError:
            print('Formato inválido. Use YYYY-MM-DD HH:MM')

    while True:
        fim_str = input('Data de fim (YYYY-MM-DD HH:MM): ')
        try:
            data_fim = datetime.strptime(fim_str, '%Y-%m-%d %H:%M')
            if data_fim <= data_inicio:
                print('Data de fim deve ser posterior à data de início.')
                continue
            break
        except ValueError:
            print('Formato inválido. Use YYYY-MM-DD HH:MM')

    while True:
        try:
            minimo = int(input('Minimo de jogadores por equipe ( > 5 ): '))
            if minimo <= 5:
                print('Minimo deve ser maior que 5')
                continue
            break
        except ValueError:
            print('Insira um número inteiro válido.')

    while True:
        try:
            maximo = int(input('Maximo de jogadores por equipe ( <= 10 ): '))
            if maximo > 10:
                print('Maximo deve ser menor ou igual a 10')
                continue
            if maximo < minimo:
                print('Maximo não pode ser menor que minimo')
                continue
            break
        except ValueError:
            print('Insira um número inteiro válido.')

    while True:
        try:
            numero = int(input('Número de equipes (8, 16 ou 32): '))
            if numero not in (8, 16, 32):
                print('Número inválido. Deve ser 8, 16 ou 32')
                continue
            break
        except ValueError:
            print('Insira um número inteiro válido.')

    # Escolher organizador (necessariamente do tipo organizador do torneio)
    usuarios = service_usuario.listar_usuarios()
    organizadores = [u for u in usuarios if u[3] == 'organizador do torneio']
    if not organizadores:
        print('Não há usuários do tipo "organizador do torneio" cadastrados. Crie um antes.')
        return

    print('Organizadores disponíveis:')
    for u in organizadores:
        print(f'id: {u[0]}\tNome: {u[1]}\tEmail: {u[2]}')

    while True:
        try:
            organizador_id = int(input('Digite o id do organizador: '))
            ids = [u[0] for u in organizadores]
            if organizador_id not in ids:
                print('ID inválido. Escolha um dos organizadores listados.')
                continue
            break
        except ValueError:
            print('Insira um número inteiro válido.')

    retorno = service_torneio.criar_torneio(nome, data_inicio, data_fim, minimo, maximo, numero, organizador_id)
    if retorno:
        print('Torneio criado com sucesso.')


def interface_listar_torneios():
    os.system('cls')
    print('---Torneios---')
    torneios = service_torneio.listar_torneios()
    if not torneios:
        print('Nenhum torneio cadastrado.')
        return
    for t in torneios:
        print(f'id: {t[0]}\tNome: {t[1]}\tInicio: {t[2]}\tFim: {t[3]}\tMin: {t[4]}\tMax: {t[5]}\tNumEq: {t[6]}\tOrganizador: {t[7]}')


def interface_deletar_torneio():
    id_torneio = ''
    while id_torneio != 'exit':
        print('---Deletar Torneio---')
        print('Digite exit para voltar ao menu anterior')
        torneios = service_torneio.listar_torneios()

        ids_validos = []
        print('Torneios disponíveis:')
        for t in torneios:
            ids_validos.append(t[0])
            print(f'id: {t[0]}\tNome: {t[1]}\tInicio: {t[2]}\tFim: {t[3]}')
        id_torneio = input('Digite o id do torneio que quer excluir: ')

        if id_torneio.lower() == 'exit':
            break

        try:
            id_int = int(id_torneio)
        except ValueError:
            print('ID inválido. Por favor, insira um número inteiro.')
            continue

        if id_int not in ids_validos:
            print('ID não encontrado. Por favor, insira um ID válido.')
            continue

        service_torneio.deletar_torneio(id_int)


def interface_update_torneio():
    while True:
        print('---Atualizar Torneio---')
        torneios = service_torneio.listar_torneios()

        ids_validos = []
        print('Torneios disponíveis:')
        for t in torneios:
            ids_validos.append(t[0])
            print(f'id: {t[0]}\tNome: {t[1]}\tInicio: {t[2]}\tFim: {t[3]}\tMin: {t[4]}\tMax: {t[5]}\tNumEq: {t[6]}')
        id_input = input('Digite o id do torneio que quer atualizar (ou "sair" para voltar): ')

        if id_input.lower() == 'sair':
            break

        try:
            id_int = int(id_input)
        except ValueError:
            print('ID inválido. Por favor, insira um número inteiro.')
            continue

        if id_int not in ids_validos:
            print('ID não encontrado. Por favor, insira um ID válido.')
            continue

        print('Deixe em branco para não alterar um campo.')
        num_str = input('Novo número de equipes (8,16,32): ')
        min_str = input('Novo mínimo de jogadores por equipe (>5): ')
        max_str = input('Novo máximo de jogadores por equipe (<=10): ')

        numero = None
        minimo = None
        maximo = None

        try:
            if num_str.strip() != '':
                numero = int(num_str)
            if min_str.strip() != '':
                minimo = int(min_str)
            if max_str.strip() != '':
                maximo = int(max_str)
        except ValueError:
            print('Um dos valores inseridos não é um número válido.')
            continue

        service_torneio.atualizar_torneio_campos(id_int, numero_equipes=numero, minimo_jogadores=minimo, maximo_jogadores=maximo)


def interface_start_torneio():
    print('---Iniciar Torneio---')
    torneios = service_torneio.listar_torneios()
    if not torneios:
        print('Nenhum torneio cadastrado.')
        return
    for t in torneios:
        print(f'id: {t[0]}\tNome: {t[1]}\tInicio: {t[2]}')

    try:
        id_int = int(input('Digite o id do torneio que quer iniciar: '))
    except ValueError:
        print('ID inválido.')
        return
    minimo_maximo = None
    for t in torneios:
        if t[0] == id_int:
            quant_equipes = t[6]
            break

    service_torneio.start_torneio(id_int, quant_equipes)