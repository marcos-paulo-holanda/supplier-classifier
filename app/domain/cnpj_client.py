from typing import Any, Dict

import requests


class CNPJClient:
    """
    Cliente para consultar informações de empresas na API pública do CNPJws.
    """

    BASE_URL = "https://publica.cnpj.ws/cnpj/"

    def __init__(self, timeout: int = 10) -> None:
        self.timeout = timeout

    def consultar(self, cnpj: str) -> Dict[str, Any]:
        """
        Consulta um CNPJ na API pública.

        Parameters
        ----------
        cnpj:
            Número do CNPJ (pode conter máscara, será sanitizado).

        Returns
        -------
        dict
            Dicionário com os dados retornados pela API.

        Raises
        ------
        ValueError
            Quando o CNPJ não é encontrado.
        RuntimeError
            Quando há muitas requisições em um curto intervalo.
        HTTPError
            Para demais erros HTTP.
        """
        # Sanitiza o CNPJ removendo caracteres não numéricos
        cnpj_sanitizado = "".join(filter(str.isdigit, cnpj))

        url = f"{self.BASE_URL}{cnpj_sanitizado}"
        response = requests.get(url, timeout=self.timeout)

        if response.status_code == 200:
            return response.json()
        if response.status_code == 404:
            raise ValueError("CNPJ não encontrado na base de dados.")
        if response.status_code == 429:
            raise RuntimeError("Muitas requisições. Aguarde antes de tentar novamente.")

        response.raise_for_status()

