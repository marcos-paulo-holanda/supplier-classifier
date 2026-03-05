from typing import List

from sentence_transformers import SentenceTransformer, util

from app.domain.categories_list import categories_list
from app.domain.categories_synonyms import CATEGORY_SYNONYMS


class ClassificadorSemantico:
    """
    Verifica se a atividade principal de uma empresa se parece com alguma categoria.
    """

    def __init__(self, categorias: list[str] | None = None) -> None:
        self.categorias = categorias or categories_list
        self.model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

        synonyms = CATEGORY_SYNONYMS
        self.example_texts: List[str] = []
        self.example_to_category: List[str] = []

        for categoria in self.categorias:
            base_text = categoria.lower()
            self.example_texts.append(base_text)
            self.example_to_category.append(categoria)

            for frase in synonyms.get(categoria, []):
                self.example_texts.append(frase.lower())
                self.example_to_category.append(categoria)

        self.embeddings = self.model.encode(self.example_texts, convert_to_tensor=True)

    def classificar(self, atividade_principal: str) -> str:
        emb_atividade = self.model.encode(
            atividade_principal.lower(), convert_to_tensor=True
        )
        similaridades = util.cos_sim(emb_atividade, self.embeddings)
        indice = similaridades.argmax().item()
        return self.example_to_category[indice]

