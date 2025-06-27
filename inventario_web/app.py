from flask import Flask, render_template, request, redirect, session, url_for
import json
import socket
import struct
import os
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "chave-secreta-top"  # Usado para manter a sessão segura
app.permanent_session_lifetime = timedelta(minutes=10)

@app.before_request
def make_session_permanent():
    session.permanent = True

# Função para converter IP em inteiro (para ordenar corretamente)
def ip_para_inteiro(ip):
    try:
        return struct.unpack("!I", socket.inet_aton(ip))[0]
    except:
        return 0

# Função para determinar a unidade baseada no IP
def identificar_unidade(ip):
    if ip.startswith("10.1.0."):
        return "Arouche"
    elif ip.startswith("10.2.0."):
        return "Hospital Santa Cecilia"
    elif ip.startswith("10.3.0."):
        return "Almoxarifado"
    elif ip.startswith("10.4.0."):
        return "Ressonancia"
    elif ip.startswith("10.5.0."):
        return "Heliopolis"
    elif ip.startswith("10.6.0."):
        return "Franco da Rocha"
    return "Outros"

# Rota de login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]
        if usuario == "admin" and senha == "ti!#0529*":
            session["logado"] = True
            return redirect(url_for("index"))
        else:
            return render_template("login.html", erro="Usuário ou senha incorretos")
    return render_template("login.html")

# Rota principal com proteção
@app.route("/")
def index():
    if not session.get("logado"):
        return redirect(url_for("login"))

    try:
        with open('inventario_geral.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except FileNotFoundError:
        dados = []

    # Corrige e padroniza os dados
    for item in dados:
        # Corrige andar sem "º"
        if "andar" in item and item["andar"] and "º" not in item["andar"]:
            item["andar"] = item["andar"].strip() + "º"

        # Padroniza primeira letra maiúscula nos campos
        for campo in ["predio", "setor"]:
            if campo in item and isinstance(item[campo], str):
                item[campo] = item[campo].strip().capitalize()

        # Corrige unidade mal escrita
        predio = item.get("predio", "").lower()
        if predio == "hospital":
            item["predio"] = "Hospital Santa Cecilia"
        elif predio == "franco":
            item["predio"] = "Franco da Rocha"

    # Organiza por unidade
    unidades = {
        "Arouche": [],
        "Hospital Santa Cecilia": [],
        "Almoxarifado": [],
        "Ressonancia": [],
        "Heliopolis": [],
        "Franco da Rocha": [],
        "Outros": []
    }

    for item in dados:
        ip = item.get("ip", "0.0.0.0")
        unidade = identificar_unidade(ip)
        unidades[unidade].append(item)

    # Ordena IPs dentro de cada unidade
    for unidade, lista in unidades.items():
        unidades[unidade] = sorted(lista, key=lambda d: ip_para_inteiro(d.get("ip", "0.0.0.0")))

    return render_template("index.html", unidades=unidades)

# Rota de detalhes
@app.route('/pc/<hostname>')
def detalhe(hostname):
    with open('inventario_geral.json', 'r', encoding='utf-8') as f:
        dados = json.load(f)

    for item in dados:
        if item["hostname"] == hostname:
            item["softwares"] = sorted(item.get("softwares", []), key=lambda s: s["nome"].lower())
            return render_template('detalhe.html', pc=item)
    return f"PC com hostname {hostname} não encontrado", 404

# NOVA ROTA: atualizar patrimonio
@app.route("/atualizar_patrimonio/<hostname>", methods=["POST"])
def atualizar_patrimonio(hostname):
    novo_patrimonio = request.form.get("novo_patrimonio", "").strip()

    with open("inventario_geral.json", "r", encoding="utf-8") as f:
        dados = json.load(f)

    atualizado = False
    for item in dados:
        if item.get("hostname") == hostname:
            item["patrimonio"] = novo_patrimonio
            atualizado = True
            break

    if atualizado:
        with open("inventario_geral.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    return redirect(url_for("detalhe", hostname=hostname))

# Rota de logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
