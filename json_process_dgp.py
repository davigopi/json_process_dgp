# flake8: noqa
# pyright: # type: ignore

import json
from datetime import datetime
from typing import Any, Union
import pandas as pd


class Json_Process_Dgp:
    # ==========================================
    # INTERFACE PÚBLICA DE PROCESSAMENTOY
    # ==========================================
    def process_to_list(self, arq_json: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if not isinstance(arq_json, list):
            raise ValueError("JSON precisa ser uma lista de registros")
        dados = [
            self._normalizar_registro(reg)
            for reg in arq_json
        ]
        return dados

    def process_to_dict(self, arq_json: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(arq_json, dict):
            raise ValueError("JSON precisa ser uma dicionario de registros")
        return self._normalizar_registro(arq_json)

    def dict_to_dataframe(self, arq_dict: Union[dict, list]) -> pd.DataFrame:
        if not arq_dict:
            return pd.DataFrame()
        if isinstance(arq_dict, dict):
            arq_dict = [arq_dict]
        return pd.DataFrame(arq_dict)

    # ==========================================
    # NORMALIZA REGISTRO (RECURSIVO)
    # ==========================================
    def _normalizar_registro(self, registro) -> dict:
        if isinstance(registro, dict):
            novo = {}
            for chave, valor in registro.items():
                novo[chave] = self._normalizar_valor(chave, valor)
            return novo
        elif isinstance(registro, list):
            return [self._normalizar_registro(item) for item in registro]
        return registro


    def _normalizar_valor(self, chave: str, valor: Any) -> Any:
        if valor is None:
            return None

        if isinstance(valor, (dict, list)):
            return self._normalizar_registro(valor)

        if self._eh_data(chave, valor):
            return self._converter_data(valor)

        if self._eh_percentual(valor):
            return self._converter_percentual(valor)

        if self._eh_numero_brasileiro(valor):
            return self._converter_numero(valor)

        return valor
    # ==========================================
    # DETECTORES
    # ==========================================
    def _eh_data(self, chave: str, valor: Any) -> bool:
        if not isinstance(valor, str):
            return False
        return "DATA" in chave.upper()

    def _eh_percentual(self, valor):
        return isinstance(valor, str) and "%" in valor

    def _eh_numero_brasileiro(self, valor):
        if not isinstance(valor, str):
            return False
        texto_limpo = valor.strip().replace(".", "").replace(",", "").replace("-", "").replace(" ", "")
        return "," in valor and texto_limpo.isdigit()

    # ==========================================
    # CONVERSORES
    # ==========================================
    def _converter_data(self, valor: str) -> Union[datetime, None]:
        formatos = [
            "%d/%m/%Y",
            "%d/%m/%y",
            "%Y-%m-%d",
            "%Y-%m-%d %H:%M:%S",
            "%d/%m/%Y %H:%M:%S",
        ]
        for fmt in formatos:
            try:
                valor = valor.strip()
                return datetime.strptime(valor, fmt)
            except ValueError:
                pass
        return None

    def _converter_percentual(self, valor: str) -> Union[float, None]:
        valor = valor.replace("%", "").strip()
        if "," in valor:
            valor = valor.replace(".", "").replace(",", ".")
        try:
            return float(valor)
        except ValueError:
            return None

    def _converter_numero(self, valor: str) -> Union[float, None]:
        valor = valor.strip().replace(" ", "").replace(".", "").replace(",", ".")
        try:
            return float(valor)
        except ValueError:
            return None

if __name__ == '__main__':
    json_process = Json_Process_Dgp()
    # Payload de teste cobrindo datas, percentuais, números PT-BR, nulos e aninhamento
    dados_misto = [
        {
            "id": 1,
            "data_cadastro": "25/08/2026",
            "taxa_comissao": "12,5%",
            "valor_venda": "1.500,75",
            "detalhes": {
                "data_atualizacao": "2026-08-25 14:30:00",
                "desconto": "5%",
                "ativo": True,
                "observacao": None
            }
        },
        {
            "id": 2,
            "data_cadastro": "01/01/2026",
            "taxa_comissao": "10%",
            "valor_venda": "250,00",
            "detalhes": None
        }
    ]

    print("=== Executando Testes ===")

    # 1. Teste de Normalização em Lista
    resultado_lista = json_process.process_to_list(dados_misto)
    print("\n[1] Resultado do process_to_list:")
    print(json.dumps(resultado_lista, indent=4, default=str))

    # 2. Teste de Normalização de Dicionário Único
    resultado_dict = json_process.process_to_dict(dados_misto[0])
    print("\n[2] Tipo da data convertida:", type(resultado_dict["data_cadastro"]))
    print("Valor da taxa convertida (float):", resultado_dict["taxa_comissao"])
    print("Valor da venda convertido (float):", resultado_dict["valor_venda"])

    # 3. Teste de Conversão para DataFrame
    df = json_process.dict_to_dataframe(resultado_lista)
    print("\n[3] DataFrame final:")
    print(df.to_string())
    print("\nTipos de colunas no DataFrame:")
    print(df.dtypes)
