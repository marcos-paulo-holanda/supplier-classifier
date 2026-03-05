from fastapi import FastAPI

from app.api.v1.routes import router as v1_router

app = FastAPI(
    title="Supplier Classifier API",
    version="1.0.0",
    description=(
        "API para classificação de fornecedores a partir de um CNPJ, "
        "utilizando regras de negócio e modelos semânticos."
    ),
)


@app.get("/", tags=["health"])
def health_check() -> dict:
    """
    Endpoint simples de saúde da aplicação.
    """

    return {"status": "ok"}


app.include_router(v1_router)

