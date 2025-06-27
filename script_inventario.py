import socket
import platform
import psutil
import wmi
import openpyxl
from tkinter import *
from tkinter import ttk, messagebox
import datetime
import os
import json
import winreg

# Inicializa o WMI (usado para coletar info de hardware no Windows)
c = wmi.WMI()

CAMINHO_REDE = r"\\10.1.0.41\Compartilhada\JSONS"

# Dicionário com prédios e seus andares
predios_andares = {
    "Arouche": [f"{i}º" for i in range(0, 11)],
    "Hospital Santa Cecilia": [f"{i}º" for i in range(0, 6)],
    "Almoxarifado": ["0º", "1º"],
    "Ressonancia": ["0º", "1º"],
    "Heliopolis": ["0º"],
    "Franco da Rocha": ["0º"]
}

# Função para atualizar os andares ao escolher o prédio
def atualizar_andares(event):
    predio = combo_predio.get()
    combo_andar['values'] = predios_andares.get(predio, [])
    if combo_andar['values']:
        combo_andar.set(combo_andar['values'][0])  # Define o primeiro como padrão

# Função para coletar softwares instalados via registro
def get_installed_software():
    software_list = []
    reg_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]
    for reg_path in reg_paths:
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
            for i in range(winreg.QueryInfoKey(reg_key)[0]):
                try:
                    sub_key_name = winreg.EnumKey(reg_key, i)
                    sub_key = winreg.OpenKey(reg_key, sub_key_name)
                    name, _ = winreg.QueryValueEx(sub_key, "DisplayName")
                    version = winreg.QueryValueEx(sub_key, "DisplayVersion")[0] if "DisplayVersion" in [winreg.EnumValue(sub_key, j)[0] for j in range(winreg.QueryInfoKey(sub_key)[1])] else "Desconhecido"
                    software_list.append({"nome": name, "versao": version})
                except:
                    continue
        except:
            continue
    return software_list

# Função principal para gerar o inventário
def gerar_inventario():
    predio = combo_predio.get().strip().capitalize()
    andar = combo_andar.get()
    setor = entry_setor.get().strip().capitalize()
    patrimonio = entry_patrimonio.get()

    if not all([predio, andar, setor]):
        messagebox.showwarning("Campos obrigatórios", "Preencha Prédio, Andar e Setor!")
        return

    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    memoria_gb = round(psutil.virtual_memory().total / (1024 ** 3))

    try:
        computador = c.Win32_ComputerSystem()[0]
        modelo = computador.Model
        fabricante = computador.Manufacturer
    except:
        modelo = "Desconhecido"
        fabricante = "Desconhecido"

    try:
        processador = c.Win32_Processor()[0].Name.strip()
    except:
        processador = platform.processor()

    nome_arquivo = f"Inventario_local_{hostname}.xlsx"
    existe = os.path.exists(nome_arquivo)

    if existe:
        wb = openpyxl.load_workbook(nome_arquivo)
        ws = wb.active
    else:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Inventário"
        ws.append(["PRÉDIO", "ANDAR", "SETOR", "MODELO", "PATRIMÔNIO", "PROCESSADOR", "MEMÓRIA", "HOSTNAME", "IP", "FABRICANTE"])

    ws.append([predio, andar, setor, modelo, patrimonio, processador, f"{memoria_gb}GB", hostname, ip, fabricante])
    wb.save(nome_arquivo)

    softwares = get_installed_software()

    dados = {
        "data_coleta": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "predio": predio,
        "andar": andar,
        "setor": setor,
        "patrimonio": patrimonio,
        "modelo": modelo,
        "fabricante": fabricante,
        "processador": processador,
        "memoria": f"{memoria_gb}GB",
        "hostname": hostname,
        "ip": ip,
        "softwares": softwares
    }

    ip_formatado = ip.replace(".", "-")
    arquivo_json = f"inventario_{ip_formatado}.json"
    caminho_completo = os.path.join(CAMINHO_REDE, arquivo_json)

    if os.path.exists(caminho_completo):
        with open(caminho_completo, "r", encoding="utf-8") as f:
            inventario_geral = json.load(f)
    else:
        inventario_geral = []

    index_existente = next((index for (index, d) in enumerate(inventario_geral) if d.get("hostname") == hostname), None)

    if index_existente is not None:
        inventario_geral[index_existente] = dados
    else:
        inventario_geral.append(dados)

    with open(caminho_completo, "w", encoding="utf-8") as f:
        json.dump(inventario_geral, f, indent=4, ensure_ascii=False)

    messagebox.showinfo("Sucesso", f"Inventário salvo com sucesso em {arquivo_json}!")
    janela.destroy()

# Interface gráfica
janela = Tk()
janela.title("Coletor de Inventário Local")
janela.geometry("400x400")

Label(janela, text="Prédio:").pack(pady=2)
combo_predio = ttk.Combobox(janela, values=list(predios_andares.keys()), width=37)
combo_predio.pack()
combo_predio.bind("<<ComboboxSelected>>", atualizar_andares)

Label(janela, text="Andar:").pack(pady=2)
combo_andar = ttk.Combobox(janela, width=37)
combo_andar.pack()

Label(janela, text="Setor:").pack(pady=2)
entry_setor = Entry(janela, width=40)
entry_setor.pack()

Label(janela, text="Patrimônio (opcional):").pack(pady=2)
entry_patrimonio = Entry(janela, width=40)
entry_patrimonio.pack()

Button(janela, text="Gerar Inventário", command=gerar_inventario).pack(pady=20)

janela.mainloop()
