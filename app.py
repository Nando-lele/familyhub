import streamlit as st
import sqlite3
from datetime import datetime

# --- BANCO DE DADOS LOCAL ---
conn = sqlite3.connect('tarefas_casa.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS historico_gamer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT,
        tarefa TEXT,
        status TEXT,
        foto BLOB,
        observacao TEXT,
        UNIQUE(data, tarefa) ON CONFLICT REPLACE
    )
''')
conn.commit()

# --- DESIGN SCI-FI NEON (CYBERPUNK) ---
st.set_page_config(page_title="FamilyHub OS", page_icon="🛸", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top, #0c1020 0%, #04060f 100%) !important;
        color: #E2E8F0 !important;
    }
    .cyber-title {
        font-size: 2.2rem;
        font-weight: 900;
        text-align: center;
        color: #00f2fe;
        text-shadow: 0 0 15px rgba(0, 242, 254, 0.6);
        margin-bottom: 5px;
    }
    .cyber-subtitle {
        text-align: center;
        color: #64748B;
        font-size: 1rem;
        margin-bottom: 25px;
    }
    .mission-card {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(0, 242, 254, 0.2);
        border-left: 6px solid #00f2fe !important;
        border-radius: 12px;
        padding: 20px;
        margin-top: 15px;
        margin-bottom: 5px;
        box-shadow: 0px 4px 20px rgba(0, 242, 254, 0.05);
    }
    .mission-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #FFFFFF !important;
    }
    label, p, div, span {
        color: #94A3B8 !important;
    }
    
    /* NOVO MODELO DE BOTÃO: ESTILO DIGITAL SCI-FI COM BORDAS DE NEON ACESAS */
    .stButton > button {
        font-weight: 800 !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        border-radius: 6px !important;
        padding: 14px 20px !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        background: transparent !important;
    }
    
    /* Botão de Enviar (Neon Azul) */
    .btn-blue button {
        border: 2px solid #00f2fe !important;
        color: #00f2fe !important;
        box-shadow: inset 0 0 8px rgba(0, 242, 254, 0.2), 0 0 10px rgba(0, 242, 254, 0.2) !important;
    }
    .btn-blue button:hover {
        background: #00f2fe !important;
        color: #04060f !important;
        box-shadow: 0 0 20px #00f2fe !important;
    }
    
    /* Botão OK (Neon Verde) */
    .btn-green button {
        border: 2px solid #10B981 !important;
        color: #10B981 !important;
        box-shadow: inset 0 0 8px rgba(16, 185, 129, 0.2), 0 0 10px rgba(16, 185, 129, 0.2) !important;
    }
    .btn-green button:hover {
        background: #10B981 !important;
        color: #04060f !important;
        box-shadow: 0 0 20px #10B981 !important;
    }
    
    /* Botão NOK (Neon Vermelho) */
    .btn-red button {
        border: 2px solid #EF4444 !important;
        color: #EF4444 !important;
        box-shadow: inset 0 0 8px rgba(239, 68, 68, 0.2), 0 0 10px rgba(239, 68, 68, 0.2) !important;
    }
    .btn-red button:hover {
        background: #EF4444 !important;
        color: #04060f !important;
        box-shadow: 0 0 20px #EF4444 !important;
    }
    
    section[data-testid="stSidebar"] { background-color: #070B14 !important; }
    </style>
""", unsafe_allow_html=True)

# --- CONTROLE DE ACESSO ---
st.sidebar.markdown("### 🔐 ACCESS CONTROL")
perfil = st.sidebar.radio("Selecione o Terminal Ativo:", ["Painel do Filho (Operador)", "Painel dos Pais (Comandante)"])

tarefas_diarias = [
    "Limpar a área que a cachorra faz cocô e xixi 🐶",
    "Limpar a areia da bandeja da gata 🐱",
    "Encher as garrafas de água 💧",
    "Arrumar a cama 🛏️",
    "Abrir a janela do quarto 🪟"
]

data_hoje = datetime.now().strftime("%Y-%m-%d")

# Carregar status do dia
cursor.execute("SELECT tarefa, status, foto, observacao FROM historico_gamer WHERE data = ?", (data_hoje,))
dados_hoje = {}
for r in cursor.fetchall():
    dados_hoje[r[0]] = {"status": r[1], "foto": r[2], "obs": r[3]}

tarefas_aprovadas = [t for t, d in dados_hoje.items() if d["status"] == "Aprovado"]

# --- TELA: FILHO ---
if perfil == "Painel do Filho (Operador)":
    st.markdown("<div class='cyber-title'>🛸 PROTOCOLO GAMER</div>", unsafe_allow_html=True)
    st.markdown("<div class='cyber-subtitle'>Complete as missões para liberar o videogame</div>", unsafe_allow_html=True)
    
    progresso = len(tarefas_aprovadas) / len(tarefas_diarias)
    st.progress(progresso)
    
    if len(tarefas_aprovadas) == len(tarefas_diarias):
        st.balloons()
        st.success("🔓 PROTOCOLO CONCLUÍDO! Videogame 100% Liberado.")
    else:
        st.warning("🔒 SISTEMA BLOQUEADO. Conclua as etapas e aguarde a validação.")

    for idx, tarefa in enumerate(tarefas_diarias):
        info = dados_hoje.get(tarefa, {"status": "Pendente", "foto": None, "obs": ""})
        
        st.markdown(f"<div class='mission-card'><div class='mission-title'>🎯 MISSÃO {idx+1}: {tarefa}</div></div>", unsafe_allow_html=True)
        
        if info["status"] == "Aprovado":
            st.markdown("<span style='color:#10B981; font-weight:bold;'>🟢 MISSÃO CONCLUÍDA E APROVADA!</span>", unsafe_allow_html=True)
        elif info["status"] == "Aguardando Validação":
            st.markdown("<span style='color:#3B82F6; font-weight:bold;'>⏳ AGUARDANDO REVISÃO DOS PAIS...</span>", unsafe_allow_html=True)
        else:
            if info["status"] == "Recusado":
                st.markdown("<span style='color:#EF4444; font-weight:bold;'>⚠️ REJEITADA! Refaça o trabalho e envie novamente.</span>", unsafe_allow_html=True)
            
            tipo = st.radio("Método de registro:", ["Câmera 📸", "Galeria 📂"], key=f"t_{idx}")
            foto_bytes = None
            
            if tipo == "Câmera 📸":
                foto = st.camera_input("Capturar", key=f"c_{idx}")
                if foto:
                    foto_bytes = foto.getvalue()
            else:
                arquivo = st.file_uploader("Upload", type=["jpg", "png", "jpeg"], key=f"f_{idx}")
                if arquivo:
                    foto_bytes = arquivo.read()
            
            obs = st.text_input("Observação da missão:", placeholder="Escreva um recado se necessário...", key=f"o_{idx}")
            
            st.markdown("<div class='btn-blue'>", unsafe_allow_html=True)
            if st.button("Transmitir Evidência 🚀", key=f"b_{idx}"):
                if foto_bytes:
                    cursor.execute(
                        "INSERT INTO historico_gamer (data, tarefa, status, foto, observacao) VALUES (?, ?, ?, ?, ?)",
                        (data_hoje, tarefa, "Aguardando Validação", foto_bytes, obs)
                    )
                    conn.commit()
                    st.rerun()
                else:
                    st.error("Adicione uma foto antes de enviar.")
            st.markdown("</div>", unsafe_allow_html=True)

# --- TELA: PAIS ---
else:
    st.markdown("<div class='cyber-title'>⚡ CENTRO DE COMANDO</div>", unsafe_allow_html=True)
    st.markdown("<div class='cyber-subtitle'>Módulo de Auditoria e Aprovação dos Pais</div>", unsafe_allow_html=True)
    
    pendentes = [t for t, d in dados_hoje.items() if d["status"] == "Aguardando Validação"]
    if not pendentes:
        st.info("🛰️ Status: Nenhuma tarefa aguardando avaliação no momento.")
        
    for idx, tarefa in enumerate(tarefas_diarias):
        info = dados_hoje.get(tarefa, {"status": "Pendente", "foto": None, "obs": ""})
        
        if info["status"] == "Aguardando Validação":
            st.markdown(f"<div class='mission-card'><div class='mission-title'>📋 REVISAR: {tarefa}</div></div>", unsafe_allow_html=True)
            if info["obs"]:
                st.write(f"💬 **Nota do filho:** \"{info['obs']}\"")
            st.image(info["foto"], width=300)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("<div class='btn-green'>", unsafe_allow_html=True)
                if st.button("🟢 CONCEDER OK", key=f"ok_{idx}"):
                    cursor.execute("UPDATE historico_gamer SET status = 'Aprovado' WHERE data = ? AND tarefa = ?", (data_hoje, tarefa))
                    conn.commit()
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            with col2:
                st.markdown("<div class='btn-red'>", unsafe_allow_html=True)
                if st.button("🔴 MARCAR NOK", key=f"nok_{idx}"):
                    cursor.execute("UPDATE historico_gamer SET status = 'Recusado' WHERE data = ? AND tarefa = ?", (data_hoje, tarefa))
                    conn.commit()
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
        elif info["status"] == "Aprovado":
            st.markdown(f"🔹 **{tarefa}** -> <span style='color:#10B981; font-weight:bold;'>Aprovado!</span>", unsafe_allow_html=True)
