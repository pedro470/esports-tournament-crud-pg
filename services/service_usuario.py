import os

import bcrypt
from db import criar_conexao

def listar_usuarios():
    conn = criar_conexao()
    sql = "SELECT id_usuario, nome, email, tipo_usuario FROM usuarios"
    cursor = conn.cursor()
    cursor.execute(sql)
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return usuarios

def listar_tipos_usuarios():
    conn = criar_conexao()
    sql = "SELECT * FROM unnest(enum_range(NULL::tipo_usuario_enum))"
    cursor = conn.cursor()
    cursor.execute(sql)
    tipos = cursor.fetchall()
    cursor.close()
    conn.close()
    return [tipo[0] for tipo in tipos]

def cadastrar_usuario(username, password, email, tipo_usuario):
    
    lista_de_emails = list(map(lambda usuario: usuario[2], listar_usuarios()))
    if email in lista_de_emails:
        print('Erro: Email já cadastrado. Tente novamente com outro email.')
        return False
    
    lista_de_tipos = listar_tipos_usuarios()
    if tipo_usuario not in lista_de_tipos:
        print('Erro: Tipo de usuário inválido. Tente novamente.')
        return False
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    conn = criar_conexao()
    sql = "INSERT INTO usuarios (nome, email, senha, tipo_usuario) VALUES (%s, %s, %s, %s)"
    cursor = conn.cursor()
    cursor.execute(sql, (username, email, hashed_password, tipo_usuario))
    conn.commit()
    cursor.close()
    conn.close()
    print(f'Usuário {username} cadastrado com sucesso no sistema.')
    return True

def autenticar_usuario(email, password):
    conn = criar_conexao()
    sql = "SELECT senha, nome FROM usuarios WHERE email=%s"
    cursor = conn.cursor()
    cursor.execute(sql, (email,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    if resultado is None:
        print('Erro: Usuário não encontrado.')
        return [False, None]
    stored_hashed_password = resultado[0]
    if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
        return [True, resultado[1]]
    else:
        print('Erro: Senha incorreta.')
        return [False, None]