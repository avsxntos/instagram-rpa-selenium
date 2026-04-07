import mysql.connector ## import da lib que conecta com banco
import os ## onde eu pego os dados do .env
from dotenv import load_dotenv ## import de funcao.

load_dotenv() ## leitura do .env.

def get_connection(): ## funcao que faz a conexao com o banco, usando os dados do .env.
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        print("Conectado ao MySQL") ## mensagem de sucesso na conexao.
        return connection

    except Exception as e:
        print(f"Erro ao conectar no banco: {e}") ## mensagem de erro caso a conexao falhe.
        return None