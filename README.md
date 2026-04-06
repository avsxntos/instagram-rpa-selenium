# Instagram RPA Selenium

## Visão geral

Este projeto é um automatizador de coleta de dados de perfis públicos do Instagram utilizando Selenium e Python. Ele abre o navegador Chrome, aguarda o login manual do usuário, navega até perfis específicos e extrai informações básicas como nome, seguidores, seguindo e número de publicações.

A intenção é funcionar como uma solução de RPA (Robotic Process Automation) leve para pesquisas, auditorias e coleta de métricas de contas públicas, com armazenamento dos dados em um banco de dados MySQL.

## Estrutura do projeto

O projeto está organizado em:

- `README.md` - documentação do projeto.
- `requirements.txt` - dependências Python necessárias (atualmente vazio, mas explícitas abaixo).
- `src/main.py` - ponto de entrada da aplicação e controle de fluxo principal.
- `src/scraper/instagram_scraper.py` - implementação do robô Selenium que abre o Instagram e captura os dados.
- `src/database/connection.py` - abstração da conexão com o banco de dados MySQL.

## Objetivo

O objetivo principal do projeto é:

1. abrir o Instagram no Chrome;
2. autenticar o usuário manualmente uma única vez;
3. navegar para perfis Instagram listados em `src/main.py`;
4. extrair dados públicos de perfil;
5. persistir esses dados em uma tabela MySQL chamada `perfis`.

## Dependências

O projeto depende destas bibliotecas Python:

- `selenium`
- `webdriver-manager`
- `mysql-connector-python`
- `python-dotenv`

### Nota

O arquivo `requirements.txt` está atualmente vazio no repositório. Para rodar o projeto, preencha-o com estas dependências ou instale manualmente:

```bash
pip install selenium webdriver-manager mysql-connector-python python-dotenv
```

## Requisitos do ambiente

Para executar o projeto corretamente, você precisa de:

- Python 3.8+ instalado
- Google Chrome instalado
- Acesso a internet para o Selenium carregar o Instagram e baixar o ChromeDriver
- MySQL ou MariaDB configurado localmente ou remotamente
- Variáveis de ambiente configuradas em um arquivo `.env`

## Configuração do banco de dados

Antes de rodar, crie o banco e a tabela que irão armazenar os perfis.

Exemplo de criação:

