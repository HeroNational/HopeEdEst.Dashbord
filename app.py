import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
import base64
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Rapport RUC - Région de l'Est",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Fonction pour injecter le CSS de manière cachée
def local_css():
    st.markdown("""
    <style>
    /* Importer la police Montserrat depuis Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700;800&display=swap');

    /* Police par défaut et couleur texte légèrement atténuée */
    :root {
        --main-text: #0b1220; /* très sombre mais pas noir pur */
        --muted-text: #475569;
    }
    /* Masquer le CSS affiché */
    .main {
        background-color: #f8f9fa;
    }

    /* En-tête principal */
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 1.2rem 1.4rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        display: flex;
        align-items: center;
        gap: 1rem;
        font-family: 'Montserrat', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
    }

    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        font-family: 'Montserrat', sans-serif;
    }

    .main-header h3 {
        color: #e0e7ff;
        font-weight: 400;
    }

    .main-header img {
        width: 88px;
        height: 88px;
        object-fit: contain;
        border-radius: 8px;
        background: rgba(255,255,255,0.08);
        padding: 6px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    }

    /* Appliquer la police Montserrat et couleur de texte par défaut pour tout le contenu */
    :root {
        --main-text: #0b1220; /* très sombre mais pas noir pur */
        --muted-text: #475569;
        --fs-h1: 28px;
        --fs-h2: 20px;
        --fs-h3: 16px;
        --fs-base: 14px;
        --fw-regular: 400;
        --fw-medium: 600;
        --fw-bold: 700;
        --line-height: 1.45;
    }

    @media (prefers-reduced-motion: reduce) { * { transition: none !important; } }

    /* Forcer Montserrat globalement pour écraser les fonts par défaut (Source Sans...) */
    html, body, .stApp, .main, .block-container, .streamlit-expanderContent, div[data-testid="stAppViewContainer"], section[data-testid="stSidebar"] {
        font-family: 'Montserrat', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial !important;
        color: var(--main-text) !important;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        line-height: var(--line-height);
        font-size: var(--fs-base);
    }

    /* Assurer que les éléments typographiques inline et widgets héritent bien */
    .stButton button, button, label, input, textarea, select {
        font-family: 'Montserrat', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial !important;
    }

    /* Titres et hiérarchie */
    .main-header h1 { font-size: var(--fs-h1); font-weight: var(--fw-bold); line-height:1.05; }
    .main-header h3 { font-size: var(--fs-h3); font-weight: var(--fw-medium); }
    .section-header h2 { font-size: var(--fs-h2); font-weight: var(--fw-medium); }

    /* Texte courant */
    p, span, li, .case-card p { font-size: var(--fs-base); color: var(--main-text); }

    /* Métriques et info boxes */
    .info-box-title { font-size: 12px; letter-spacing: 0.6px; font-weight: var(--fw-medium); color: var(--muted-text); }
    .info-box-value { font-size: 28px; font-weight: var(--fw-bold); color: #1e3a8a; }

    /* Sidebar: labels et radios */
    section[data-testid="stSidebar"] .stRadio > label { font-family: 'Montserrat', sans-serif; font-weight: var(--fw-medium); }

    div[data-testid="stMetricLabel"] {
        color: #64748b;
        font-weight: 500;
        font-size: 13px;
    }

    /* Adapter les textes secondaires */
    .team-name, .info-box-subtitle, .case-card p, .recommendation-box, .recommendation-box-urgent, .team-member {
        color: var(--muted-text);
        font-size: var(--fs-base);
    }

    /* Cartes de statistiques */
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #3b82f6;
        margin-bottom: 1rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }

    /* Sections */
    .section-header {
        background: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 2rem 0 1rem 0;
        border-left: 4px solid #3b82f6;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    .section-header h2 {
        color: #1e3a8a;
        margin: 0;
        font-size: 1.8rem;
    }

    /* Métriques personnalisées */
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #1e3a8a;
    }

    div[data-testid="stMetricLabel"] {
        color: #64748b;
        font-weight: 500;
    }

    /* Adapter les textes secondaires */
    .team-name, .info-box-subtitle, .case-card p, .recommendation-box, .recommendation-box-urgent, .team-member {
        color: var(--muted-text);
    }

    /* Cartes d'expansion */
    .streamlit-expanderHeader {
        background-color: white;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .streamlit-expanderHeader:hover {
        border-color: #3b82f6;
        background-color: #f0f9ff;
    }

    /* Zone de recommandations */
    .recommendation-box {
        background: #f0f9ff;
        border-left: 4px solid #0284c7;
        padding: 1rem;
        border-radius: 4px;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }

    .recommendation-box:hover {
        transform: translateX(10px);
        box-shadow: 0 2px 8px rgba(2, 132, 199, 0.2);
    }

    .recommendation-box-urgent {
        background: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 4px;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }

    .recommendation-box-urgent:hover {
        transform: translateX(10px);
        box-shadow: 0 2px 8px rgba(245, 158, 11, 0.2);
    }

    /* Footer */
    .footer {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-top: 3rem;
    }

    /* Style de l'équipe */
    .team-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 8px;
    }

    .team-member {
        display: inline-block;
        background: white;
        padding: 6px 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        color: #334155;
        font-size: 13px;
        border-left: 3px solid #3b82f6;
        transition: transform 0.2s;
    }

    .team-member:hover {
        transform: translateY(-2px);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
        border-right: 1px solid #cbd5e1;
    }

    section[data-testid="stSidebar"] > div {
        background: transparent;
    }

    /* Style du sélecteur de langue */
    section[data-testid="stSidebar"] .stRadio > label {
        color: #1e3a8a !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        margin-bottom: 1rem;
    }

    section[data-testid="stSidebar"] .stRadio label {
        color: #334155 !important;
        font-weight: 500 !important;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label {
        background: white;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        border-color: #3b82f6;
        background: #f0f9ff;
        transform: translateX(5px);
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] {
        background: #3b82f6;
        color: white !important;
        border-color: #3b82f6;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] span {
        color: white !important;
    }

    /* Conteneurs de cas remarquables */
    .case-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        border-top: 3px solid #3b82f6;
        transition: all 0.3s ease;
    }

    .case-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }

    .case-card h3 {
        color: #1e3a8a;
        margin-top: 0;
        margin-bottom: 1rem;
    }

    .case-card p {
        margin: 0.5rem 0;
        line-height: 1.6;
        color: #475569;
    }

    /* Cartes statistiques stylisées */
    .info-box {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        border-left: 4px solid #3b82f6;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }

    .info-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
    }

    .info-box-title {
        font-size: 0.9rem;
        color: #64748b;
        font-weight: 600;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .info-box-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e3a8a;
        margin-bottom: 0.5rem;
    }

    .info-box-subtitle {
        font-size: 0.85rem;
        color: #94a3b8;
    }

    /* Team cards */
    .team-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }

    .team-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(2,6,23,0.06);
        border-left: 4px solid #3b82f6;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .team-avatar {
        width: 72px;
        height: 72px;
        border-radius: 50%;
        background: linear-gradient(135deg,#3b82f6 0%, #60a5fa 100%);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1.25rem;
        flex: 0 0 56px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    }

    .team-info {
        display: flex;
        flex-direction: column;
    }

    .team-name {
        font-weight: 700;
        color: #0f172a;
        margin: 0;
    }

    .team-role {
        margin: 0;
        color: #64748b;
        font-size: 0.9rem;
    }

    /* Badge de statut */
    .status-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        margin-top: 0.5rem;
    }

    .status-critical {
        background: #fee2e2;
        color: #991b1b;
    }

    .status-warning {
        background: #fef3c7;
        color: #92400e;
    }

    .status-success {
        background: #d1fae5;
        color: #065f46;
    }
    </style>
    """, unsafe_allow_html=True)

