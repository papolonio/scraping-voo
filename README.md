# Scraping-VOO

<p align="center">
  <img alt="Python Version" src="[https://img.shields.io/badge/python-3.12-blue.svg](https://img.shields.io/badge/python-3.12-blue.svg)">
  <img alt="License" src="[https://img.shields.io/badge/license-MIT-green.svg](https://img.shields.io/badge/license-MIT-green.svg)">
  <img alt="Status" src="[https://img.shields.io/badge/status-ativo-brightgreen.svg](https://img.shields.io/badge/status-ativo-brightgreen.svg)">
</p>

## Descrição

**Scraping-VOO** é um crawler modular e configurável desenvolvido em Python e Selenium, projetado para automatizar a coleta de dados de voos em sites de companhias aéreas (como Latam, Azul, Gol).

A arquitetura do projeto utiliza um fluxo de automação orientado a dados (*Data-Driven*), onde os passos da raspagem (cliques, preenchimento de formulários, esperas) são definidos em formato JSON e armazenados no **Redis**. Isso permite modificar ou adicionar novos fluxos de coleta sem alterar o código principal do crawler. Os dados coletados são persistidos em um banco de dados **MongoDB**, e todo o ambiente (aplicação, banco e cache) é orquestrado de forma simples e eficiente com **Docker Compose**.

## Índice

- [Principais Características](#principais-características)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Arquitetura do Projeto](#arquitetura-do-projeto)
- [Diagrama de Fluxo de Execução](#diagrama-de-fluxo-de-execução)
- [Pré-requisitos](#pré-requisitos)
- [Como Executar Localmente](#como-executar-localmente)
- [Conceitos de Arquitetura Aplicados](#conceitos-de-arquitetura-aplicados)
- [Autor](#autor)
- [Licença](#licença)

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

