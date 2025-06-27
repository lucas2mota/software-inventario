import json
import os

ARQUIVO_MESTRE = "inventario_geral.json"

# Carrega o arquivo mestre (cria vazio se não existir)
if os.path.exists(ARQUIVO_MESTRE):
    with open(ARQUIVO_MESTRE, "r", encoding="utf-8") as f:
        dados_mestre = json.load(f)
else:
    dados_mestre = []

# Lista todos os arquivos .json da pasta (menos o mestre)
for arquivo in os.listdir():
    if arquivo.endswith(".json") and arquivo != ARQUIVO_MESTRE:
        print(f"➡️ Lendo {arquivo}")
        with open(arquivo, "r", encoding="utf-8") as f:
            dados_novos = json.load(f)

        if isinstance(dados_novos, dict):
            dados_novos = [dados_novos]

        hostnames_existentes = [d["hostname"] for d in dados_mestre]

        for d in dados_novos:
            if d["hostname"] not in hostnames_existentes:
                dados_mestre.append(d)

# Salva tudo de volta no mestre
with open(ARQUIVO_MESTRE, "w", encoding="utf-8") as f:
    json.dump(dados_mestre, f, indent=4, ensure_ascii=False)

print("✅ Todos os JSONs foram mesclados com sucesso!")
