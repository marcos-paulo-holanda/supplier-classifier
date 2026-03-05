## Supplier Classifier API

API para classificação de fornecedores a partir de um **CNPJ**, utilizando regras de negócio (detecção e associação de categorias) e um **classificador semântico** baseado em `sentence-transformers`.

### Estrutura do projeto

- **`app/`**: pacote principal da aplicação.
  - **`app/main.py`**: instancia a aplicação FastAPI e registra as rotas.
  - **`app/api/v1/`**: camada de API (rotas HTTP).
    - `routes.py`: define os endpoints da versão 1 da API.
  - **`app/services/`**: orquestra chamadas à API de CNPJ e às regras de negócio.
    - `supplier_service.py`: serviço de classificação de fornecedores.
  - **`app/domain/`**: regras de negócio e integrações de baixo nível.
    - `cnpj_client.py`: cliente HTTP para a API pública do CNPJws.
    - `detector.py`: detecção direta de categorias no nome fantasia.
    - `associator.py`: associação aproximada de categorias ao nome fantasia.
    - `semantic_classifier.py`: classificador semântico baseado em embeddings.
- **Arquivos de apoio no diretório raiz**:
  - `categories_list.py`: lista de categorias disponíveis.
  - `categories_synonyms.py`: sinônimos/exemplos por categoria.
  - `requirements.txt`: dependências do projeto.
  - `main.py`: atalho para execução da API (entrypoint uvicorn).

### Como instalar

Recomenda-se o uso de um ambiente virtual:

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### Como executar a API

Dentro da raiz do projeto, execute:

```bash
uvicorn app.main:app --reload
```

Por padrão, a aplicação ficará disponível em `http://127.0.0.1:8000`.

### Endpoints principais

- **Health check**
  - **GET** `/`
  - Retorna o status simples da aplicação.

- **Categorias associadas**
  - **GET** `/api/v1/categorias-associadas/{cnpj}`
  - **Parâmetros**
    - `cnpj` (path): CNPJ da empresa (com ou sem máscara).
  - **Resposta**
    - `cnpj`: CNPJ recebido.
    - `categorias_associadas`: lista de categorias encontradas com base no **nome fantasia** da empresa.

- **Categorias classificadas (semântico)**
  - **GET** `/api/v1/categorias-classificadas/{cnpj}`
  - **Parâmetros**
    - `cnpj` (path): CNPJ da empresa (com ou sem máscara).
  - **Resposta**
    - `cnpj`: CNPJ recebido.
    - `categoria_classificada`: categoria mais provável com base na **atividade principal** da empresa.

### Documentação automática

Ao rodar a API, a documentação interativa gerada pelo FastAPI estará disponível em:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

Nesses endpoints você pode testar as rotas e visualizar o schema completo da API.

