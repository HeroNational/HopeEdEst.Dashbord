import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

# Configuration de la page
st.set_page_config(
    page_title="Rapport RUC - Région de l'Est",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fonction pour injecter le CSS de manière cachée
def local_css():
    st.markdown("""
    <style>
    /* Masquer le CSS affiché */
    .main {
        background-color: #f8f9fa;
    }

    /* En-tête principal */
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .main-header h3 {
        color: #e0e7ff;
        font-weight: 400;
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
    </style>
    """, unsafe_allow_html=True)

# Appliquer le CSS
local_css()

# Charger les données depuis le fichier JSON
@st.cache_data
def load_data():
    with open('data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

data = load_data()

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
st.sidebar.image("Logo RUC.png", use_container_width=True)
st.sidebar.markdown("---")
lang = st.sidebar.radio("Language / Langue", ['Français', 'English'])
lang_code = 'fr' if lang == 'Français' else 'en'

# En-tête principal avec style
st.markdown(f"""
    <div class="main-header">
        <h1>{t('title', lang_code)}</h1>
        <h3>{t('subtitle', lang_code)}</h3>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem;">{t('region', lang_code)} | {t('period', lang_code)}: {data['project_info']['period']}</p>
    </div>
""", unsafe_allow_html=True)

# Section Contexte
with st.expander(f"{t('mission_context', lang_code)}", expanded=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"#### {t('context', lang_code)}")
        st.markdown(t('context_text', lang_code))
    with col2:
        st.markdown(f"#### {t('team', lang_code)}")
        for member in data['team']:
            st.markdown(f"• {member}")

# Vue d'ensemble
st.markdown(f'<div class="section-header"><h2>{t("overview", lang_code)}</h2></div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(t('families_surveyed', lang_code), f"{data['survey_data']['total_families']}")
with col2:
    st.metric(t('children_registered', lang_code), f"{data['survey_data']['total_children']}")
with col3:
    st.metric(t('boys', lang_code), f"{data['survey_data']['boys']}")
with col4:
    st.metric(t('girls', lang_code), f"{data['survey_data']['girls']}")

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
    color_continuous_scale='Blues',
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

fig_conditions = go.Figure(go.Bar(
    x=list(conditions_data.values()),
    y=list(conditions_data.keys()),
    orientation='h',
    marker=dict(
        color=list(conditions_data.values()),
        colorscale='Reds',
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

col1, col2 = st.columns(2)

with col1:
    fig_families = px.bar(
        df_localities,
        x=t('locality', lang_code),
        y=t('families', lang_code),
        title=t('families', lang_code),
        color=t('families', lang_code),
        color_continuous_scale='Blues',
        text=t('families', lang_code)
    )
    fig_families.update_traces(texttemplate='%{text}', textposition='outside')
    fig_families.update_layout(
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font=dict(size=20, color='#1e3a8a')
    )
    st.plotly_chart(fig_families, use_container_width=True)

with col2:
    fig_children = px.bar(
        df_localities,
        x=t('locality', lang_code),
        y=t('children', lang_code),
        title=t('children', lang_code),
        color=t('children', lang_code),
        color_continuous_scale='Greens',
        text=t('children', lang_code)
    )
    fig_children.update_traces(texttemplate='%{text}', textposition='outside')
    fig_children.update_layout(
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font=dict(size=20, color='#1e3a8a')
    )
    st.plotly_chart(fig_children, use_container_width=True)

# Graphique camembert
col1, col2 = st.columns(2)

with col1:
    fig_pie_families = px.pie(
        df_localities,
        values=t('families', lang_code),
        names=t('locality', lang_code),
        title=f"{t('distribution_title', lang_code)} - {t('families', lang_code)}"
    )
    st.plotly_chart(fig_pie_families, use_container_width=True)

with col2:
    fig_pie_children = px.pie(
        df_localities,
        values=t('children', lang_code),
        names=t('locality', lang_code),
        title=f"{t('distribution_title', lang_code)} - {t('children', lang_code)}"
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
st.markdown(f"""
    <div class="footer">
        <h3>Raise-Up Cameroon (RUC)</h3>
        <p style="font-size: 1.1rem; font-style: italic;">"{data['project_info'][slogan_key]}"</p>
        <p style="margin-top: 1rem; opacity: 0.9;">Fondée en {data['project_info']['founding_year']} | {data['ruc_info']['active_members_cameroon']} membres actifs</p>
    </div>
""", unsafe_allow_html=True)
