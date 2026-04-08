import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import unicodedata
from pathlib import Path

st.set_page_config(
    page_title="Consulta de Email",
    page_icon="📧",
    layout="centered"
)

def normalizar_texto(texto):
    if pd.isna(texto):
        return ""
    texto = str(texto).strip().lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto

def encontrar_coluna(df, nomes_possiveis):
    colunas_norm = {normalizar_texto(col): col for col in df.columns}
    for nome in nomes_possiveis:
        nome_norm = normalizar_texto(nome)
        if nome_norm in colunas_norm:
            return colunas_norm[nome_norm]
    return None

@st.cache_data
def carregar_dados(caminho_arquivo):
    df = pd.read_excel(caminho_arquivo)

    col_nome = encontrar_coluna(df, ["nome", "nome completo"])
    col_email = encontrar_coluna(df, ["email", "e-mail"])
    col_status = encontrar_coluna(df, ["status"])

    if not col_nome or not col_email or not col_status:
        raise ValueError("A planilha precisa ter colunas equivalentes a nome, email e status.")

    df = df[[col_nome, col_email, col_status]].copy()
    df.columns = ["nome", "email", "status"]
    df["nome_normalizado"] = df["nome"].apply(normalizar_texto)
    df["status"] = df["status"].astype(str).str.strip().str.upper()
    return df

def gerar_link_whatsapp(numero):
    numero_limpo = "".join(filter(str.isdigit, numero))
    return f"https://wa.me/{numero_limpo}"

ARQUIVO_DADOS = "dados.xlsx"
LOGO = None
NUMERO_WHATSAPP = "+55 91 98559-5528"
LINK_WHATSAPP = gerar_link_whatsapp(NUMERO_WHATSAPP)

st.markdown("""
<style>
    .stApp {
        background: #f5f7fb;
    }

    .block-container {
        padding-top: 3.5rem;
        padding-bottom: 2rem;
        max-width: 760px;
    }

    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1rem;
        margin-top: 0.4rem;
        margin-bottom: 2rem;
    }

    .result-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        padding: 20px;
        margin-top: 18px;
    }

    .info-row {
        font-size: 1rem;
        color: #0f172a;
        margin-bottom: 14px;
    }

    .info-label {
        font-weight: 700;
        color: #0f172a;
    }

    .status-badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 999px;
        font-size: 0.88rem;
        font-weight: 700;
    }

    .ativo {
        background: #dcfce7;
        color: #166534;
        border: 1px solid #bbf7d0;
    }

    .desativado {
        background: #fee2e2;
        color: #991b1b;
        border: 1px solid #fecaca;
    }

    .help-box {
        background: #f8fafc;
        border: 1px dashed #cbd5e1;
        border-radius: 18px;
        padding: 20px;
        margin-top: 24px;
        text-align: center;
    }

    .help-title {
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 6px;
    }

    .help-text {
        color: #64748b;
        font-size: 0.95rem;
    }

    div[data-testid="stTextInput"] label {
        color: #334155 !important;
        font-weight: 600 !important;
    }

    div[data-testid="stTextInput"] input {
        background: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #dbe4ee !important;
        border-radius: 14px !important;
        padding: 0.85rem 1rem !important;
        box-shadow: none !important;
    }

    div[data-testid="stTextInput"] input:focus {
        border: 1px solid #94a3b8 !important;
        box-shadow: 0 0 0 1px #cbd5e1 !important;
    }

    div[data-testid="stLinkButton"] a {
        background: #0f172a !important;
        color: white !important;
        border-radius: 14px !important;
        text-align: center !important;
        font-weight: 600 !important;
        border: none !important;
    }

    @media (max-width: 640px) {
        .subtitle {
            font-size: 0.95rem;
            margin-bottom: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

def mostrar_logo():
    caminho_logo = None

    if LOGO and Path(LOGO).exists():
        caminho_logo = LOGO
    else:
        for nome in ["logo.png", "logo.jpg", "logo.jpeg", "logo.webp"]:
            if Path(nome).exists():
                caminho_logo = nome
                break

    if caminho_logo:
        st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(caminho_logo, width=340)

        st.markdown("<div style='margin-bottom:10px'></div>", unsafe_allow_html=True)

mostrar_logo()

st.markdown(
    """
    <div class="subtitle">
        Digite seu nome para localizar seu email institucional
    </div>
    """,
    unsafe_allow_html=True
)

try:
    df = carregar_dados(ARQUIVO_DADOS)
except FileNotFoundError:
    st.error("Arquivo 'dados.xlsx' não encontrado na pasta do projeto.")
    st.stop()
except Exception as e:
    st.error(f"Erro ao carregar a planilha: {e}")
    st.stop()

busca = st.text_input(
    "Digite o nome",
    placeholder="Ex.: Maria, João Silva, Ana Souza..."
)

if busca:
    busca_norm = normalizar_texto(busca)
    resultados = df[df["nome_normalizado"].str.contains(busca_norm, na=False)].copy()

    if len(resultados) == 0:
        st.markdown("""
        <div style="
            background:#fee2e2;
            border:1px solid #fecaca;
            color:#000000;
            padding:14px 16px;
            border-radius:12px;
            font-weight:500;
            margin-top:10px;
        ">
            Nenhum resultado encontrado. Tente digitar outra parte do nome.
        </div>
        """, unsafe_allow_html=True)
    else:
        resultados = resultados.sort_values("nome")
        registro = resultados.iloc[0]

        status = registro["status"]
        classe_status = "ativo" if status == "ATIVO" else "desativado"

        st.markdown('<div class="result-card">', unsafe_allow_html=True)

        st.markdown(
            f'<div class="info-row"><span class="info-label">Nome:</span> {registro["nome"]}</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'''
            <div class="info-row">
                <span class="info-label">Status:</span>
                <span class="status-badge {classe_status}">{status}</span>
            </div>
            ''',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="info-row"><span class="info-label">Email:</span></div>',
            unsafe_allow_html=True
        )

        email_valor = str(registro["email"]).replace("'", "\\'")

        components.html(
            f"""
            <div style="display:flex; gap:12px; align-items:stretch; margin-top:8px; flex-wrap:wrap;">
                <div style="
                    flex:1;
                    min-width:260px;
                    background:#ffffff;
                    border:1px solid #dbe4ee;
                    border-radius:14px;
                    padding:14px 16px;
                    color:#334155;
                    font-size:0.98rem;
                    min-height:50px;
                    display:flex;
                    align-items:center;
                    box-sizing:border-box;
                    overflow-wrap:anywhere;">
                    {email_valor}
                </div>

                <button
                    onclick="
                        navigator.clipboard.writeText('{email_valor}');
                        const btn = document.getElementById('copy-btn');
                        btn.innerText = 'Copiado!';
                        setTimeout(() => btn.innerText = 'Copiar email', 1500);
                    "
                    id="copy-btn"
                    style="
                        background:#2563eb;
                        color:white;
                        border:none;
                        border-radius:14px;
                        padding:0 18px;
                        font-weight:600;
                        cursor:pointer;
                        min-height:50px;
                        min-width:170px;">
                    Copiar email
                </button>
            </div>
            """,
            height=85,
        )

        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="help-box">
    <div class="help-title">Em caso de dúvida</div>
    <div class="help-text">
        Entre em contato com o suporte técnico pelo WhatsApp.
    </div>
</div>
""", unsafe_allow_html=True)

st.link_button("Falar no WhatsApp", LINK_WHATSAPP, use_container_width=True)