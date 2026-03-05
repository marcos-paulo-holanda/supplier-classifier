import unicodedata
from typing import List

from rapidfuzz import fuzz


class AssociadorCategoriaFornecedor:
    """
    Verifica se o nome da categoria se parece com alguma palavra do nome do fornecedor.
    """

    def __init__(self, categorias: list[str], limiar_similaridade: int = 80) -> None:
        self.categorias = categorias
        self.limiar = limiar_similaridade
        self.categorias_normalizadas = [self._normalizar(cat) for cat in categorias]

    def _normalizar(self, texto: str) -> str:
        texto_norm = unicodedata.normalize("NFKD", texto)
        texto_norm = texto_norm.encode("ASCII", "ignore").decode("ASCII")
        return texto_norm.lower()

    def associar(self, nome_fornecedor: str) -> List[str]:
        nome_normalizado = self._normalizar(nome_fornecedor)
        palavras_fornecedor = nome_normalizado.split()

        categorias_encontradas: List[str] = []

        for categoria, categoria_normalizada in zip(
            self.categorias, self.categorias_normalizadas
        ):
            palavras_categoria = categoria_normalizada.split()
            for palavra_cat in palavras_categoria:
                for palavra_forn in palavras_fornecedor:
                    score = fuzz.partial_ratio(palavra_cat, palavra_forn)
                    if score >= self.limiar:
                        categorias_encontradas.append(categoria)
                        break
                else:
                    continue
                break

        return categorias_encontradas

