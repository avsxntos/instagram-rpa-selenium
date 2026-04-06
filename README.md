# 📌 Instagram RPA com Selenium + MySQL

## 📖 Visão geral

Este projeto é um **Robotic Process Automation (RPA)** desenvolvido em Python com Selenium para coleta automatizada de dados públicos de perfis do Instagram.

Ele acessa perfis, extrai informações básicas (nome, seguidores, seguindo, publicações) e salva esses dados em um banco de dados MySQL.

O sistema também possui:
- login persistente (sessão salva)
- scraping automatizado
- estrutura modular
- integração com banco de dados
- código preparado para expansão

---

# ⚙️ Tecnologias utilizadas

- Python 3.x
- Selenium
- WebDriver Manager
- MySQL
- ChromeDriver
- SQL (Workbench ou CLI)

---

# 📁 Estrutura do projeto


instagram-rpa-selenium/
│
├── src/
│ ├── scraper/
│ │ └── instagram_scraper.py
│ │
│ ├── database/
│ │ └── connection.py
│ │
│ └── main.py
│
├── docs/
│ ├── arquitetura.md
│ ├── banco_dados.md
│ └── fluxo.md
│
├── .env
├── requirements.txt
└── README.md


---

