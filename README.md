
## Descrição

**Scraping-VOO** é um projeto desenvolvido com o objetivo de criar um crawler modular e configurável em Python + Selenium, projetado para automatizar a coleta de dados de companhias aéreas (como Latam, Azul e Gol).

A arquitetura foi construída com foco em flexibilidade, escalabilidade e manutenção, utilizando Redis para armazenar fluxos dinâmicos de execução (Data-Driven Automation) e MongoDB para persistência dos dados coletados.
Todo o ambiente é orquestrado via Docker Compose, garantindo reprodutibilidade e fácil implantação.

## Índice

- [Principais Características](#principais-características)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Arquitetura do Projeto](#arquitetura-do-projeto)
- [Diagrama de Fluxo de Execução](#diagrama-de-fluxo-de-execução)

## Principais Características

- **Automação Data-Driven**: O comportamento do crawler é definido por scripts JSON armazenados no Redis, permitindo alta flexibilidade.
- **Execução Headless**: Utiliza o Selenium com navegador em modo *headless*, otimizando a execução em servidores sem interface gráfica.
- **Persistência Robusta**: Armazena os resultados da coleta de forma estruturada em um banco de dados NoSQL (MongoDB).
- **Ambiente Containerizado**: Facilidade para subir todo o ambiente de desenvolvimento e produção com um único comando (`docker-compose up`).
- **Gerenciamento de Dependências Moderno**: Usa o [Poetry](https://python-poetry.org/) para um gerenciamento de pacotes e dependências limpo e determinístico.
- **Arquitetura Escalável**: Projetado para escalabilidade horizontal, permitindo que múltiplos crawlers rodem como containers independentes.

## Tecnologias Utilizadas

- **Linguagem**: Python 3.12
- **Automação Web**: Selenium
- **Banco de Dados**: MongoDB (para armazenamento dos resultados)
- **Cache**: Redis (para armazenamento dos scripts de passos)
- **Orquestração**: Docker & Docker Compose
- **Gerenciador de Dependências**: Poetry

## Arquitetura do Projeto

A estrutura de diretórios foi organizada para separar responsabilidades e facilitar a manutenção:
```
src/
├── crawler/
│   ├── abstract_crawler.py     # Classe base com o fluxo genérico (Template Method)
│   ├── old_abstract_crawler.py # Versão anterior para referência
│   └── __init__.py
├── tools/
│   ├── browser_provider.py     # Configura e fornece a instância do navegador Selenium
│   ├── mongodb.py              # Gerencia a conexão e persistência no MongoDB
│   ├── redis.py                # Responsável pela leitura dos steps do Redis
│   └── steps/
│       └── actions.py          # Módulo com as ações dinâmicas (click, input, wait, etc.)
├── __main__.py                 # Ponto de entrada (entrypoint) da aplicação
└── generic_crawler.py          # Implementação concreta que orquestra o processo
```

## Diagrama de Fluxo de Execução

O fluxo de trabalho mostra o `GenericCrawler` como o orquestrador central, lendo as instruções do Redis, interagindo com o site alvo via Selenium, e persistindo os resultados no MongoDB.

```text
+------------------------+
|         Redis          |
| (Armazena steps/JSON)  |
+-----------+------------+
            |
            | 1. Crawler lê os passos de execução
            |
            v
+------------------------+                                 +-----------------+
|     GenericCrawler     | --- 2. Executa ações via --->   |     Selenium    | ---> (Site Alvo)
|   (Orquestrador Lógico)| <---    (Retorna dados)    <--- |    WebDriver    |
+-----------+------------+
            |
            | 3. Crawler formata e prepara os dados extraídos
            |
            v
+------------------------+
|        MongoDB         |
|  (Salva os resultados) |
+------------------------+

