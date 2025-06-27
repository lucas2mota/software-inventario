# 🖥️ Sistema de Inventário de Equipamentos

Este é um sistema de inventário de computadores e softwares desenvolvido em Python com interface Tkinter e visualização web com Flask.

## 📦 Funcionalidades

- Coleta automática de informações da máquina (modelo, memória, processador, IP, hostname, etc).
- Listagem de softwares instalados via registro do Windows.
- Exportação em Excel e JSON.
- Upload dos dados para pasta compartilhada em rede.
- Interface web com autenticação (login/senha).
- Visualização dos dados por unidade (ex: Arouche, Hospital, Ressonância...).
- Detalhamento individual por PC.
- Edição rápida do campo "Patrimônio" direto no navegador.
- Organização por IP e unidade.
- Sessão com timeout automático (10 min).
- Integração com GitHub.

## 🛠️ Tecnologias

- Python 3
- Tkinter
- Flask
- WMI
- psutil
- openpyxl
- HTML/CSS (Jinja2 templates)

## 🧪 Como executar

### 📋 Requisitos

- Python 3 instalado
- Windows
- Acesso à rede interna (ex: `\\10.1.0.41\Compartilhada\JSONS`)

### 🎮 Modo local (coleta do inventário)

1. Execute `script_inventario.py` para abrir a interface Tkinter.
2. Preencha as informações e clique em "Gerar Inventário".
3. O arquivo será salvo na pasta da rede ou localmente (caso a rede não esteja acessível).

### 🌐 Modo Web (visualização)

1. Execute `app.py`
2. Acesse no navegador: [http://localhost:5000](http://localhost:5000) ou pelo IP da VM.
3. Login: `admin` — Senha: `ti!#0529*`

## 🧠 Estrutura do Projeto
inventario/
├── app.py
├── script_inventario.py
├── mesclar_jsons.py
├── templates/
│ ├── index.html
│ ├── login.html
│ └── detalhe.html
├── inventario_geral.json
└── .gitignore


## 👨‍💻 Autor

- **Lucas Mota**  
- Contato: [https://www.linkedin.com/in/lucas2mota/]

---

🚀 Projeto em constante evolução. Ideias são bem-vindas!
