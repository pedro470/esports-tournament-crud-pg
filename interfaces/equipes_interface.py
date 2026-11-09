#impor aleios
import os

#import services
import services.service_equipe as service_equipe


#Interface principal de equipes
def interface_equipes():
    
    while True:
        os.system('cls')
        print('---Interface de Equipes---')

        print('1 - Inserir equipe')
        print('2 - Deletar equipe')
        print('3 - Atualizar equipe')
        print('4 - Listar equipes')
        print('5 - Voltar ao menu principal')
        opcao = input('Escolha uma opção: ')

        if opcao == '1':
            interface_inserir_equipe()
        elif opcao == '2':
            interface_deletar_equipe()
        elif opcao == '3':
            interface_update_equipe()
        elif opcao == '4':
            listar_torneios_da_equipe()
        elif opcao == '5':
            break
        else:
            print('Opção inválida. Tente novamente.')


#Interface para inserir equipes
def interface_inserir_equipe():
    os.system('cls')
    nome_equipe = input('Qual será o nome da equipe: ')
    regiao = input('Qual a região de vocês: ')

    #Não pode mais de 10 pessoas na equipe
    while True:
        try:
            quant_integrantes = int(input('Quantos serão da equipe?: '))
            if quant_integrantes > 10:
                print('Não pode mais de 10 pessoas na equipe')
                continue
            break
        except ValueError:
            print('Por favor, insira um número válido.')
    
    #Se tiver líder, pedir o nome do líder
    while True:
        opcao_lider = input('O time tem líder? \n 1-Sim ou 2-Não?: ')
        if opcao_lider == '1' or opcao_lider == '2':
            lider = opcao_lider == '1'
            if lider:
                nome_lider = input('Qual o nome do líder: ')
            else:
                nome_lider = None
            retorno_inserir = service_equipe.inserir_equipe(nome_equipe, regiao, quant_integrantes, lider, nome_lider)
            print(retorno_inserir)
            break
        else:
            print('Opção inválida. Insira 1 para sim ou 2 para não')


#Deletar a equipe
def interface_deletar_equipe():
    id_equipes = ''
    while id_equipes != 'exit':
        print('---Deletar Equipe---')
        print('Digite exit para voltar ao menu anterior')
        equipes = service_equipe.ler_equipes()

        id_equipes_validos = []
        print('Equipes disponíveis:')
        for equipe in equipes:
            #Resgata todos os ids para validação
            id_equipes_validos.append(equipe[0])
            print(f'id: {equipe[0]} \t | \t Nome: {equipe[1]}\t | \t Região: {equipe[2]}\t | \t Integrantes: {equipe[3]}\t | \t Líder: {equipe[4]}\t | \t Nome Líder: {equipe[5]}')
        id_equipes = input('Digite o id do time que quer tirar: ')

        #Garantir que o id seja um inteiro
        try:
            id_equipes_int = int(id_equipes)
        except ValueError:
            print("ID inválido. Por favor, insira um número inteiro.")
            continue
    
        #Garantir que o id exista
        if id_equipes_int not in id_equipes_validos:
            print("ID não encontrado. Por favor, insira um ID válido.")
            continue

        service_equipe.deletar_equipe(id_equipes_int)

        equipes = service_equipe.ler_equipes()
        print('\nTabela após exclusão:')
        for i in equipes:
            print(i)


#Dar update na equipe
def interface_update_equipe():
    while True:
        print('---Atualizar Equipe---')
        equipes = service_equipe.ler_equipes()

        id_equipes_validos = []
        print('Equipes disponíveis:')
        for equipe in equipes:
            #Resgata todos os ids para validação
            id_equipes_validos.append(equipe[0])
            print(f'id: {equipe[0]}\t | \t Nome: {equipe[1]}\t | \t Região: {equipe[2]}\t | \t Integrantes: {equipe[3]}\t | \t Líder: {equipe[4]}\t | \t Nome Líder: {equipe[5]}')
        id_equipe = input('Digite o id do time que quer atualizar (ou "sair" para voltar): ')

        if id_equipe.lower() == 'sair':
            break

        #Garantir que o id seja um inteiro
        try:
            id_equipe_int = int(id_equipe)
        except ValueError:
            print("ID inválido. Por favor, insira um número inteiro.")
            continue
    
        #Garantir que o id exista
        if id_equipe_int not in id_equipes_validos:
            print("ID não encontrado. Por favor, insira um ID válido.")
            continue

        novo_nome = input('Digite o novo nome da equipe: ')
        nova_regiao = input('Digite a nova região da equipe: ')

        service_equipe.update_equipe(novo_nome, id_equipe_int, nova_regiao)
        print('Equipe atualizada com sucesso!')

def listar_equipes():
    equipes = service_equipe.ler_equipes()
    if not equipes:
        print('Nenhuma equipe cadastrada.')
        return
    print('Equipes disponíveis:')
    for e in equipes:
        print(f'id: {e[0]}\t | \t Nome: {e[1]}\t | \t Região: {e[2]}\t | \t Integrantes: {e[3]}')

def listar_torneios_da_equipe():
    id_equipe = ''
    while True:
        listar_equipes()
        id_equipe = input('Digite o id da equipe para ver seus torneios (ou "sair" para voltar): ')
        if id_equipe.lower() == 'sair':
            return
        try:
            id_equipe_int = int(id_equipe)
            break
        except ValueError:
            print("ID inválido. Por favor, insira um número inteiro.")
            continue
    torneios = service_equipe.listar_torneios_da_equipe(id_equipe_int)
    if not torneios:
        print('Nenhum torneio encontrado para essa equipe.')
        return
    print('Torneios da equipe:')
    for t in torneios:
        print(f'id: {t[0]}  \t | \t Nome: {t[1]}\t | \t Inicio: {t[2]}\t | \t Fim: {t[3]}')