```sql
CREATE DATABASE instagram_scraper;
USE instagram_scraper;

CREATE TABLE perfis (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) NOT NULL,
  nome VARCHAR(255),
  seguidores VARCHAR(255),
  seguindo VARCHAR(255),
  publicacoes VARCHAR(255),
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Esse é o schema esperado pelo código em `src/main.py`, que insere `username`, `nome`, `seguidores`, `seguindo` e `publicacoes`.

## Configuração de variáveis de ambiente

Crie um arquivo chamado `.env` na raiz do projeto contendo as credenciais do seu banco MySQL:

```env
DB_HOST=localhost
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=instagram_scraper
```

O arquivo `.env` NÃO deve ser versionado em um repositório público, pois contém dados sensíveis.

## Como executar

1. Crie e ative um ambiente virtual (recomendado):

```bash
python -m venv venv
venv\Scripts\activate
```

2. Instale as dependências:

```bash
pip install selenium webdriver-manager mysql-connector-python python-dotenv
```

3. Garanta que o `.env` esteja configurado.

4. Execute o script principal:

```bash
python src\main.py
```

5. Quando o Chrome abrir, faça login no Instagram manualmente e pressione `ENTER` no terminal.

6. O script navegará pelos perfis listados em `src/main.py` e salvará os dados no banco.

## Explicação detalhada do código

### `src/main.py`

Este arquivo é o ponto de entrada e controla o fluxo de execução.

- `from scraper.instagram_scraper import InstagramScraper`
- `from database.connection import get_connection`

#### `salvar_dados(dados)`

- Abre a conexão MySQL via `get_connection()`.
- Prepara a instrução `INSERT INTO perfis (...) VALUES (%s, %s, %s, %s, %s)`.
- Usa a tupla `valores` com os campos extraídos do Instagram.
- Executa o SQL, faz `commit()` e fecha cursor/conexão.
- Em caso de erro, imprime uma mensagem no console.

#### `main()`

- Instancia `InstagramScraper()`.
- Chama `scraper.abrir_instagram()` para carregar a página inicial do Instagram.
- Define uma lista de usuários em `usuarios`.
- Para cada usuário, chama `scraper.get_profile_data(user)`.
- Se a coleta retornar dados válidos, chama `salvar_dados(dados)`.
- Ao final do processo, chama `scraper.fechar()` para encerrar o browser.

### `src/scraper/instagram_scraper.py`

Este arquivo contém toda a lógica do Selenium.

#### `InstagramScraper.__init__`

- Cria um objeto `webdriver.ChromeOptions()`.
- Adiciona `--start-maximized` para abrir o Chrome maximizado.
- Adiciona `--user-data-dir=C:\selenium\instagram_profile` para usar um perfil de usuário Chrome persistente. Isso mantém login salvo entre execuções.
- Cria o driver Chrome usando `ChromeDriverManager().install()` para baixar o driver automaticamente.

> Importante: o caminho `C:\selenium\instagram_profile` é fixo no código. Se desejar usar um diretório diferente, altere essa linha.

#### `abrir_instagram(self)`

- Acessa `https://www.instagram.com/`.
- Pausa a execução com `input("👉 Faça login UMA vez e pressione ENTER...")`.
- Isso exige login manual apenas na primeira execução (ou quando a sessão expirar).

#### `get_profile_data(self, username)`

- Navega para `https://www.instagram.com/{username}/`.
- Usa `WebDriverWait` para aguardar a presença do elemento `<header>` da página, garantindo que o perfil carregou.
- Tenta extrair o nome exibido em `h2`. Se não encontrar, define `nome = None`.
- Busca todos os spans dentro do header e procura pelos textos de seguidores e seguindo.
  - Se o texto contém `seguidor` ou `followers`, salva em `seguidores`.
  - Se o texto contém `seguindo` ou `following`, salva em `seguindo`.
- Tenta extrair o número de publicações usando XPath `//header//li[1]//span`.
- Retorna um dicionário com os valores extraídos.
- Se ocorrer qualquer exceção no processo, imprime `Erro ao coletar {username}: {e}` e retorna `None`.

#### `fechar(self)`

- Encerra o navegador com `self.driver.quit()`.

### `src/database/connection.py`

- Importa `mysql.connector`, `os` e `load_dotenv` de `dotenv`.
- Chama `load_dotenv()` para carregar variáveis de ambiente do arquivo `.env`.
- `get_connection()` tenta criar a conexão MySQL usando:
  - `host=os.getenv("DB_HOST")`
  - `user=os.getenv("DB_USER")`
  - `password=os.getenv("DB_PASSWORD")`
  - `database=os.getenv("DB_NAME")`
- Se a conexão for bem-sucedida, imprime `Conectado ao MySQL` e retorna o objeto de conexão.
- Em caso de erro, imprime `Erro ao conectar no banco: {e}` e retorna `None`.

## Fluxo de execução completo

1. `python src\main.py`
2. O driver Chrome é iniciado com perfil persistente.
3. O navegador abre `https://www.instagram.com/`.
4. O usuário faz login manual e pressiona ENTER.
5. O script percorre a lista de perfis definidos em `usuarios`.
6. Para cada perfil, ele acessa a URL do perfil.
7. Aguarda o carregamento do header.
8. Extrai `nome`, `seguidores`, `seguindo` e `publicacoes`.
9. Salva os dados na tabela MySQL `perfis`.
10. Ao fim, fecha o navegador.

## Como adicionar ou remover perfis

Edite a lista `usuarios` em `src/main.py`:

```python
usuarios = [
    "vincittaco",
    "foilcardsoficial",
    "arakinidi_airdunkini",
    "obarbeirodg"
]
```

Adicione ou remova nomes de usuário conforme necessário.

## Observações importantes

### Login persistente

O uso de `--user-data-dir=C:\selenium\instagram_profile` significa que o Chrome salvará os cookies e o login naquele diretório. Isso evita que seja necessário realizar login toda vez que o script rodar.

### Fragilidade do scraping

O Instagram altera frequentemente sua interface HTML. O código atual depende de:

- `header` existente na página de perfil
- `h2` para o nome de exibição
- spans com textos que contenham `seguidor`, `followers`, `seguindo` ou `following`
- `//header//li[1]//span` para número de publicações

Se a página do Instagram mudar, o scraper pode deixar de funcionar ou passar a coletar valores `None`.

### Riscos e limites

- O Instagram pode detectar e bloquear comportamentos automatizados.
- Use uma conta de teste e respeite os limites de requisições.
- Não use o script em escala para perfis privados ou com intenções que violem os termos de serviço.

## Possíveis melhorias

1. adicionar login automático com usuário/senha em vez de login manual;
2. extrair mais campos, como bio, link, local, número de stories etc.;
3. salvar resultados em CSV ou JSON além do MySQL;
4. suportar `headless` com tratamento especial de cookies;
5. usar proxies e rotacionar agentes de usuário para reduzir bloqueios;
6. extrair os dados de seguidores/seguindo com formatação consistente;
7. adicionar logs estruturados e relatórios de execução;
8. usar um banco SQLite local para casos de uso mais simples;
9. implementar um mecanismo de retry ao falhar na requisição;
10. converter a lista de usuários em leitura dinâmica a partir de arquivo CSV/JSON.

## Erros comuns e como resolver

- `Erro ao conectar no banco:`
  - Verifique se o MySQL está rodando.
  - Confira se `DB_HOST`, `DB_USER`, `DB_PASSWORD` e `DB_NAME` no `.env` estão corretos.

- `Erro ao coletar {username}: ...`
  - Pode ser causado por perfil inexistente, bloqueio do Instagram ou mudança na estrutura da página.
  - Verifique se a conta é pública e se o Instagram está carregando corretamente.

- O Chrome abre, mas não coleta dados:
  - Confirme se você fez login corretamente.
  - Confira se o perfil existe e se a página foi totalmente carregada.

## Considerações de segurança

- Nunca compartilhe seu `.env` com credenciais de banco de dados.
- Evite deixar seu usuário e senha do Instagram armazenados em código.
- Use uma conta de teste sempre que possível.

## O que foi documentado aqui

Este README explica:

- cada arquivo do projeto;
- o fluxo completo de execução;
- as dependências necessárias;
- a configuração do banco de dados;
- como preencher `.env`;
- os pontos de fragilidade do scraper;
- sugestões de melhorias e extensões;
- diagnósticos de erro.

## Próximos passos sugeridos

1. popular `requirements.txt` com as dependências do projeto.
2. criar o banco e a tabela `perfis` no MySQL.
3. rodar o script e confirmar que os dados aparecem no banco.
4. revisar e eventualmente parametrizar `usuarios` para carregar de um arquivo.
5. adicionar tratamento de erros mais robusto e logs detalhados.

---

### Referência de arquivos

- `src/main.py` - controla a execução e insere os dados no banco.
- `src/scraper/instagram_scraper.py` - faz o scraping do Instagram.
- `src/database/connection.py` - gerencia a conexão com o banco de dados.

### Mensagens exibidas na execução

- `Conectado ao MySQL` - conexão bem sucedida.
- `Salvo: {username}` - inserção bem sucedida no banco.
- `Erro no banco: {e}` - falha ao gravar no banco.
- `❌ Erro ao coletar {username}: {e}` - falha na coleta de dados do perfil.