# Appliquer le CSS
local_css()

# Responsive sidebar behavior: keep collapsed by default (mobile), expand on large screens
import streamlit.components.v1 as components

components.html("""
<style>
/* Force la sidebar visible sur grands écrans */
@media (min-width: 992px) {{
    section[data-testid="stSidebar"] {{
        transform: none !important;
        left: 0 !important;
        position: relative !important;
        visibility: visible !important;
    }}
    /* Décaler le contenu principal pour faire de la place */
    div[data-testid="stAppViewContainer"] > .main {{
        margin-left: 320px !important;
    }}
}}
</style>
<script>
// Essayer d'ouvrir la sidebar côté client si l'écran est large.
(function(){
    try{
        const breakpoint = 992;
        if(window.innerWidth >= breakpoint){
            // Add class to body to mimic expanded sidebar
            document.documentElement.classList.add('streamlit-sidebar-open');
            document.body.classList.add('streamlit-expanded');
            // Try clicking the toggle if present
            const tryClick = () => {
                const btn = document.querySelector('button[title="Open sidebar"], button[aria-label="Toggle sidebar"], button[data-testid="stSidebarToggle"]');
                if(btn && btn.getAttribute('aria-expanded') !== 'true') btn.click();
            };
            tryClick();
            // also try again after a short delay in case DOM not ready
            setTimeout(tryClick, 500);
        }
    }catch(e){console.warn('sidebar script failed', e)}
})();
</script>
""", height=40)

