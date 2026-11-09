"""
Script de teste funcional para o fluxo de torneio/jogos/resultados.
Execute com: python tests/test_flow.py

Observações:
- O script usa as funções do pacote `services` já existente.
- Não realiza limpeza automática profunda no banco. Ao final há instruções de limpeza manual.
- Requer que o banco (`db.criar_conexao`) esteja acessível e que as tabelas do script `scripts/BD_Jogos.sql` existam.
"""

import time
from datetime import datetime, timedelta
import argparse
import os
import sys

# Garantir que o diretório do projeto (`Projeto_BD`) esteja no sys.path
# Isso permite executar o teste a partir da pasta mãe sem erro de importação de `db`.
HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(HERE, '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import db as db_mod
import services.service_usuario as su
import services.service_equipe as se
import services.service_torneio as st
import services.service_jogo as sj
import services.service_resultado as sr


def find_user_by_email(email):
    users = su.listar_usuarios()
    for u in users:
        if u[2] == email:
            return u[0]
    return None


def find_torneio_by_name(nome):
    torneios = st.listar_torneios()
    for t in torneios:
        if t[1] == nome:
            return t[0]
    return None


def find_equipe_by_name(nome):
    equipes = se.ler_equipes()
    for e in equipes:
        if e[1] == nome:
            return e[0]
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true', help='Executa o fluxo sem persistir alterações (faz rollback no final)')
    args = parser.parse_args()

    dry_run = args.dry_run

    ts = int(time.time())
    real_conn = None
    if dry_run:
        # criar conexão real e um wrapper que evita commits/fechos automáticos
        real_conn = db_mod.criar_conexao()

        class _ProxyConn:
            def __init__(self, real):
                self._real = real

            def cursor(self):
                return self._real.cursor()

            def commit(self):
                # no-op em dry-run: acumulamos mudanças e faremos rollback no final
                return None

            def rollback(self):
                return self._real.rollback()

            def close(self):
                # no-op: não fechar até fazermos rollback/close no final
                return None

            def __getattr__(self, item):
                return getattr(self._real, item)

        proxy = _ProxyConn(real_conn)

        # injetar a função criar_conexao nos módulos de serviço para retornar o proxy
        for mod in (su, se, st, sj, sr):
            setattr(mod, 'criar_conexao', (lambda p=proxy: p))

        print('Modo dry-run ativo: nenhuma alteração será persistida (rollback no final).')
    else:
        dry_run = False
    org_email = f"org_{ts}@test.local"
    org_name = f"Org Test {ts}"
    org_pwd = "testpass"

    print('\n==> 1) Criando usuário organizador (se necessário)')
    if not find_user_by_email(org_email):
        ok = su.cadastrar_usuario(org_name, org_pwd, org_email, 'organizador do torneio')
        if not ok:
            print('Falha ao cadastrar organizador. Verifique o banco e tipos de usuário. Abortando.')
            return
        time.sleep(0.5)

    organizador_id = find_user_by_email(org_email)
    print('Organizador id =', organizador_id)

    print('\n==> 2) Criando torneio de teste (8 equipes)')
    nome_torneio = f"Torneio Teste {ts}"
    inicio = datetime.now()
    fim = inicio + timedelta(days=1)
    created = st.criar_torneio(nome_torneio, inicio, fim, 6, 10, 8, organizador_id)
    if not created:
        print('Erro ao criar torneio. Abortando.')
        return
    time.sleep(0.5)
    torneio_id = find_torneio_by_name(nome_torneio)
    print('Torneio id =', torneio_id)

    print('\n==> 3) Criando 8 equipes e inscrevendo-as')
    equipe_ids = []
    for i in range(1, 9):
        nome_e = f"Equipe_{ts}_{i}"
        se.inserir_equipe(nome_e, f"Regiao{i}", 7, False, None)
        time.sleep(0.1)
        eid = find_equipe_by_name(nome_e)
        if not eid:
            print('Não conseguiu recuperar id da equipe criada:', nome_e)
            return
        equipe_ids.append(eid)
        insc = st.inscrever_equipe(torneio_id, eid)
        if not insc:
            print(f'Falha ao inscrever equipe {eid} no torneio')
            return

    print('Equipes inscritas:', equipe_ids)

    print('\n==> 4) Iniciando torneio')
    started = st.start_torneio(torneio_id, 8)
    if not started:
        print('Falha ao iniciar torneio. Abortando.')
        return

    print('\n==> 5) Criando primeiro jogo entre equipes 1 e 2')
    data_jogo = (datetime.now() + timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M')
    ok = sj.criar_jogo(torneio_id, equipe_ids[0], equipe_ids[1], data_jogo)
    if not ok:
        print('Falha ao criar primeiro jogo. Abortando.')
        return

    jogos = sj.listar_jogos(torneio_id)
    print('Jogos atuais:', jogos)
    primeiro_id = jogos[-1][0]

    print('\n==> 6) Tentando criar segundo jogo sem resultado (deve falhar)')
    data_jogo2 = (datetime.now() + timedelta(minutes=40)).strftime('%Y-%m-%d %H:%M')
    # Com a regra atualizada, um novo jogo só deve ser bloqueado se as equipes envolvidas
    # tiverem seu último jogo sem resultado. Como equipes[2] e equipes[3] ainda não jogaram,
    # a criação deve ser permitida.
    ok2 = sj.criar_jogo(torneio_id, equipe_ids[2], equipe_ids[3], data_jogo2)
    if ok2:
        print('Comportamento esperado: segundo jogo criado, pois as equipes ainda não tinham jogos pendentes.')
        jogos = sj.listar_jogos(torneio_id)
        segundo_id = jogos[-1][0]
    else:
        print('Erro: segundo jogo não foi criado embora as equipes não tenham jogos pendentes.')

    print('\n==> 7) Inserindo resultado do primeiro jogo (equipe 1 vence)')
    duracao = '00:30:00'
    res_ok = sr.criar_resultado(primeiro_id, duracao, 10, 5)
    if not res_ok:
        print('Falha ao inserir resultado. Abortando.')
        return

    print('\n==> 8) Verificando/obtendo segundo jogo (se já criado, será reutilizado)')
    if 'segundo_id' not in locals():
        ok3 = sj.criar_jogo(torneio_id, equipe_ids[2], equipe_ids[3], data_jogo2)
        if not ok3:
            print('Falha ao criar segundo jogo após resultado. Abortando.')
            return
        jogos = sj.listar_jogos(torneio_id)
        segundo_id = jogos[-1][0]
    else:
        jogos = sj.listar_jogos(torneio_id)
        print('Jogos agora:', jogos)

    print('\n==> 9) Adicionando resultado do segundo jogo (equipe 4 vence)')
    res_ok2 = sr.criar_resultado(segundo_id, duracao, 5, 10)
    if not res_ok2:
        print('Falha ao inserir resultado do segundo jogo. Abortando.')
        return

    print('\n==> 10) Simular vitórias do mesmo time para finalizar torneio')
    # Encontrar um time para ser "campeão" e criar jogos onde ele vence 3 vezes (log2(8)=3)
    campeao = equipe_ids[0]
    opponents = [e for e in equipe_ids if e != campeao]
    created_games = 1  # já criamos 1 jogo e vitória
    for opp in opponents[:5]:  # criamos alguns jogos; precisamos 3 vitórias
        dt = (datetime.now() + timedelta(minutes=60 + created_games*10)).strftime('%Y-%m-%d %H:%M')
        okg = sj.criar_jogo(torneio_id, campeao, opp, dt)
        if not okg:
            print('Falha ao criar jogo para simular vitória contra', opp)
            continue
        jogos = sj.listar_jogos(torneio_id)
        jid = jogos[-1][0]
        # campeao vence
        srv = sr.criar_resultado(jid, '00:25:00', 8, 1)
        if srv:
            created_games += 1
        if created_games >= 3:
            break

    print('Vitórias simuladas do campeão:', created_games)

    # Verificar estado do torneio
    torneios = st.listar_torneios()
    estado = None
    for t in torneios:
        if t[0] == torneio_id:
            estado = t[4] if len(t) > 4 else None
    conn_check = db_mod.criar_conexao()
    cur = conn_check.cursor()
    cur.execute('SELECT estado FROM torneios WHERE id_torneio=%s', (torneio_id,))
    row = cur.fetchone()
    cur.close()
    conn_check.close()
    if row:
        estado = row[0]

    print('\n==> Resultado final esperado: torneio deve estar "finalizado" quando campeão atingiu as vitórias necessárias')
    print('Estado atual do torneio:', estado)

    print('\n==> Teste concluído. NOTA: O banco foi alterado por este teste; se desejar limpar, remova manualmente os registros gerados (usuarios, equipes, torneios, jogos, resultados, torneio_equipe).')
    # se dry-run, reverte todas as mudanças realizadas na conexão real
    if dry_run and real_conn:
        try:
            real_conn.rollback()
            real_conn.close()
            print('Rollback executado e conexão fechada (dry-run).')
        except Exception as e:
            print('Erro ao reverter mudanças no dry-run:', e)


if __name__ == '__main__':
    main()
