import os
import services.service_usuario as service_usuario
from time import sleep

def tela_de_autenticacao():
    os.system('cls')
    print('---Tela de Autenticação---')
    choice = input('Você já possui uma conta? \n 1- Sim \n 2- Não \n')
    if choice == '1':
        tela_de_login()
        return True
    elif choice == '2':
        tela_de_cadastro()
    else:
        print('Opção inválida. Tente novamente.')
        tela_de_autenticacao()
    return False

def tela_de_login():
    os.system('cls')
    print('---Tela de Login---')
    email = input('Digite seu email: ')
    password = input('Digite sua senha: ')
    autenticado = service_usuario.autenticar_usuario(email, password)
    #Primeiro elemento: usuario
    if not autenticado[0]:
        print('Falha na autenticação. Tente novamente.')
        sleep(1.5)
        tela_de_login()
    else:
        os.system('cls')
        print(f'Bem-vindo, {autenticado[1]}!')

def tela_de_cadastro():
    os.system('cls')
    print('---Tela de Cadastro---')
    while True:

        # Coleta de dados do usuário
        username = input('Escolha um nome de usuário: ')

        # Validação da senha
        while True:
            password = input('Escolha uma senha: ')
            if len(password) >= 4:
                break
            else:
                print('Senha muito curta. Deve ter pelo menos 4 caracteres.')
        
        # Validação do email
        while True:
            email = input('Digite seu email: ')
            if '@' in email and '.' in email:
                break
            else:
                print('Email inválido. Tente novamente.')
    
        # Validação do tipo de usuário
        usuarios_disponiveis = service_usuario.listar_tipos_usuarios()
        while True:
            print('Tipos de usuários disponíveis:')
            for i, tipo in enumerate(usuarios_disponiveis, start=1):
                print(f' {i}- {tipo}')
            try:
                tipo_usuario = int(input('Digite o tipo de usuário: '))
                if tipo_usuario in range(1, len(usuarios_disponiveis)+1):
                    tipo_usuario = usuarios_disponiveis[tipo_usuario - 1]
                    break
                else:
                    print('Opção inválida. Tente novamente.')
            except ValueError:
                print('Opção inválida. Tente novamente.')

        resultado = service_usuario.cadastrar_usuario(username, password, email, tipo_usuario)
        if not resultado:
            continue
        print(f'Conta criada com sucesso para {username}!')
        break