# Charger les données depuis le fichier JSON
@st.cache_data
def load_data():
    with open('data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

data = load_data()

# Palette de couleurs utilisée pour les séries
COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#6366f1', '#06b6d4']

# Traductions
TRANSLATIONS = {
    'fr': {
        'title': "Rapport de Mission d'Enquête",
        'subtitle': data['project_info']['title'],
        'region': data['project_info']['region'],
        'period': "Période",
        'context': "Contexte de l'Enquête",
        'context_text': f"""
        Raise-Up Cameroon (RUC) est une association fondée en {data['project_info']['founding_year']} par {data['project_info']['founder']}, rassemblant les
        Camerounais patriotes du monde entier. L'association compte {data['ruc_info']['active_members_cameroon']} membres actifs au Cameroun et est
        représentée dans {data['ruc_info']['international_countries']} pays à l'international.

        Cette enquête s'inscrit dans le cadre du projet "{data['project_info']['title']}",
        visant à identifier et répondre aux besoins éducatifs des populations vulnérables dans la région de l'Est.
        """,
        'mission_context': "Contexte de la Mission",
        'team': "Équipe d'Enquête",
        'overview': "Vue d'Ensemble",
        'families_surveyed': "Familles Enquêtées",
        'children_registered': "Enfants Enregistrés",
        'boys': "Garçons",
        'girls': "Filles",
        'localities_map': "Carte des Localités Enquêtées",
        'locality': "Localité",
        'families': "Familles",
        'children': "Enfants",
        'critical_indicators': "Indicateurs Critiques",
        'education_section': "Situation Éducative",
        'school_abandonment': "Abandon Scolaire (Primaire)",
        'families_sacrificing': "Familles Sacrifiant la Scolarisation",
        'no_birth_certificate': "Enfants Sans Acte de Naissance",
        'mining_workers': "Travailleurs Miniers < 18 ans",
        'living_conditions': "Conditions de Vie",
        'no_electricity': "Familles Sans Électricité",
        'no_water': "Familles Sans Eau Potable",
        'no_latrines': "Familles Sans Latrines",
        'far_from_health': "Éloignées Centre de Santé (>10km)",
        'distribution_title': "Distribution par Localité",
        'recommendations': "Recommandations Stratégiques",
        'immediate_actions': "Actions Immédiates (Sept-Déc 2025)",
        'long_term': "Vision à Long Terme",
        'summary': "Résumé Exécutif",
        'income_analysis': "Analyse des Revenus",
        'low_income': "Familles < 25 000 FCFA/mois",
        'avg_household': "Taille Moyenne du Ménage",
        'people': "personnes",
        'about_ruc': "À Propos de RUC",
        'seedesa': "Stratégie SEEDESA - 7 Piliers",
        'notable_cases': "Cas Remarquables",
        'key_findings': "Constats Clés",
        'date': "Date",
        'quarters': "Quartiers/Villages",
        'age': "Âge",
        'previous_edition': "Édition Précédente"
    },
    'en': {
        'title': "Survey Mission Report",
        'subtitle': data['project_info']['title'],
        'region': data['project_info']['region'],
        'period': "Period",
        'context': "Survey Context",
        'context_text': f"""
        Raise-Up Cameroon (RUC) is an association founded in {data['project_info']['founding_year']} by {data['project_info']['founder']}, bringing together
        patriotic Cameroonians from around the world. The association has {data['ruc_info']['active_members_cameroon']} active members in Cameroon and
        is represented in {data['ruc_info']['international_countries']} countries internationally.

        This survey is part of the "{data['project_info']['title']}" project, aimed at
        identifying and addressing the educational needs of vulnerable populations in the East Region.
        """,
        'mission_context': "Mission Context",
        'team': "Survey Team",
        'overview': "Overview",
        'families_surveyed': "Families Surveyed",
        'children_registered': "Children Registered",
        'boys': "Boys",
        'girls': "Girls",
        'localities_map': "Map of Surveyed Localities",
        'locality': "Locality",
        'families': "Families",
        'children': "Children",
        'critical_indicators': "Critical Indicators",
        'education_section': "Educational Situation",
        'school_abandonment': "School Abandonment (Primary)",
        'families_sacrificing': "Families Sacrificing Schooling",
        'no_birth_certificate': "Children Without Birth Certificate",
        'mining_workers': "Mining Workers < 18 years",
        'living_conditions': "Living Conditions",
        'no_electricity': "Families Without Electricity",
        'no_water': "Families Without Drinking Water",
        'no_latrines': "Families Without Latrines",
        'far_from_health': "Far from Health Center (>10km)",
        'distribution_title': "Distribution by Locality",
        'recommendations': "Strategic Recommendations",
        'immediate_actions': "Immediate Actions (Sept-Dec 2025)",
        'long_term': "Long-Term Vision",
        'summary': "Executive Summary",
        'income_analysis': "Income Analysis",
        'low_income': "Families < 25,000 FCFA/month",
        'avg_household': "Average Household Size",
        'people': "people",
        'about_ruc': "About RUC",
        'seedesa': "SEEDESA Strategy - 7 Pillars",
        'notable_cases': "Notable Cases",
        'key_findings': "Key Findings",
        'date': "Date",
        'quarters': "Quarters/Villages",
        'age': "Age",
        'previous_edition': "Previous Edition"
    }
}

# Fonction pour obtenir les traductions
def t(key, lang='fr'):
    return TRANSLATIONS[lang].get(key, key)

# Sidebar
st.sidebar.markdown("---")
lang = st.sidebar.radio("Language / Langue", ['Français', 'English'])
lang_code = 'fr' if lang == 'Français' else 'en'

# En-tête principal avec style
# Header: render as a gradient banner with embedded logo (base64) and flag-underline
logo_src = ""
logo_path = "Logo RUC.png"
if os.path.exists(logo_path):
        try:
                with open(logo_path, 'rb') as f:
                        logo_b64 = base64.b64encode(f.read()).decode()
                        logo_src = f"data:image/png;base64,{logo_b64}"
        except Exception:
                logo_src = ""

header_html = f"""
<div class="main-header" style="display:flex; align-items:center; gap:12px; padding:12px 16px;">
  {f'<img src="{logo_src}" class="header-logo" style="width:64px; height:64px"/>' if logo_src else ''}
  <div>
    <div style="font-weight:700; font-size:20px; margin-bottom:2px;">{t('title', lang_code)}</div>
    <div style="font-size:15px; color:#e0e7ff; margin-bottom:2px;">{t('subtitle', lang_code)}</div>
    <div style="font-size:12px; color:#dbeafe;">{t('region', lang_code)} | {t('period', lang_code)}: {data['project_info']['period']}</div>
  </div>
</div>
<!-- flag underline -->
<div style="display:flex; justify-content:center; margin-top:8px; margin-bottom:16px;">
    <div style="width:240px; display:flex; align-items:center; gap:0;">
        <div style="flex:1; height:12px; background:#2ecc71;"></div>
        <div style="flex:1; height:12px; background:#e74c3c; display:flex; align-items:center; justify-content:center;">
            <div style="font-size:10px; color:yellow; line-height:1;">★</div>
        </div>
        <div style="flex:1; height:12px; background:#f6e05e;"></div>
    </div>
</div>
"""

st.markdown(header_html, unsafe_allow_html=True)

# Section Contexte
with st.expander(f"{t('mission_context', lang_code)}", expanded=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"#### {t('context', lang_code)}")
        st.markdown(t('context_text', lang_code))
    with col2:
        st.markdown(f"#### {t('team', lang_code)}")
        # Créer la liste des membres
        team_html = "<div class='team-container'>"
        
        for member in data['team']:
            team_html += f"<div class='team-member'>{member}</div>"
        team_html += "</div>"
        
        st.markdown(team_html, unsafe_allow_html=True)

# Vue d'ensemble
st.markdown(f'<div class="section-header"><h2>{t("overview", lang_code)}</h2></div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""<div class="info-box">
<div class="info-box-title">{t('families_surveyed', lang_code)}</div>
<div class="info-box-value">{data['survey_data']['total_families']}</div>
<div class="info-box-subtitle">5 {t('localities_map', lang_code).lower()}</div>
</div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""<div class="info-box">
<div class="info-box-title">{t('children_registered', lang_code)}</div>
<div class="info-box-value">{data['survey_data']['total_children']}</div>
<div class="info-box-subtitle">{t('avg_household', lang_code)}: {data['survey_data']['average_household_size']}</div>
</div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""<div class="info-box">
<div class="info-box-title">{t('boys', lang_code)}</div>
<div class="info-box-value">{data['survey_data']['boys']}</div>
<div class="info-box-subtitle">{round(data['survey_data']['boys']/data['survey_data']['total_children']*100, 1)}%</div>
</div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""<div class="info-box">
<div class="info-box-title">{t('girls', lang_code)}</div>
<div class="info-box-value">{data['survey_data']['girls']}</div>
<div class="info-box-subtitle">{round(data['survey_data']['girls']/data['survey_data']['total_children']*100, 1)}%</div>
</div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Carte géographique
st.markdown(f'<div class="section-header"><h2>{t("localities_map", lang_code)}</h2></div>', unsafe_allow_html=True)

# Création du DataFrame pour la carte
map_data = []
for locality in data['localities']:
    map_data.append({
        'locality': locality['name'],
        'lat': locality['latitude'],
        'lon': locality['longitude'],
        'families': locality['families'],
        'children': locality['children']
    })
df_map = pd.DataFrame(map_data)

# Carte avec Plotly
fig_map = px.scatter_mapbox(
    df_map,
    lat='lat',
    lon='lon',
    size='children',
    hover_name='locality',
    hover_data={
        'families': True,
        'children': True,
        'lat': False,
        'lon': False
    },
    color='children',
    color_continuous_scale='Viridis',
    zoom=6,
    height=500
)

fig_map.update_layout(
    mapbox_style="open-street-map",
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

st.plotly_chart(fig_map, use_container_width=True)

# Constats clés par localité
st.markdown(f"#### {t('key_findings', lang_code)}")
for locality in data['localities']:
    with st.expander(f"{locality['name']} - {locality['families']} {t('families', lang_code).lower()}, {locality['children']} {t('children', lang_code).lower()}"):
        st.markdown(f"**{t('date', lang_code)}:** {locality['date']}")
        findings_key = 'key_findings_fr' if lang_code == 'fr' else 'key_findings_en'
        st.markdown(f"**{t('key_findings', lang_code)}:** {locality[findings_key]}")
        if 'quarters_visited' in locality:
            st.markdown(f"**{t('quarters', lang_code)}:** {', '.join(locality['quarters_visited'])}")

# Résumé exécutif
st.markdown(f'<div class="section-header"><h2>{t("summary", lang_code)}</h2></div>', unsafe_allow_html=True)
st.markdown(f'<div class="stat-card">{data["executive_summary"][lang_code]}</div>', unsafe_allow_html=True)

# Indicateurs critiques
st.markdown(f'<div class="section-header"><h2>{t("critical_indicators", lang_code)}</h2></div>', unsafe_allow_html=True)

# Section Éducation
st.markdown(f"### {t('education_section', lang_code)}")
col1, col2 = st.columns(2)

with col1:
    # Graphique abandon scolaire
    fig_abandon = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=data['key_statistics']['education']['primary_abandonment_rate'],
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': t('school_abandonment', lang_code), 'font': {'size': 20, 'color': '#1e3a8a'}},
        delta={'reference': 20, 'increasing': {'color': "red"}},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "#dc2626"},
            'steps': [
                {'range': [0, 20], 'color': "#86efac"},
                {'range': [20, 40], 'color': "#fde047"},
                {'range': [40, 100], 'color': "#fca5a5"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 45
            }
        }
    ))
    fig_abandon.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_abandon, use_container_width=True)

