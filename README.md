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

É ideal para pesquisas, auditorias de marcas, coleta de métricas e análises de contas públicas.

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
pip install -r requirements.txt
```

## Requisitos do ambiente

| Requisito | Versão | Notas |
|-----------|--------|-------|
| Python | 3.8+ | Testado em 3.8 até 3.11 |
| Google Chrome | Última versão | Driver será baixado automaticamente |
| MySQL / MariaDB | 5.7+ | Banco local ou remoto |
| Conexão de internet | - | Necessária para acessar Instagram |
| `.env` configurado | - | Com credenciais do banco |

## Configuração do banco de dados

### Criação do banco e tabela

Execute no seu MySQL/MariaDB:

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

## Configuração de variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DB_HOST=localhost
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=instagram_scraper
```

### ⚠️ Segurança

- **NUNCA** versionie o arquivo `.env` (já está em `.gitignore`)
- Mantenha `.env.example` no repositório como referência (sem valores reais)

## Como executar

### Pré-requisitos
- Python 3.8+ instalado
- Google Chrome instalado
- MySQL/MariaDB executando
- Arquivo `.env` configurado

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

Execute o SQL de criação do banco (seção acima).

**6. Execute o projeto**

```bash
# Windows
python src\main.py

# Linux/Mac
python src/main.py
```

**7. Faça login manualmente**

- O Chrome abrirá automaticamente
- Faça login no Instagram manualmente
- Pressione `ENTER` no terminal após o login
- O script começará a coletar dados dos perfis

### Resultado esperado

```
Conectado ao MySQL
Salvo: vincittaco
Salvo: foilcardsoficial
```

Os dados estarão disponíveis na tabela `perfis` do seu banco MySQL.

## Como adicionar ou remover perfis

Os perfis a coletar são definidos em uma lista dentro de `src/main.py`:

```python
# Em src/main.py, função main()
usuarios = [
      "vincittaco",
      "foilcardsoficial",
      "arakinidi_airdunkini",
      "obarbeirodg"
]
```

**Para adicionar:** Adicione o username à lista

**Para remover:** Remova o username da lista

## Observações técnicas

### Login persistente

O projeto usa cookies e dados persistentes do Chrome para manter a sessão entre execuções. Login é realizado uma única vez.

### Fragilidade do DOM do Instagram

O scraper depende da estrutura HTML do Instagram, que muda frequentemente. Se o Instagram reformular sua página de perfil, os seletores podem quebrar.

**Solução:** Atualize os seletores CSS/XPath em `instagram_scraper.py` conforme necessário.

### Limitações

| Limitação | Descrição |
|-----------|-----------|
| **Perfis privados** | Dados não disponíveis para perfis privados |
| **Mudanças de layout** | Instagram redesenha interface com frequência |
| **Bloqueios** | Instagram pode bloquear comportamento automatizado |
| **Rate limits** | Múltiplas requisições rápidas podem resultar em restrições |

## Troubleshooting

### Erro: `Erro ao conectar no banco`

**Soluções:**
- Verificar se MySQL está rodando
- Verificar credenciais em `.env`
- Testar conexão: `mysql -h localhost -u seu_usuario -p`

### Erro: `Erro ao coletar {username}`

**Possíveis causas:**
- Perfil não existe
- Perfil é privado
- Instagram bloqueou/detectou automação
- Estrutura HTML do Instagram mudou

### Chrome não coleta dados

**Soluções:**
- Confirmar que fez login e pressionou ENTER
- Deletar perfil do Chrome e fazer login novamente
- Aumentar timeout de espera em `instagram_scraper.py`

### ImportError: No module named 'selenium'

```bash
pip install -r requirements.txt
```

## Segurança

- Nunca compartilhe arquivos com credenciais reais
- Use uma conta de teste no Instagram
- Considere usar proxies para scraping em escala
- Respeite os termos de serviço do Instagram
- Colete apenas dados públicos

## Licença

Este projeto é fornecido como-é para fins educacionais e de pesquisa.
