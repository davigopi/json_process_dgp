# flake8: noqa
# pyright: # type: ignore

import json
from datetime import datetime
from typing import Any, Union
import pandas as pd


class Json_Process_Dgp:
    def dict_to_dataframe(self, arq_dict: Union[dict, list]) -> pd.DataFrame:
        if not arq_dict:
            return pd.DataFrame()
        if isinstance(arq_dict, dict):
            arq_dict = [arq_dict]
        return pd.DataFrame(arq_dict)

    # ==========================================
    # CONVERSORES
    # ==========================================
    def _convert_date(self, value: str) -> datetime | None:
        value = value.strip()
        formatos = [
            "%d/%m/%Y",
            "%d/%m/%y",
            "%Y-%m-%d",
            "%Y-%m-%d %H:%M:%S",
            "%d/%m/%Y %H:%M:%S",
        ]
        for formato  in formatos:
            try:
                value = value.strip()
                value_date = datetime.strptime(value, formato)
                return value_date.strftime("%d/%m/%Y")
            except ValueError:
                pass
        return value

    def _convert_number(self, value: Union[str]) -> Union[float, None]:
        val_str = str(value).strip().replace("\xa0", "")
        if not val_str:
            return value
        # Preserva o sinal negativo se existir no início
        is_negative = val_str.startswith("-")
        # Remove qualquer caractere que não seja dígito, vírgula ou ponto
        clean_str = "".join(c for c in val_str if c.isdigit() or c in ",.")
        if not clean_str:
            return value
        # Descobre os índices do último ponto e da última vírgula
        last_dot = clean_str.rfind(".")
        last_comma = clean_str.rfind(",")
        if last_comma > last_dot:
            # Formato Brasileiro (ex: "1.000,50" ou "1000,50")
            # O ponto é milhar (remove) e a vírgula é decimal (vira ponto)
            clean_str = clean_str.replace(".", "").replace(",", ".")
        elif last_dot > last_comma:
            # Formato Americano (ex: "1,000.50" ou "1000.50")
            # A vírgula é milhar (remove)
            clean_str = clean_str.replace(",", "")
        try:
            num = int(clean_str)
            return -num if is_negative else num
        except ValueError:
            try:
                num = float(clean_str)
                return -num if is_negative else num
            except ValueError:
                return value

    def _convert_percentage(self, value: str) -> Union[float, None]:
        value = value.replace("%", "").strip()
        if "," in value:
            value = value.replace(".", "").replace(",", ".")
        try:
            return float(value)
        except ValueError:
            return value

    # ==========================================
    # DETECTORES
    # ==========================================
    def _eh_date(self, value: Any) -> bool:
        if not isinstance(value, str):
            return False
        try:
            datetime.fromisoformat(value)
            return True
        except ValueError:
            return False

    def _eh_percentage(self, value):
        return isinstance(value, str) and "%" in value

    def _eh_numbre(self, value):
        if isinstance(value, str):
            value_clean = value.strip().replace(" ", "").replace("-", "").replace(".", "").replace(",", ".")
            return value_clean.isdigit()
        return False

    # ==========================================
    # FUNCT
    # ==========================================
    def _normalize_value(self, value: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, (dict, list)):
            return self._normalize_arq(value)
        if self._eh_date(value):
            return self._convert_date(value)
        if self._eh_percentage(value):
            return self._convert_percentage(value)
        if self._eh_numbre(value):
            return self._convert_number(value)
        return value

    # ==========================================
    # START
    # ==========================================
    def _normalize_arq(self, value: Any) -> Any:
        if isinstance(value, dict):
            dict_ney = {}
            for key, value in value.items():
                value = self._normalize_value(value=value)
                dict_ney[key] = value
            return dict_ney
        elif isinstance(value, list):
            return [self._normalize_value(value=valu) for valu in value]
        return self._normalize_value(value)


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
    print("value da taxa convertida (float):", resultado_dict["taxa_comissao"])
    print("value da venda convertido (float):", resultado_dict["valor_venda"])

    # 3. Teste de Conversão para DataFrame
    df = json_process.dict_to_dataframe(resultado_lista)
    print("\n[3] DataFrame final:")
    print(df.to_string())
    print("\nTipos de colunas no DataFrame:")
    print(df.dtypes)
