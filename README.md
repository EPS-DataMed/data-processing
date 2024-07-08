
# Data Processing

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=EPS-DataMed_data-processing&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=EPS-DataMed_data-processing)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=EPS-DataMed_data-processing&metric=coverage)](https://sonarcloud.io/summary/new_code?id=EPS-DataMed_data-processing)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=EPS-DataMed_data-processing&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=EPS-DataMed_data-processing)

## Descrição do Projeto

Este projeto tem como objetivo fornecer uma solução completa para processamento de dados. Utilizando tecnologias modernas, o projeto oferece uma solução robusta e funcionalidades para manipulação e extração de dados de exames médicos.

## Configuração do ambiente de desenvolvimento local

### Pré-requisitos

- Python 3.11 ou superior
- `venv` para gerenciamento de ambientes virtuais
- Dependências listadas em `requirements.txt`

Siga os passos abaixo para configurar o ambiente de desenvolvimento local:

1. **Clone o repositório**

   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd data-processing
   ```

2. **Crie e ative um ambiente virtual**

   ```bash
   python -m venv venv
   source venv/bin/activate   # No Windows, use `venv\Scripts\activate`
   ```

3. **Instale as dependências**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt 
   ```

4. **Configure as variáveis de ambiente**

   Crie um arquivo `.env` na raiz do projeto e copie o conteúdo do arquivo `.env.example`, ajustando os valores conforme necessário.

5. **Execute a aplicação**

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8004 --reload
   ```

   A aplicação estará disponível em `http://127.0.0.1:8004`.

### Testes

1. Para executar os testes, utilize o comando abaixo:

    ```bash
    pytest
    ```

## Configuração do ambiente de desenvolvimento com Docker

### Pré-requisitos

- Docker
- Docker Compose

1. **Configure as variáveis de ambiente (caso ainda não tenha configurado)**

   Crie um arquivo `.env` na raiz do projeto e copie o conteúdo do arquivo `.env.example`, ajustando os valores conforme necessário.

2. **Construir a imagem Docker**
    ```bash
    docker-compose build
    ```

3. **Executar o container**
    ```bash
    docker-compose up
    ```

A aplicação estará disponível em `http://127.0.0.1:8004`.

## Licença

Este projeto está licenciado sob a [MIT License](./LICENSE).