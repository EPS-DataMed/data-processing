
# Data Processing

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=EPS-DataMed_data-processing&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=EPS-DataMed_data-processing) [![Coverage](https://sonarcloud.io/api/project_badges/measure?project=EPS-DataMed_data-processing&metric=coverage)](https://sonarcloud.io/summary/new_code?id=EPS-DataMed_data-processing) [![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=EPS-DataMed_data-processing&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=EPS-DataMed_data-processing)

## Descrição do Projeto

Este projeto tem como objetivo fornecer uma solução completa para processamento de dados. Utilizando tecnologias modernas, o projeto oferece uma solução robusta e funcionalidades para manipulação e análise de exames.

## Pré-requisitos

- Python 3.8 ou superior
- `venv` para gerenciamento de ambientes virtuais
- Dependências listadas em `requirements.txt`

## Instalação Local

Siga os passos abaixo para configurar o ambiente de desenvolvimento local:

1. **Clone o repositório**

   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd data-processing-main
   ```

2. **Crie e ative um ambiente virtual**

   ```bash
   python -m venv venv
   source venv/bin/activate   # No Windows, use `venv\Scripts\activate`
   ```

3. **Instale as dependências**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente**

   Crie um arquivo `.env` na raiz do projeto e copie o conteúdo do arquivo `.env.example`, ajustando os valores conforme necessário.

5. **Execute a aplicação**

   ```bash
   uvicorn app.main:app --reload
   ```

   A aplicação estará disponível em `http://127.0.0.1:8000`.

## Testes

Para executar os testes, utilize o comando abaixo:

```bash
pytest
```

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
