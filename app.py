# ============================
#        ESTILO GLOBAL
# ============================

st.markdown("""
<style>

    /* ======= FUENTES ======= */
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif !important;
    }

    /* ======= FONDO GENERAL ======= */
    body {
        background-color: #5947fd !important;
        color: white !important;
    }

    .main {
        background-color: #5947fd !important;
        color: white !important;
    }

    /* ======= TÍTULOS ======= */
    .title {
        color: white !important;
        font-size: 34px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 20px;
    }

    .step-title {
        color: white !important;
        font-size: 28px !important;
        font-weight: 800 !important;
        margin-top: 20px !important;
        margin-bottom: 10px !important;
    }

    .sub {
        color: white !important;
        font-size: 22px !important;
        font-weight: 700 !important;
    }

    label, .stRadio label, .stCheckbox label {
        color: white !important;
        font-size: 20px !important;
        font-weight: 700 !important;
    }

    /* ======= BOTONES ======= */
    .stButton>button {
        background-color: #1d1e1c !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        border: 2px solid white !important;
    }

    .stButton>button:hover {
        background-color: white !important;
        color: #1d1e1c !important;
        border: 2px solid #1d1e1c !important;
    }

    /* ======= INPUTS ======= */
    .stTextInput input, .stNumberInput input, textarea {
        background-color: #1d1e1c !important;
        color: white !important;
        border-radius: 8px !important;
        border: 2px solid white !important;
    }

    /* ======= CHECKBOX Y RADIO ESTILIZADOS ======= */
    /* Ocultamos el input original */
    input[type="checkbox"], input[type="radio"] {
        position: absolute;
        opacity: 0;
    }

    /* Estilo general del contenedor */
    .stCheckbox, .stRadio {
        padding: 6px 0px;
    }

    /* Cuadrado blanco */
    .stCheckbox label::before, .stRadio label::before {
        content: "";
        display: inline-block;
        width: 20px;
        height: 20px;
        margin-right: 10px;
        border: 2px solid white;
        background-color: white;
        border-radius: 4px;
        vertical-align: middle;
    }

    /* Check azul cuando está seleccionado */
    input[type="checkbox"]:checked + label::before,
    input[type="radio"]:checked + label::before {
        background-color: #5947fd !important;
        border: 2px solid white !important;
        background-image: url("data:image/svg+xml;utf8,<svg fill='white' viewBox='0 0 16 16' xmlns='http://www.w3.org/2000/svg'><path d='M12.97 4.97a.75.75 0 0 0-1.06-1.06L6.5 9.31 4.09 6.91a.75.75 0 1 0-1.06 1.06l3 3a.75.75 0 0 0 1.06 0l6-6z'/></svg>");
        background-repeat: no-repeat;
        background-position: center;
    }

    /* ======= LOGO EN CABECERA ======= */
    .header-logo {
        width: 180px;
        margin-left: auto;
        margin-right: auto;
        display: block;
        margin-bottom: 20px;
    }

</style>
""", unsafe_allow_html=True)


# ======= LOGO SUPERIOR (APARECE EN TODAS LAS PÁGINAS) =======
st.image("https://raw.githubusercontent.com/redu92/Biotech-/main/logo%20biotech.jpg",
         use_container_width=False,
         width=180)
