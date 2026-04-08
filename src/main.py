from scraper.instagram_scraper import InstagramScraper ## import de classe
from database.connection import get_connection ## import de funcao


def salvar_dados(dados): ## salvamento de dados
    try:
        con = get_connection() ## abrir conexao com banco
        cursor = con.cursor() ## criar cursor pra executar comandos SQL

        # basico de insercao de banco de dados
        sql = """ 
        INSERT INTO perfis (username, nome, seguidores, seguindo, publicacoes)
        VALUES (%s, %s, %s, %s, %s)
        """

        valores = (
            dados["username"],
            dados["nome"],
            dados["seguidores"],
            dados["seguindo"],
            dados["publicacoes"]
        )

        cursor.execute(sql, valores) # executa o comando 
        con.commit() # salva o que foi preenchido

        cursor.close() 
        con.close() ## os dois tao só fechando

        print(f"Salvo: {dados['username']}") ## feedback do sistema

    except Exception as e:
        print(f"Erro no banco: {e}") # feedback só que pra erro

# onde a magia acontece, funcao principal
def main():
    scraper = InstagramScraper() # criacao de instancia

    scraper.abrir_instagram() # abrir o insta

    usuarios = ["avsxntos", "nrtz_g", "nike", "cristiano", "sxmnsty"] # quais perfis que quero pegar os dados

    # for pra passar por cada perfil e pegar os dados, depois salvar no banco
    for user in usuarios:
        dados = scraper.get_profile_data(user)

        if dados:
            salvar_dados(dados)

    scraper.fechar()


if __name__ == "__main__": ## filtro pra evitar bagunça e evitar rodar scraper sem querer
    main()