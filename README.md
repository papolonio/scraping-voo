# Scraping-VOO

Um crawler modular e configurável desenvolvido em Python + Selenium, projetado para automatizar a coleta de dados de companhias aéreas (ex: Latam, Azul, Gol) com integração a Redis, MongoDB e execução em containers Docker.

---

## Principais Funcionalidades

- Arquitetura genérica e extensível baseada em classes abstratas (AbstractCrawler)
- Orquestração dinâmica via JSON armazenado no Redis (steps before / main / after)
- Execução headless com o Chrome controlado via Selenium (BrowserProvider)
- Armazenamento automático dos resultados no MongoDB
- Suporte a múltiplos crawlers (Latam, Azul etc.) com apenas troca de configuração
- Escalável — novos sites podem ser adicionados sem alterar o core, apenas criando novos steps

---

## Estrutura do Projeto

