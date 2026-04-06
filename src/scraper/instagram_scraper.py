from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InstagramScraper:

    def __init__(self):
        options = webdriver.ChromeOptions()

        options.add_argument("--start-maximized")

        # NÃO AGUENTAVA MAIS FICAR LOGANDO TODA HORA, ENTÃO USEI PERFIL DO CHROME PRA MANTER O LOGIN SALVO
        options.add_argument(r"--user-data-dir=C:\selenium\instagram_profile")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    def abrir_instagram(self):
        self.driver.get("https://www.instagram.com/")
        input("👉 Faça login UMA vez e pressione ENTER...")

    def get_profile_data(self, username):
        try:
            self.driver.get(f"https://www.instagram.com/{username}/")

            wait = WebDriverWait(self.driver, 15)

            wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "header"))
            )

            try:
                nome = self.driver.find_element(By.TAG_NAME, "h2").text
            except:
                nome = None

            spans = self.driver.find_elements(By.XPATH, "//header//span")

            seguidores = None
            seguindo = None

            for span in spans:
                texto = span.get_attribute("title") or span.text

                if texto:
                    if "seguidor" in texto or "followers" in texto:
                        seguidores = texto

                    if "seguindo" in texto or "following" in texto:
                        seguindo = texto

            try:
                publicacoes = self.driver.find_element(
                    By.XPATH, "//header//li[1]//span"
                ).text
            except:
                publicacoes = None

            return {
                "username": username,
                "nome": nome,
                "seguidores": seguidores,
                "seguindo": seguindo,
                "publicacoes": publicacoes
            }

        except Exception as e:
            print(f"❌ Erro ao coletar {username}: {e}")
            return None

    def fechar(self):
        self.driver.quit()