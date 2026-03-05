"""
Ponto de entrada para execução da API FastAPI em modo de desenvolvimento.

Execute, por exemplo:

    uvicorn app.main:app --reload

O módulo `app.main` contém a instância FastAPI com todas as rotas.
"""

from app.main import app  # noqa: F401
    