with col2:
    # Graphique familles sacrifiant l'éducation
    fig_sacrifice = go.Figure(go.Indicator(
        mode="gauge+number",
        value=data['key_statistics']['critical_findings']['families_sacrificing_education_percent'],
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': t('families_sacrificing', lang_code), 'font': {'size': 20, 'color': '#1e3a8a'}},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "#dc2626"},
            'steps': [
                {'range': [0, 30], 'color': "#86efac"},
                {'range': [30, 60], 'color': "#fde047"},
                {'range': [60, 100], 'color': "#fca5a5"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 85
            }
        }
    ))
    fig_sacrifice.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_sacrifice, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.metric(
        t('no_birth_certificate', lang_code),
        f"{data['key_statistics']['education']['children_without_birth_certificate_percent']}%",
        delta=f"-{data['key_statistics']['education']['children_without_birth_certificate_percent']}%",
        delta_color="inverse"
    )
with col2:
    st.metric(
        t('mining_workers', lang_code),
        f"{data['key_statistics']['mining']['workers_under_18_percent']}%",
        delta=f"-{data['key_statistics']['mining']['workers_under_18_percent']}%",
        delta_color="inverse"
    )

st.markdown("<br>", unsafe_allow_html=True)

# Conditions de vie
st.markdown(f"### {t('living_conditions', lang_code)}")

