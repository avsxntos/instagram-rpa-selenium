from selenium import webdriver # importar selenium 
from selenium.webdriver.common.by import By # importa a classe que localizaa elementos
from selenium.webdriver.chrome.service import Service # serviço que cuida do driver do chrome
from webdriver_manager.chrome import ChromeDriverManager # baixar no automatico o driver do chrome, sem precisar ficar baixando manualmente e colocando no PATH
from selenium.webdriver.support.ui import WebDriverWait # vai esperar ate tudo carregar pra rodar, sugestao da internet.
from selenium.webdriver.support import expected_conditions as EC #parecido com de cima, mas condição pra esperar


class InstagramScraper: # classe do scraping melhor pra encapsular comportamento e manter sessões
    
    # metodo construtor 
    def __init__(self):
        options = webdriver.ChromeOptions() # config do chrome

        options.add_argument("--start-maximized") # navegador em tela cheia

        # NÃO AGUENTAVA MAIS FICAR LOGANDO TODA HORA, ENTÃO USEI PERFIL DO CHROME PRA MANTER O LOGIN SALVO
        options.add_argument(r"--user-data-dir=C:\selenium\instagram_profile")

        self.driver = webdriver.Chrome(  # pra fortalecer o que está em cima, do login
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    def abrir_instagram(self): # abre o insta, mas espera uma confirmação da minha parte pra poder pegar os dados
        self.driver.get("https://www.instagram.com/")
        input("👉 Faça login UMA vez e pressione ENTER...")

    def get_profile_data(self, username):
        try:
            self.driver.get(f"https://www.instagram.com/{username}/") # vai pro perfil

            wait = WebDriverWait(self.driver, 15) # auto explicativo.

            wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "header")) # esperar o header carregar
            )

            try:
                nome = self.driver.find_element(By.TAG_NAME, "h2").text # tentativa de pegar o nome, mas alguns nao tem, entao tem que ser tratado o erro
            except:
                nome = None 

            spans = self.driver.find_elements(By.XPATH, "//header//span") # pegar span do header onde tem seguidor...

            # as variaveis que vao armazenar essa duas informacoes 
            seguidores = None
            seguindo = None

            for span in spans:
                texto = span.get_attribute("title") or span.text

                if texto:
                    if "seguidor" in texto or "followers" in texto:
                        seguidores = texto

                    if "seguindo" in texto or "following" in texto:
                        seguindo = texto
            # # Tenta pegar número de publicações, mas nao consegui fazer dar certo, nao consigo arrumar.
            try:
                publicacoes = self.driver.find_element(
                    By.XPATH, "//header//li[1]//span"
                ).text
            except:
                publicacoes = None
            
            #retorno das coisas bem separadas.
            return {
                "username": username,
                "nome": nome,
                "seguidores": seguidores,
                "seguindo": seguindo,
                "publicacoes": publicacoes
            }

        except Exception as e:
            print(f"Erro ao coletar {username}: {e}") # qualquer erro, recebo feedback do sistema.
            return None

    def fechar(self):
        self.driver.quit() ## fecha tudinho depois