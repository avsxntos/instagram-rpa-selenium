from scraper.instagram_scraper import InstagramScraper
from database.connection import get_connection


def salvar_dados(dados):
    try:
        con = get_connection()
        cursor = con.cursor()

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

        cursor.execute(sql, valores)
        con.commit()

        cursor.close()
        con.close()

        print(f"Salvo: {dados['username']}")

    except Exception as e:
        print(f"Erro no banco: {e}")


def main():
    scraper = InstagramScraper()

    scraper.abrir_instagram()

    usuarios = ["alexandre_vsp", "mikavit_", "issinhaha", "pedro.fer7"]

    for user in usuarios:
        dados = scraper.get_profile_data(user)

        if dados:
            salvar_dados(dados)

    scraper.fechar()


if __name__ == "__main__":
    main()