# Créer un graphique en barres horizontales
conditions_data = {
    t('no_electricity', lang_code): data['key_statistics']['living_conditions']['families_without_electricity_percent'],
    t('no_water', lang_code): data['key_statistics']['living_conditions']['families_without_water_percent'],
    t('no_latrines', lang_code): data['key_statistics']['living_conditions']['families_without_latrines_percent'],
    t('far_from_health', lang_code): data['key_statistics']['living_conditions']['families_far_from_health_center_percent']
}

colors_for_conditions = [COLORS[3], COLORS[2], COLORS[4], COLORS[1]]
fig_conditions = go.Figure(go.Bar(
    x=list(conditions_data.values()),
    y=list(conditions_data.keys()),
    orientation='h',
    marker=dict(
        color=colors_for_conditions,
        showscale=False,
        line=dict(color='#1e3a8a', width=1)
    ),
    text=[f"{v}%" for v in conditions_data.values()],
    textposition='auto',
    textfont=dict(size=14, color='white', family='Arial Black')
))

fig_conditions.update_layout(
    title={'text': t('living_conditions', lang_code), 'font': {'size': 22, 'color': '#1e3a8a'}},
    xaxis_title="Pourcentage (%)" if lang_code == 'fr' else "Percentage (%)",
    height=400,
    showlegend=False,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(gridcolor='#e2e8f0'),
    yaxis=dict(gridcolor='#e2e8f0')
)

