# Instagram RPA Selenium

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/selenium-4.x-brightgreen)](https://www.selenium.dev/)
[![MySQL](https://img.shields.io/badge/mysql-compatible-orange)](https://www.mysql.com/)
[![Status](https://img.shields.io/badge/status-ativo-success)]()

## Visão geral

**Instagram RPA Selenium** é uma solução de automação (RPA) leve desenvolvida em Python para coleta estruturada de dados públicos de perfis do Instagram. 

O projeto:
- Abre o navegador Chrome de forma automatizada
- Aguarda login manual do usuário (realizado uma única vez)
- Navega até perfis Instagram específicos
- Extrai dados públicos: nome, seguidores, seguindo, número de publicações
- Persiste os dados em banco MySQL para análise posterior

É ideal para pesquisas, auditorias de marcas, coleta de métricas e análises de contas públicas, com foco em conformidade com políticas de scraping consciente.

## Estrutura do projeto

```
instagram-rpa-selenium/
├── src/
│   ├── main.py                      # Entrada principal e orquestração
│   ├── scraper/
│   │   └── instagram_scraper.py    # Lógica de scraping com Selenium
│   └── database/
│       └── connection.py            # Gerenciamento de conexão MySQL
├── .env                             # Variáveis de ambiente (não versionado)
├── .env.example                     # Modelo de variáveis (para referência)
├── requirements.txt                 # Dependências Python
├── .gitignore                       # Arquivos ignorados pelo Git
└── README.md                        # Esta documentação
```

### Descrição dos arquivos principais

- **`src/main.py`** — Ponto de entrada e controle de fluxo principal. Cria instância do scraper, inicia o navegador e orquestra a coleta de dados.
- **`src/scraper/instagram_scraper.py`** — Implementação do robô Selenium. Gerencia o WebDriver, navega no Instagram e extrai os dados de cada perfil.
- **`src/database/connection.py`** — Abstração da conexão com MySQL. Carrega credenciais do `.env` e oferece método centralizado para conectar ao banco.

## Objetivo e escopo

O projeto foi desenvolvido para:

1. **Abrir** o Instagram no Chrome de forma automatizada
2. **Autenticar** o usuário manualmente uma única vez (sessão persistente)
3. **Navegar** até los perfis públicos especificados em `src/main.py`
4. **Extrair** dados públicos: nome do perfil, número de seguidores, seguindo e publicações
5. **Persistir** os dados em tabela MySQL para posterior análise e auditoria

O sistema é projetado para ser **leve**, **modular** e **escalável**, facilitando extensões futuras (dados adicionais, novos serviços de armazenamento, etc.).

## Dependências

O projeto utiliza as seguintes bibliotecas Python:

| Pacote | Versão | Objetivo |
|--------|--------|----------|
| `selenium` | 4.x+ | Automação de navegador |
| `webdriver-manager` | 4.x+ | Gerenciamento automático do ChromeDriver |
| `mysql-connector-python` | 8.x+ | Conexão com banco MySQL |
| `python-dotenv` | 1.x+ | Carregamento de variáveis de ambiente |

### Instalação das dependências

```bash
# Instalação via pip
pip install -r requirements.txt

# Ou manualmente
pip install selenium webdriver-manager mysql-connector-python python-dotenv
```

## Requisitos do ambiente

Antes de executar, certifique-se de ter:

| Requisito | Versão | Notas |
|-----------|--------|-------|
| Python | 3.8+ | Testado em 3.8 até 3.11 |
| Google Chrome | Última versão | Driver será baixado automaticamente |
| MySQL / MariaDB | 5.7+ | Banco local ou remoto |
| Conexão de internet | - | Necessária para acessar Instagram |
| `.env` configurado | - | Com credenciais do banco (veja seção abaixo) |

## Configuração do banco de dados

### Criação do banco e tabela

Antes de executar o projeto, crie o banco de dados e a tabela que armazenarão os perfis.

**Execute no seu MySQL/MariaDB:**

```sql
CREATE DATABASE instagram_scraper;
USE instagram_scraper;

CREATE TABLE perfis (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) NOT NULL UNIQUE,
  nome VARCHAR(255),
  seguidores VARCHAR(255),
  seguindo VARCHAR(255),
  publicacoes VARCHAR(255),
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_username (username)
);
```

**Explicação do schema:**
- `id`: identificador único (chave primária com auto-increment)
- `username`: nome do usuário do Instagram (chave única para evitar duplicatas)
- `nome`: nome de exibição do perfil
- `seguidores`, `seguindo`, `publicacoes`: dados extraídos (armazenados como texto)
- `criado_em`: timestamp de inserção
- `atualizado_em`: timestamp de última atualização
- `idx_username`: índice para buscas rápidas por username

## Configuração de variáveis de ambiente

### Criar arquivo `.env`

Crie um arquivo chamado `.env` na raiz do projeto com as credenciais do seu banco MySQL:

```env
# Credenciais do banco de dados
DB_HOST=localhost
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=instagram_scraper
```

### Exemplo de `.env` (`.env.example`)

Mantenha também um arquivo `.env.example` no repositório para referência (sem os valores reais):

```env
DB_HOST=localhost
DB_USER=
DB_PASSWORD=
DB_NAME=instagram_scraper
```

### ⚠️ Segurança

- **NUNCA** versionie o arquivo `.env` (adicione à `.gitignore`)
- O `.env` contém credenciais sensíveis
- Compartilhe apenas `.env.example` com a equipe/repositório
- Use contas de teste no banco quando possível

## Como executar

### Pré-requisitos
- Python 3.8+ instalado
- Google Chrome instalado
- MySQL/MariaDB executando
- Arquivo `.env` configurado com credenciais

### Instruções passo a passo

**1. Clone ou baixe o repositório**

```bash
cd instagram-rpa-selenium
```

**2. Crie e ative um ambiente virtual (recomendado)**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

**3. Instale as dependências**

```bash
pip install -r requirements.txt
```

**4. Configure o arquivo `.env`**

Crie/edite `.env` com suas credenciais MySQL na raiz do projeto.

**5. Configure o banco de dados**

Execute o SQL de criação do banco (seção "Configuração do banco de dados" acima).

**6. Execute o projeto**

```bash
# Windows
python src\main.py

# Linux/Mac
python src/main.py
```

**7. Faça login manualmente**

- O Chrome abrirá automaticamente
- Faça login no Instagram manualmente (primeira execução)
- Pressione `ENTER` no terminal após o login
- O script começará a coletar dados dos perfis

### Resultado esperado

Você verá mensagens como:
```
Conectado ao MySQL
Salvo: vincittaco
Salvo: foilcardsoficial
```

Os dados estarão disponíveis na tabela `perfis` do seu banco MySQL.

## Explicação detalhada do código

### Arquitetura geral

```
main.py (orquestração)
  ├── InstagramScraper (coleta de dados)
  │   ├── abrir_instagram()
  │   ├── get_profile_data()
  │   └── fechar()
  └── salvar_dados() 
      └── get_connection() (conexão MySQL)
```

### `src/main.py` — Ponto de entrada

Este arquivo é responsável por orquestrar todo o fluxo de execução.

**Importações:**
```python
from scraper.instagram_scraper import InstagramScraper
from database.connection import get_connection
```

#### Função `salvar_dados(dados)`

Persiste os dados coletados no banco MySQL.

**Processo:**
1. Abre conexão MySQL via `get_connection()`
2. Prepara statement SQL preparado: `INSERT INTO perfis (...) VALUES (%s, %s, %s, %s, %s)`
3. Extrai valores do dicionário `dados` e monta tupla `valores`
4. Executa o INSERT, faz `commit()` e fecha recursos
5. Em caso de erro, imprime mensagem descritiva

**Tratamento de erros:** Usa try/except para capturar exceções de conexão ou SQL.

#### Função `main()`

Orquestra o fluxo completo de coleta.

**Etapas:**
1. Instancia `InstagramScraper()`
2. Chama `scraper.abrir_instagram()` para carregar a página inicial
3. Define lista de usuários a coletar
4. Para cada usuário:
   - Llama `scraper.get_profile_data(user)`
   - Se dados válidos, chama `salvar_dados(dados)`
5. Ao fim, libera recursos com `scraper.fechar()`

### `src/scraper/instagram_scraper.py` — Lógica de scraping

Implementa toda a automação com Selenium para extrair dados do Instagram.

#### Método `__init__`

Configura as opções do Chrome e inicializa o WebDriver.

**Configurações:**
- `--start-maximized`: Abre o Chrome em modo tela cheia
- `--user-data-dir=C:\selenium\instagram_profile`: Usa perfil persistente para manter login salvo entre execuções
- `ChromeDriverManager().install()`: Baixa driver automaticamente (sem necessidade de configuração manual)

> **Nota importante:** O caminho `C:\selenium\instagram_profile` é fixo. Para usar outro diretório, edite essa linha no código.

#### Método `abrir_instagram()`

Carrega a página inicial do Instagram e aguarda login manual.

**Fluxo:**
1. Acessa `https://www.instagram.com/`
2. Exibe mensagem: `👉 Faça login UMA vez e pressione ENTER...`
3. Aguarda o usuário fazer login manualmente no Chrome
4. Ao pressionar ENTER, a sessão é salva no perfil persistente

**Por quê login manual?** Por razões de segurança — evita armazenar credenciais em código.

#### Método `get_profile_data(username)`

Navega até um perfil específico e extrai os dados públicos.

**Processo detalhado:**

1. **Navegação:** Acessa `https://www.instagram.com/{username}/`

2. **Espera de carregamento:** Usa `WebDriverWait` com timeout de 15 segundos para aguardar elemento `<header>` aparecer

3. **Extração do nome:** Localiza `<h2>` dentro do header (nome de exibição)

4. **Extração de seguidores/seguindo:**
   - Busca todos os `<span>` dentro do header
   - Procura por textos contendo `seguidor`, `followers`, `seguindo`, `following`
   - Captura os valores encontrados (ex: "1,234 followers")

5. **Extração de publicações:** Usa XPath `//header//li[1]//span` para obter o número de posts

6. **Retorno:** Retorna dicionário com campos:
   ```python
   {
       "username": "fulano",
       "nome": "Fulano Silva",
       "seguidores": "1,234 followers",
       "seguindo": "567 following",
       "publicacoes": "89"
   }
   ```

7. **Tratamento de erro:** Se algo falhar, imprime `Erro ao coletar {username}` e retorna `None`

#### Método `fechar()`

Encerra o navegador e libera recursos.
```python
self.driver.quit()  # Fecha Chrome e mata processo
```

### `src/database/connection.py` — Gerenciamento de conexão

Abstrai a conexão com o banco MySQL de forma reutilizável e segura.

**Importações:**
```python
import mysql.connector
import os
from dotenv import load_dotenv
```

#### Função `get_connection()`

Cria e retorna uma conexão com o banco MySQL usando variáveis de ambiente.

**Processo:**

1. `load_dotenv()` — Carrega as variáveis do arquivo `.env` para `os.environ`

2. Lê credenciais via `os.getenv()`:
   - `DB_HOST` — hostname (ex: localhost)
   - `DB_USER` — usuário MySQL
   - `DB_PASSWORD` — senha
   - `DB_NAME` — nome do banco de dados

3. Cria conexão com `mysql.connector.connect()`

4. **Sucesso:** Imprime `Conectado ao MySQL` e retorna objeto de conexão

5. **Erro:** Captura exception, imprime `Erro ao conectar no banco: {e}` e retorna `None`

**Segurança:**
- Credenciais nunca aparecem no código (vêm do `.env`)
- Permite reutilização sem duplicação de lógica
- Centraliza tratamento de erros

## Fluxo de execução completo

```
1. Executa: python src/main.py
   ↓
2. Instancia InstagramScraper()
   ├─ Cria ChromeOptions com perfil persistente
   └─ Inicializa WebDriver com ChromeManager
   ↓
3. Chama scraper.abrir_instagram()
   ├─ Abre https://www.instagram.com/
   └─ Aguarda login manual do usuário
   ↓
4. Para cada username na lista de usuários:
   ├─ Chama get_profile_data(username)
   │  ├─ Navega para https://www.instagram.com/{username}/
   │  ├─ Aguarda carregamento do header (WebDriverWait)
   │  ├─ Extrai nome, seguidores, seguindo, publicações
   │  └─ Retorna dicionário com dados
   │
   └─ Se dados válidos, chama salvar_dados(dados)
      ├─ Abre conexão MySQL
      ├─ Prepara INSERT
      ├─ Executa e faz COMMIT
      └─ Exibe "Salvo: {username}"
   ↓
5. Chama scraper.fechar()
   ├─ driver.quit()
   └─ Encerra Chrome
   ↓
6. Programa finalizado
```

---

## Como adicionar ou remover perfis

Os perfis a coletar são definidos em uma lista dentro de `src/main.py`.

**Localização:**
```python
# Em src/main.py, dentro da função main()
usuarios = [
    "vincittaco",
    "foilcardsoficial",
    "arakinidi_airdunkini",
    "obarbeirodg"
]
```

**Para adicionar um perfil:**
```python
usuarios = [
    "vincittaco",
    "foilcardsoficial",
    "arakinidi_airdunkini",
    "obarbeirodg",
    "novo_usuario_aqui"  # ← Adicione aqui
]
```

**Para remover um perfil:**
```python
usuarios = [
    "vincittaco",
    "foilcardsoficial"
    # removeu arakinidi_airdunkini e obarbeirodg
]
```

**Carregamento dinâmico (melhoria futura):**
Você pode modificar `main.py` para ler a lista de um arquivo CSV/JSON:
```python
import json

with open('usuarios.json', 'r') as f:
    usuarios = json.load(f)
```

## Observações técnicas importantes

### Login persistente

O projeto usa cookies e dados persistentes do Chrome armazenados em `C:\selenium\instagram_profile`.

**Vantagens:**
- Login realizado uma única vez
- Cada execução reutiliza a sessão existente
- Mais rápido e seguro

**Como funciona:**
```
--user-data-dir=C:\selenium\instagram_profile
```

Isso instrui o Chrome a usar este diretório como perfil do usuário (salva cookies, cache, etc).

### Fragilidade do HTML/CSS do Instagram

O scraper depende da estrutura HTML do Instagram, que **muda frequentemente**.

**Elementos monitorados:**
- `<header>` — presente na página de perfil
- `<h2>` — contém nome de exibição
- `<span>` — contém textos de followers/following (variam entre PT e EN)
- `//header//li[1]//span` — número de publicações via XPath

**O que pode quebrar:**
Se o Instagram reformular sua página de perfil (mudança comum), o scraper pode:
- Retornar `None` nos campos
- Coletar valores incorretos
- Falhar completamente

**Solução:**
Monitore as mensagens de erro e atualize os seletores CSS/XPath conforme necessário.

### Riscos e limitações

| Risco | Descrição | Mitigação |
|-------|-----------|-----------|
| **Bloqueio de IP** | Instagram pode bloquear IPs fazendo muitas requisições | Use conta de teste, respeite rate limits |
| **Detecção de bot** | Comportamento anômalo pode ser detectado | Login manual, sessão persistente |
| **Termos de serviço** | Scraping pode violar TOS do Instagram | Use apenas para perfis públicos, pesquisa legítima |
| **Dados privados** | O script acessa apenas dados públicos | Está ciente de que perfis privados mostram "Não disponível" |
| **Mudanças de layout** | Instagram redesenha interface com frequência | Atualize XPath/CSS quando necessário |

## Roadmap e possíveis melhorias

| ID | Implementação | Prioridade | Status | Descrição |
|----|----|-----------|--------|-----------|
| 1 | Login automático | Alta | ⏳ Planejado | Adicionar suporte a credenciais automáticas (com criptografia) |
| 2 | Extração de mais campos | Alta | ⏳ Planejado | Bio, link pessoal, localização, stories, posts recentes |
| 3 | Suporte a CSV/JSON | Média | ⏳ Planejado | Exportar dados em múltiplos formatos além de MySQL |
| 4 | Modo headless | Média | ⏳ Planejado | Rodar Chrome sem interface (mais eficiente em servidores) |
| 5 | Suporte a proxies | Alta | ⏳ Planejado | Rotacionar IPs para evitar bloqueios |
| 6 | Retry automático | Média | ⏳ Planejado | Tentar novamente perfis que falharam |
| 7 | Logs estruturados | Média | ⏳ Planejado | Usar `logging` em vez de `print()` |
| 8 | Configuração dinâmica | Média | ⏳ Planejado | Ler perfis de arquivo JSON/CSV durante execução |
| 9 | API REST | Baixa | ⏳ Explorando | Expor dados via Flask/FastAPI |
| 10 | Testes unitários | Alta | ⏳ Planejado | Coverage para principais funções |

## Troubleshooting e erros comuns

### Erro: `Erro ao conectar no banco`

**Possíveis causas:**
- MySQL não está rodando
- Credenciais incorretas no `.env`
- Firewall bloqueando conexão
- Banco MySQL remoto indisponível

**Soluções:**
```bash
# Verificar se MySQL está rodando (Windows)
netstat -ano | findstr :3306

# Verificar se MySQL está rodando (Linux)
sudo systemctl status mysql

# Testar conexão MySQL via CLI
mysql -h localhost -u seu_usuario -p

# Verificar conteúdo do .env
cat .env  # Linux/Mac
type .env  # Windows
```

### Erro: `Erro ao coletar {username}: ...`

**Possíveis causas:**
- Perfil não existe ou foi deletado
- Perfil é privado (dados não disponíveis)
- Instagram bloqueou/detectou automação
- Estrutura HTML do Instagram mudou

**Soluções:**
```python
# Adicione verificação de perfil válido
try:
    # Verificar se perfil existe
    if "Página não encontrada" in driver.page_source:
        return None
except Exception as e:
    print(f"Erro ao validar perfil: {e}")
    return None
```

### Chrome abre mas não coleta dados

**Possíveis causas:**
- Login não foi realizado (pressionar ENTER sem logar)
- Sessão expirou
- Usando Chrome headless (não suportado com perfil persistente)

**Soluções:**
```bash
# Deletar perfil do Chrome e fazer login novamente
rmdir /s "C:\selenium\instagram_profile"  # Windows
rm -rf ~/.selenium/instagram_profile      # Linux/Mac

# Aumentar timeout de espera (em instagram_scraper.py)
wait = WebDriverWait(self.driver, 30)  # ao invés de 15
```

### ChromeDriver não encontrado

**Possível causa:**
- `webdriver-manager` não foi instalado

**Solução:**
```bash
pip install webdriver-manager
```

### ImportError: No module named 'selenium'

**Solução:**
```bash
pip install -r requirements.txt
# ou
pip install selenium webdriver-manager mysql-connector-python python-dotenv
```

## Considerações de segurança

- **Credenciais:** Nunca compartilhe/commit o arquivo `.env` com dados reais
- **Conta de teste:** Use uma conta testing no Instagram para reduzir riscos
- **Banco de dados:** Use usuário MySQL com permissões mínimas (apenas a database necessária)
- **IP/Proxy:** Considere usar  proxies se fizer scraping em escala, para não ser bloqueado
- **Dados pessoais:** Respeite privacidade — colete apenas dados públicos e com direito legal
- **Rate limiting:** Adicione delays entre requisições para não sobrecarregar servidores
- **Validação de dados:** Sempre valide dados extraídos antes de inserir no banco

### Exemplo de configuração segura de usuário MySQL

```sql
-- Criar usuário com permissões mínimas
CREATE USER 'instagram_bot'@'localhost' IDENTIFIED BY 'senha_forte_aqui';

-- Permissões apenas na database instagram_scraper
GRANT SELECT, INSERT, UPDATE ON instagram_scraper.* TO 'instagram_bot'@'localhost';

-- Aplicar permissões
FLUSH PRIVILEGES;
```

## Histórico de mudanças (Changelog)

### v1.1.0 — Documentação completa e melhorias estruturais
**Data:** 06/04/2026

#### Adições
- ✨ Badges de status e compatibilidade no README
- ✨ Tabelas de requisitos, dependências e roadmap
- ✨ Diagramas de arquitetura e fluxo de execução
- ✨ Seção detalhada de Troubleshooting com soluções práticas
- ✨ Exemplos de código e configurações seguras
- ✨ Migração de lista simples para tabela estruturada de melhorias
- ✨ Dicas de segurança com exemplo de usuário MySQL restrito
- ✨ Suporte a `.env.example` documentado

#### Melhorias
- 📝 Reorganização completa da estrutura do README
- 📝 Escrita mais técnica e profissional
- 📝 Explicação detalhada de cada método/função
- 📝 Clarificação do fluxo de execução passo a passo
- 📝 Índice melhorado de navegação
- 📝 Adição de exemplos práticos em Python/SQL/Bash

#### Correções
- ✅ Resolvidos merge conflicts no README
- ✅ Padronização de nomenclatura de variáveis
- ✅ Ajuste de paths para compatibilidade cross-plataform

#### Tarefas agora documentadas
- 📌 Schema MySQL com índices e timestamps
- 📌 Carregamento dinâmico de usuários via JSON (como melhoria futura)
- 📌 Operações CRUD esperadas no banco
- 📌 Rate limiting e estratégias anti-bloqueio

---

### v1.0.0 — Release inicial
**Data:** Inicial (anterior)

#### Incluído
- ✅ Scraper Selenium básico
- ✅ Conexão MySQL funcional
- ✅ Login persistente via Chrome profile
- ✅ Extração de dados: nome, seguidores, seguindo, publicações
- ✅ Tratamento básico de erros
- ✅ Documentação inicial

---

## Guia de referência rápida

### Arquivos do projeto

| Arquivo | Objetivo |
|---------|----------|
| `src/main.py` | Orquestração e controle do fluxo |
| `src/scraper/instagram_scraper.py` | Automação Selenium + extração de dados |
| `src/database/connection.py` | Gerenciamento de conexão MySQL |
| `.env` | Credenciais (não versionado) |
| `requirements.txt` | Dependências Python |
| `README.md` | Esta documentação |

### Mensagens de log durante execução

```
Conectado ao MySQL           # ✅ Conexão bem-sucedida
Salvo: vincittaco            # ✅ Perfil salvo no banco
Erro no banco: {e}           # ❌ Falha ao persistir
Erro ao coletar username: {e} # ❌ Falha ao extrair dados
```

### Variáveis de ambiente (.env)

```env
DB_HOST=localhost              # Host MySQL
DB_USER=seu_usuario            # Usuário MySQL
DB_PASSWORD=sua_senha          # Senha (NÃO comitar!)
DB_NAME=instagram_scraper      # Nome do banco
```

### Comandos úteis

```bash
# Executar o scraper
python src/main.py

# Testar conexão MySQL
mysql -h localhost -u seu_usuario -p sua_senha

# Visualizar dados coletados
SELECT * FROM perfis ORDER BY criado_em DESC;

# Deletar dados (cuidado!)
TRUNCATE TABLE perfis;
```

---

## Próximas ações recomendadas

1. **Setup inicial:**
   - [ ] Instalar Python 3.8+
   - [ ] Instalar Google Chrome
   - [ ] Instalar MySQL
   - [ ] Clonar/baixar o repositório

2. **Configuração:**
   - [ ] Criar `.env` com credenciais
   - [ ] Criar database e tabela no MySQL (ver SQL acima)
   - [ ] Instalar dependências: `pip install -r requirements.txt`

3. **Testes:**
   - [ ] Executar `python src/main.py`
   - [ ] Fazer login no Instagram
   - [ ] Confirmar dados na tabela `perfis`

4. **Próximas melhorias:**
   - [ ] Adicionar suporte a CSV/JSON export
   - [ ] Implementar login automático com credenciais criptografadas
   - [ ] Adicionar retry automático para perfis que falharem
   - [ ] Criar interface web simples (Django/Flask)
   - [ ] Implementar testes unitários

5. **Manutenção contínua:**
   - [ ] Monitorar mudanças no layout do Instagram
   - [ ] Atualizar seletores XPath/CSS quando necessário
   - [ ] Revisar logs de erro regularmente
   - [ ] Fazer backups do banco MySQL

---

## Contribuição e suporte

### Reportar bugs
Se encontrar problemas, verifique:
1. Arquivo `.env` está correto?
2. MySQL está rodando?
3. Chrome está atualizado?
4. Estrutura HTML do Instagram mudou?

### Solicitar features
Prefixe o título com:
- `[FEATURE]` para novas funcionalidades
- `[BUG]` para bugs encontrados
- `[DOCS]` para melhorias de documentação

---

## Licença

Este projeto é fornecido como-é para fins educacionais e de pesquisa. Use com responsabilidade e respeite os termos de serviço do Instagram.

