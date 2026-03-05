from collections import defaultdict
from time import time
from typing import Dict, List

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel

from app.services.supplier_service import (
    SupplierClassificationService,
    get_supplier_service,
)
import os


load_dotenv()

RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT", "3"))
_WINDOW_SECONDS = 60
_requests_by_ip: Dict[str, List[float]] = defaultdict(list)


def rate_limiter(request: Request) -> None:
    """
    Limita a quantidade de requisições por IP em uma janela de 1 minuto.
    O limite é configurado pela variável RATE_LIMIT no arquivo .env.
    """

    client_ip = request.client.host if request.client else "anonymous"
    now = time()

    timestamps = _requests_by_ip[client_ip]
    # mantém apenas requisições dentro da janela
    timestamps = [ts for ts in timestamps if now - ts < _WINDOW_SECONDS]

    if len(timestamps) >= RATE_LIMIT_PER_MINUTE:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Limite de requisições excedido. Tente novamente em instantes.",
        )

    timestamps.append(now)
    _requests_by_ip[client_ip] = timestamps


class CategoriasAssociadasResponse(BaseModel):
    cnpj: str
    categorias_associadas: List[str]


class CategoriaClassificadaResponse(BaseModel):
    cnpj: str
    categoria_classificada: str


router = APIRouter(prefix="/api/v1", tags=["supplier-classifier"])


@router.get(
    "/categorias-associadas/{cnpj}",
    response_model=CategoriasAssociadasResponse,
    summary="Retorna categorias associadas para o CNPJ informado.",
    description=(
        "Busca dados do CNPJ na API pública do CNPJws e aplica as regras de "
        "detecção/associação de categorias com base no nome fantasia."
    ),
)
def obter_categorias_associadas(
    cnpj: str,
    _: None = Depends(rate_limiter),
    service: SupplierClassificationService = Depends(get_supplier_service),
) -> CategoriasAssociadasResponse:
    try:
        categorias = service.obter_categorias_associadas(cnpj)
        return CategoriasAssociadasResponse(cnpj=cnpj, categorias_associadas=categorias)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(exc),
        ) from exc
    except Exception as exc:  # pragma: no cover - fallback genérico
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Erro ao consultar informações do CNPJ.",
        ) from exc


@router.get(
    "/categorias-classificadas/{cnpj}",
    response_model=CategoriaClassificadaResponse,
    summary="Retorna a categoria classificada para o CNPJ informado.",
    description=(
        "Busca dados do CNPJ na API pública do CNPJws e aplica o classificador "
        "semântico com base na atividade econômica principal da empresa."
    ),
)
def obter_categoria_classificada(
    cnpj: str,
    _: None = Depends(rate_limiter),
    service: SupplierClassificationService = Depends(get_supplier_service),
) -> CategoriaClassificadaResponse:
    try:
        categoria = service.obter_categoria_classificada(cnpj)
        return CategoriaClassificadaResponse(
            cnpj=cnpj,
            categoria_classificada=categoria,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(exc),
        ) from exc
    except Exception as exc:  # pragma: no cover - fallback genérico
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Erro ao consultar informações do CNPJ.",
        ) from exc

