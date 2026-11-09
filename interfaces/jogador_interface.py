#imports aleios
import os
from time import sleep

#imports services
import services.service_equipe as service_equipe 
import services.service_jogadores as service_jogador

#Definindo a interface do jogador
def interface_jogador():

    while True:
        
        os.system('cls')
        
        print('Escolha uma das opções a baixo:' \
        '\n1 - Inserir jogador' \
        '\n2 - Atualizar jogador' \
        '\n3 - Deletar jogador' \
        '\n4 - Atualizar equipe do jogador' \
        '\n5 - Listar Jogadores' \
        '\n6 - retornar ao menu')
        esc = input('Escolha uma opção: ')

        if esc == '1':
            interface_Inserir_Jogador()
        if esc == '2':
            interface_atualizar_jogador()
        if esc == '3':
            interface_deletar_jogador()
        if esc == '4':
            interface_atualizar_equipe_jogador()
        if esc == '5':
            interface_listar_jogadores()
        if esc == '6':
            break
        else:
            print('Opção inválida. Tente Novamente')


    
# Já inserir o jogador e a qual equipe ele pertence
def interface_Inserir_Jogador():

    while True:
        os.system('cls')
        nome = input('Digite seu nome completo: ')
        regiao = input('Região do Jogador: ')

        print('\n   EQUIPES DISPONÍVEIS   ')
        equipes = service_equipe.ler_equipes()

        for e in equipes:
            print(f'ID:{e[0]} - \tNOME:{e[1]}')
        
        while True:
            id_equipe = int(input('\nDigite o ID da equipe: '))
            if any(e[0] == id_equipe for e in equipes):
                break
            print('ID inválido! Digite novamente')
            sair = input('\nEscreva "exit" se desejar sair ou Enter para continuar:')

            if sair == 'exit':
                interface_jogador()

        service_jogador.inserir_jogador(nome, regiao, id_equipe)
        sleep(1.5)
        break


#Atualizar o jogador, só não fiz pra atualizar a equipe dele
def interface_atualizar_jogador():
    while True:

        os.system('cls')
        print('\n   JOGADORES DISPONÍVEIS   ')

        jogadores = service_jogador.ler_jogadores()

        id_jogadores_disponivel = []
        for j in jogadores:
            id_jogadores_disponivel.append(j[0])
            print(f'ID:{j[0]} - \tNome: {j[1]} - \tRegião:{j[2]} - \tEQUIPE:{j[3]}')
        id_jogador = input('Digite o ID que você deseja atualizar(ou "exit" para sair)')
        
        if id_jogador.lower() == 'exit':
            interface_jogador()
            return
        
        try:
            id_jogador_delet = int(id_jogador)
        except ValueError:
            print('ID inválido! Por favor, insira um número inteiro válido')
            continue

        if id_jogador_delet not in id_jogadores_disponivel:
            print('ID não encontrado. Por favor, insira um ID válido.')
            continue
        
        novo_nome = input('Digite novo nome do Jogador: ')
        novo_regiao = input('Digite nova região do Jogador: ')

        service_jogador.atualizar_jogador(id_jogador_delet, novo_nome, novo_regiao)
        sleep(1.5)
        return


def interface_atualizar_equipe_jogador():

    while True:

        os.system('cls')
        print('\n   JOGADORES DISPONÍVEIS   ')

        jogadores = service_jogador.ler_jogadores()

        id_jogadores_disponivel = []
        for j in jogadores:
            id_jogadores_disponivel.append(j[0])
            print(f'ID{j[0]} - \tNome: {j[1]} - \tRegião:{j[2]} - \tEQUIPE:{j[3]}')
        id_jogador = input('Digite o ID do Jogador que deseja mudar de equipe(ou "exit" para sair)').lower()

        if id_jogador.lower() == 'exit':
            interface_jogador()
            return

        try:
            id_jogador_delet = int(id_jogador)
        except:
            print('ID inválido')
            continue

        if id_jogador_delet not in id_jogadores_disponivel:
            print('Jogador não encontrado')
            return
        
        print('\n   EQUIPES DISPONÍVEIS   ')
        equipes = service_equipe.ler_equipes()

        id_equipes_disponiveis = []
        for e in equipes:
            id_equipes_disponiveis.append(e[0])
            print(f'ID:{e[0]} - \tNOME:{e[1]}')
        
        novo_id_equipe = input('\nDigite o ID da nova equipe do jogador: ')

        try:
            novo_id_equipe_int = int(novo_id_equipe)
        except:
            print('ID Inválido.')
            return
        
        if novo_id_equipe_int not in id_equipes_disponiveis:
            print('Equipe não encontrada.')
            return
        
        service_jogador.atualizar_equipe_jogador(id_jogador_delet, novo_id_equipe_int)
        print('Jogador em uma nova equipe com sucesso!')
        
        cont = input('\nDeseja atualizar outro jogador(sim ou não)?: ')

        if cont.startswith('n'):
            interface_jogador()
            return
        else:
            continue


def interface_deletar_jogador():

    while True:

        os.system('cls')
        print('\n   JOGADORES DISPONÍVEIS   ')

        jogadores = service_jogador.ler_jogadores()

        id_jogadores_disponivel = []
        for j in jogadores:
            id_jogadores_disponivel.append(j[0])
            print(f'ID:{j[0]} - \tNome: {j[1]} - \tRegião:{j[2]} - \tEQUIPE:{j[3]}')
        id_jogador = input('\nDigite o ID do Jogador que deseja deletar(ou "exit" para sair): ').lower()

        if id_jogador == 'exit':
            interface_jogador()
            return

        try:
            id_jogador_delet = int(id_jogador)
        except:
            print('Digite um número/ID válido')
            continue

        if id_jogador_delet not in id_jogadores_disponivel:
            print('Esse ID não existe')
        
        service_jogador.deletar_jogador(id_jogador_delet)
        sleep(1.5)
        break

def interface_listar_jogadores():

    while True:
        os.system('cls')
        print('\n   JOGADORES DISPONÍVEIS   ')

        jogadores = service_jogador.ler_jogadores()

        id_jogadores_disponivel = []
        for j in jogadores:
            id_jogadores_disponivel.append(j[0])
            print(f'ID:{j[0]} - \tNome: {j[1]} - \tRegião:{j[2]} - \tEQUIPE:{j[3]}')
        
        exit = input('\nDigite "exit" para retornar a tela inicial: ')

        if exit == 'exit':
            interface_jogador()
            return