st.plotly_chart(fig_conditions, use_container_width=True)

# Distribution par localité
st.markdown(f'<div class="section-header"><h2>{t("distribution_title", lang_code)}</h2></div>', unsafe_allow_html=True)

# Créer DataFrame pour les graphiques
df_localities = pd.DataFrame([
    {
        t('locality', lang_code): loc['name'],
        t('families', lang_code): loc['families'],
        t('children', lang_code): loc['children']
    }
    for loc in data['localities']
])

# Graphique combiné avec deux axes
fig_combined = make_subplots(
    rows=1, cols=1,
    specs=[[{"secondary_y": True}]]
)

fig_combined.add_trace(
    go.Bar(
        x=df_localities[t('locality', lang_code)],
        y=df_localities[t('families', lang_code)],
        name=t('families', lang_code),
        # assign a color per locality by cycling through the palette
        marker_color=[COLORS[i % len(COLORS)] for i in range(len(df_localities))],
        text=df_localities[t('families', lang_code)],
        textposition='outside',
        textfont=dict(color='white', size=12),
    ),
    secondary_y=False,
)

fig_combined.add_trace(
    go.Scatter(
        x=df_localities[t('locality', lang_code)],
        y=df_localities[t('children', lang_code)],
        name=t('children', lang_code),
        # keep the line a single color but color markers per locality to match the bars
        mode='lines+markers+text',
        text=df_localities[t('children', lang_code)],
        textposition='top center',
        textfont=dict(color='white', size=12),
        line=dict(width=3, color=COLORS[1]),
        marker=dict(size=12, color=[COLORS[i % len(COLORS)] for i in range(len(df_localities))])
    ),
    secondary_y=True,
)

