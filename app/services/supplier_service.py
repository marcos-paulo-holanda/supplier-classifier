from functools import lru_cache
from typing import List

from app.domain.categories_list import categories_list

from app.domain.associator import AssociadorCategoriaFornecedor
from app.domain.cnpj_client import CNPJClient
from app.domain.detector import DetectorCategoriaFornecedor
from app.domain.semantic_classifier import ClassificadorSemantico


class SupplierClassificationService:
    """
    Serviço responsável por orquestrar a consulta de CNPJ e a classificação
    nas categorias de fornecedores.
    """

    def __init__(self) -> None:
        self.cnpj_client = CNPJClient()
        self.categorias = categories_list
        self.detector = DetectorCategoriaFornecedor(self.categorias)
        self.associador = AssociadorCategoriaFornecedor(self.categorias)
        self.classificador = ClassificadorSemantico(self.categorias)

    def _obter_dados_empresa(self, cnpj: str) -> dict:
        return self.cnpj_client.consultar(cnpj)

    def obter_categorias_associadas(self, cnpj: str) -> List[str]:
        """
        Retorna categorias associadas com base no nome fantasia.
        """
        dados = self._obter_dados_empresa(cnpj)
        nome_fantasia = dados["estabelecimento"]["nome_fantasia"]

        categorias_associadas = self.detector.buscar_categoria(nome_fantasia)
        if not categorias_associadas:
            categorias_associadas = self.associador.associar(nome_fantasia)

        return categorias_associadas

    def obter_categoria_classificada(self, cnpj: str) -> str:
        """
        Retorna uma categoria classificada com base na atividade principal.
        """
        dados = self._obter_dados_empresa(cnpj)
        atividade_principal = dados["estabelecimento"]["atividade_principal"][
            "descricao"
        ]
        return self.classificador.classificar(atividade_principal)


@lru_cache()
def get_supplier_service() -> SupplierClassificationService:
    """
    Fornece uma instância singleton do serviço para ser usada via injeção
    de dependência no FastAPI.
    """

    return SupplierClassificationService()

