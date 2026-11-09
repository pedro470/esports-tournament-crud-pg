import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def criar_conexao():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME", "aula"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASS", ""),
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
        )
        return conn
    except Exception as e:
        print(f"Erro de conexão: {e}")
        return None
