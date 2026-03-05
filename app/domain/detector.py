import unicodedata
from typing import List


class DetectorCategoriaFornecedor:
    """
    Verifica se o nome da categoria está presente no nome do fornecedor.
    """

    def __init__(self, categorias: list[str]) -> None:
        # Normaliza todas as categorias para facilitar a busca
        self.categorias = [self._normalizar(cat) for cat in categorias]

    def _normalizar(self, texto: str) -> str:
        # Remove acentos e converte para minúsculas
        texto_norm = unicodedata.normalize("NFKD", texto)
        texto_norm = texto_norm.encode("ASCII", "ignore").decode("ASCII")
        return texto_norm.lower()

    def buscar_categoria(self, nome_fornecedor: str) -> List[str]:
        """
        Retorna uma lista de categorias que aparecem no nome do fornecedor.
        """
        nome_normalizado = self._normalizar(nome_fornecedor)
        categorias_encontradas = [
            cat for cat in self.categorias if cat in nome_normalizado
        ]
        return categorias_encontradas

