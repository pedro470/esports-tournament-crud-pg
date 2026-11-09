import os
import services.service_torneio as service_torneio
import services.service_equipe as service_equipe


def interface_torneio_equipes():
    os.system('cls')
    while True:
        print('---Gerenciar Equipes do Torneio---')
        print('1 - Listar equipes inscritas em um torneio')
        print('2 - Inscrever equipe em torneio (antes do start)')
        print('3 - Remover inscrição de equipe (antes do start)')
        print('4 - Voltar')

        opcao = input('Escolha uma opção: ')

        if opcao == '1':
            listar_equipes_torneio()
        elif opcao == '2':
            inscrever_equipe_interface()
        elif opcao == '3':
            remover_inscricao_interface()
        elif opcao == '4':
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


def _selecionar_equipe():
    equipes = service_equipe.ler_equipes()
    if not equipes:
        print('Nenhuma equipe cadastrada.')
        return None
    ids = []
    print('Equipes disponíveis:')
    for e in equipes:
        ids.append(e[0])
        print(f'id: {e[0]}\t | \t Nome: {e[1]}\t | \t Região: {e[2]}\t | \t Integrantes: {e[3]}')

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


def listar_equipes_torneio():
    id_torneio = _selecionar_torneio()
    if id_torneio is None:
        return
    equipes = service_torneio.listar_equipes_inscritas(id_torneio)
    if not equipes:
        print('Nenhuma equipe inscrita nesse torneio.')
        return
    print('Equipes inscritas:')
    for e in equipes:
        print(f'id: {e[0]}\t | \t Nome: {e[1]}\t | \t Região: {e[2]}')


def inscrever_equipe_interface():
    id_torneio = _selecionar_torneio()
    if id_torneio is None:
        return

    iniciado = service_torneio._torneio_iniciado(id_torneio)
    if iniciado is None:
        print('Torneio não encontrado.')
        return
    if iniciado:
        print('Não é possível inscrever equipes em torneio já iniciado.')
        return

    id_equipe = _selecionar_equipe()
    if id_equipe is None:
        return

    service_torneio.inscrever_equipe(id_torneio, id_equipe)


def remover_inscricao_interface():
    id_torneio = _selecionar_torneio()
    if id_torneio is None:
        return

    iniciado = service_torneio._torneio_iniciado(id_torneio)
    if iniciado is None:
        print('Torneio não encontrado.')
        return
    if iniciado:
        print('Não é possível remover inscrições de torneio já iniciado.')
        return

    id_equipe = _selecionar_equipe()
    if id_equipe is None:
        return

    service_torneio.remover_inscricao(id_torneio, id_equipe)