fig_combined.update_layout(
    title={'text': f"{t('distribution_title', lang_code)}", 'font': {'size': 24, 'color': '#1e3a8a'}},
    height=500,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    hovermode='x unified',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

fig_combined.update_xaxes(title_text=t('locality', lang_code))
fig_combined.update_yaxes(title_text=t('families', lang_code), secondary_y=False)
fig_combined.update_yaxes(title_text=t('children', lang_code), secondary_y=True)

st.plotly_chart(fig_combined, use_container_width=True)

# Graphique camembert
col1, col2 = st.columns(2)

with col1:
    fig_pie_families = px.pie(
        df_localities,
        values=t('families', lang_code),
        names=t('locality', lang_code),
        title=f"{t('distribution_title', lang_code)} - {t('families', lang_code)}",
        color_discrete_sequence=COLORS
    )
    st.plotly_chart(fig_pie_families, use_container_width=True)

with col2:
    fig_pie_children = px.pie(
        df_localities,
        values=t('children', lang_code),
        names=t('locality', lang_code),
        title=f"{t('distribution_title', lang_code)} - {t('children', lang_code)}",
        color_discrete_sequence=COLORS
    )
    st.plotly_chart(fig_pie_children, use_container_width=True)

st.markdown("---")

# Analyse des revenus
st.markdown(f'<div class="section-header"><h2>{t("income_analysis", lang_code)}</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.metric(t('low_income', lang_code), f"{data['key_statistics']['income']['families_below_25000_fcfa_percent']}%")
with col2:
    st.metric(t('avg_household', lang_code), f"{data['survey_data']['average_household_size']} {t('people', lang_code)}")

# Graphique revenus
income_data = pd.DataFrame({
    'Category': ['< 25,000 FCFA', '≥ 25,000 FCFA'],
    'Percentage': [
        data['key_statistics']['income']['families_below_25000_fcfa_percent'],
        100 - data['key_statistics']['income']['families_below_25000_fcfa_percent']
    ]
})

fig_income = px.pie(
    income_data,
    values='Percentage',
    names='Category',
    title=t('income_analysis', lang_code),
    color_discrete_sequence=['#ff4444', '#44ff44']
)
st.plotly_chart(fig_income, use_container_width=True)

st.markdown("---")

# Cas remarquables
st.markdown(f'<div class="section-header"><h2>{t("notable_cases", lang_code)}</h2></div>', unsafe_allow_html=True)

cols = st.columns(2)
for idx, case in enumerate(data['notable_cases']):
    with cols[idx % 2]:
        story_key = 'story_fr' if lang_code == 'fr' else 'story_en'

        # Construction du HTML sans balises visibles
        age_html = ""
        if 'age' in case:
            age_html = f"<p><strong>{t('age', lang_code)}:</strong> {case['age']} ans</p>"

        case_html = f"""<div class="case-card">
<h3>{case['name']}</h3>
{age_html}
<p><strong>{t('locality', lang_code)}:</strong> {case['location']}</p>
<p>{case[story_key]}</p>
</div>"""
        st.markdown(case_html, unsafe_allow_html=True)

# Recommandations
st.markdown(f'<div class="section-header"><h2>{t("recommendations", lang_code)}</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### {t('immediate_actions', lang_code)}")
    for rec in data['recommendations']['immediate_actions']:
        action_key = 'action_fr' if lang_code == 'fr' else 'action_en'
        st.markdown(f'<div class="recommendation-box-urgent">✓ {rec[action_key]}</div>', unsafe_allow_html=True)

with col2:
    st.markdown(f"### {t('long_term', lang_code)}")
    for rec in data['recommendations']['long_term']:
        action_key = 'action_fr' if lang_code == 'fr' else 'action_en'
        st.markdown(f'<div class="recommendation-box">• {rec[action_key]}</div>', unsafe_allow_html=True)

# À propos de RUC
st.markdown(f'<div class="section-header"><h2>{t("about_ruc", lang_code)}</h2></div>', unsafe_allow_html=True)

st.markdown(f"### {t('seedesa', lang_code)}")

# Créer 7 colonnes pour les 7 piliers
cols = st.columns(7)
for idx, pillar in enumerate(data['seedesa_pillars']):
    with cols[idx]:
        name_key = 'name_fr' if lang_code == 'fr' else 'name_en'
        st.markdown(f"""
            <div style="text-align: center; padding: 1rem; background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{pillar['icon']}</div>
                <div style="font-weight: 600; color: #1e3a8a; font-size: 0.9rem;">{pillar[name_key]}</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Édition précédente
st.markdown(f"#### {t('previous_edition', lang_code)}")
prev = data['previous_edition']
st.markdown(f"""
    <div class="stat-card">
        <strong>{prev['name']}</strong> - {prev['year']}<br>
        <strong>Régions / Regions:</strong> {', '.join(prev['regions'])}<br>
        <strong>Enfants aidés / Children helped:</strong> {prev['children_helped']}
    </div>
""", unsafe_allow_html=True)

# Footer
slogan_key = 'slogan_fr' if lang_code == 'fr' else 'slogan_en'
today = datetime.now().strftime("%d/%m/%Y") if lang_code == 'fr' else datetime.now().strftime("%Y-%m-%d")

st.markdown(f"""
    <div class="footer" style="color: #ffffff !important;">
        <h3 style="color: #ffffff !important; margin-bottom: 0.5rem;">Raise-Up Cameroon (RUC)</h3>
        <p style="font-size: 1.1rem; font-style: italic; color: #ffffff !important;">"{data['project_info'][slogan_key]}"</p>
        <p style="margin-top: 1rem; color: rgba(255,255,255,0.95) !important;">Fondée en {data['project_info']['founding_year']} | {data['ruc_info']['active_members_cameroon']} membres actifs</p>
        <p style="margin-top: 0.5rem; color: rgba(255,255,255,0.95) !important;">{"Date : " if lang_code == 'fr' else "Date: "}{today}</p>
    </div>
""", unsafe_allow_html=True)
