TUTORIAL: CRIAR E CENTRALIZAR A BIBLIOTECA E COMANDO CLI (json_process_dgp)
===============================================================================
## 📋 Sumário
1. [ESTRUTURA DA PASTA DO PROJETO LOCAL](#1-ESTRUTURA-DA-PASTA-DO-PROJETO-LOCAL)
2. [PUBLICAR NO GITHUB](#2-PUBLICAR-NO-GITHUB)
3. [INSTALAR E ATUALIZAÇÕES](#3-INSTALAR-E-ATUALIZAÇÕES)
4. [COMO USAR NOS SEUS PROJETOS](#4-COMO-USAR-NOS-SEUS-PROJETOS)
5. [EXEMPLOS DE CÓDIGO DE COMO UTILIZAR](#5-EXEMPLOS-DE-CÓDIGO-DE-COMO-UTILIZAR)

---------------------------------------------------------
## 1. ESTRUTURA DA PASTA DO PROJETO LOCAL
---------------------------------------------------------
Crie uma pasta com o nome json_process_dgp e coloque os dois arquivos dentro dela:
```
json_process_dgp/
    ├── json_process_dgp.py
    ├── pyproject.toml
    ├── README.md
    ├── LICENSE (Opcional)
    ├── .gitignore
    ├── .editorconfig
    ├── requirements-dev.txt
    └── CHANGELOG.md
```
---------------------------------------------------------
## 2. PUBLICAR NO GITHUB
---------------------------------------------------------
Repositório público ou privado no GitHub com o nome json_process_dgp.

URL do repositório: https://github.com/davigopi/json_process_dgp

---------------------------------------------------------
## 3. INSTALAR E ATUALIZAÇÕES
---------------------------------------------------------

Abra o terminal do seu computador, ative o ambiente virtual e, no diretório do repositório json_process_dgp, execute

### A) INSTALAR A FERRAMENTA NO COMPUTADOR
```bash
pip install git+https://github.com/davigopi/json_process_dgp.git
```

### B) ATUALIZAR A FERRAMENTA NO FUTURO

Alterado a version em pyproject.toml:
```bash
pip install --upgrade git+https://github.com/davigopi/json_process_dgp.git
```
Força a atualização:
```bash
pip install --force-reinstall git+https://github.com/davigopi/json_process_dgp.git
```
```bash
pip install --upgrade --no-cache-dir git+https://github.com/davigopi/json_process_dgp.git
```

### C) INSTALAR REQUIREMENTS

```bash
pip install -r venv\Lib\site-packages\json_process_dgp\requirements.txt
```
---------------------------------------------------------
## 4. COMO USAR NOS SEUS PROJETOS
---------------------------------------------------------
- Via importação dentro de scripts Python futuros:
```python
from json_process_dgp import Json_Process_Dgp
```
```python
import json_process_dgp
```
- Via terminal (em qualquer pasta de projeto React Native, Python, etc.):
  Basta abrir o terminal na pasta desejada e digitar:
```bash
python -m json_process_dgp
```
---------------------------------------------------------
## 5. EXEMPLOS DE CÓDIGO DE COMO UTILIZAR
---------------------------------------------------------

### A) Exemplo Básico (Inicialização e Verificação Simples)
```python
import json
from json_process_dgp import Json_Process_Dgp

# Instancia o json_process
json_process = Json_Process_Dgp()

# Payload simples contendo strings de valores numéricos, percentuais e datas
json_exemplo = [
    {
        "id": 1,
        "data_cadastro": "25/08/2026",
        "taxa_desconto": "15,5%",
        "valor_total": "1.250,50"
    }
]

# Processa a lista e converte os tipos
dados_normalizados = json_process.process_to_list(json_exemplo)
print(dados_normalizados)
```

### B) Exemplo Avançado (Estruturas Aninhadas, DataFrame e Exceções)
```python
import json
import pandas as pd
from json_process_dgp import Json_Process_Dgp

json_process = Json_Process_Dgp()

# Payload complexo com aninhamento e valores nulos
payload_complexo = [
    {
        "cliente": "Empresa ABC",
        "data_emissao": "2026-08-25 14:30:00",
        "financeiro": {
            "meta_atingida": "98,7%",
            "faturamento_bruto": "2.450.000,75",
            "observacoes": None
        },
        "historico_datas": ["01/01/2026", "15/06/2026"]
    }
]

try:
    # 1. Processa e normaliza recursivamente dicionários e listas aninhadas
    dados_processados = json_process.process_to_list(payload_complexo)

    # 2. Converte os dados estruturados para um DataFrame do Pandas
    df = json_process.dict_to_dataframe(dados_processados)

    print("--- Dados Normalizados ---")
    print(json.dumps(dados_processados, indent=4, default=str))

    print("\n--- DataFrame Resultante ---")
    print(df)

except ValueError as err:
    print(f"Erro na validação do payload: {err}")
except Exception as err:
    print(f"Erro inesperado durante o processamento: {err}")
```

### C) Exemplo de Execução CLI / Teste Integrado
```bash
# 1. Instale as dependências necessárias
pip install pandas

# 2. Execute o script de teste do json_process via terminal
python -c "
from json_process_dgp import Json_Process_Dgp
p = Json_Process_Dgp()
res = p.process_to_dict({'data_criacao': '25/08/2026', 'valor': '100,50'})
print(res)
"
```
---------------------------------------------------------
