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

# Charger les données depuis le fichier JSON
@st.cache_data
def load_data():
    with open('data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

data = load_data()

# Traductions
TRANSLATIONS = {
    'fr': {
        'title': "Rapport de Mission d'Enquête RUC",
        'subtitle': data['project_info']['title'],
        'region': data['project_info']['region'],
        'period': "Période",
        'context': "Contexte de l'Enquête",
        'context_text': f"""
        Raise-Up Cameroon (RUC) est une association fondée en {data['ruc_info']['active_members_cameroon']} par {data['project_info']['founder']}, rassemblant les
        Camerounais patriotes du monde entier. L'association compte {data['ruc_info']['active_members_cameroon']} membres actifs au Cameroun et est
        représentée dans {data['ruc_info']['international_countries']} pays à l'international.

        Cette enquête s'inscrit dans le cadre du projet "{data['project_info']['title']}",
        visant à identifier et répondre aux besoins éducatifs des populations vulnérables dans la région de l'Est.
        """,
        'mission_context': "Contexte de la Mission",
        'team': "Équipe d'Enquête",
        'overview': "Vue d'Ensemble",
        'key_figures': "Chiffres Clés",
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
        'far_from_health': "Familles Éloignées Centre de Santé (>10km)",
        'distribution_title': "Distribution par Localité",
        'recommendations': "Recommandations Stratégiques",
        'immediate_actions': "Actions Immédiates (Sept-Déc 2025)",
        'long_term': "Vision à Long Terme",
        'summary': "Résumé Exécutif",
        'by_locality': "Données par Localité",
        'income_analysis': "Analyse des Revenus",
        'low_income': "Familles avec Revenu < 25 000 FCFA/mois",
        'avg_household': "Taille Moyenne du Ménage",
        'people': "personnes",
        'about_ruc': "À Propos de RUC",
        'seedesa': "Stratégie SEEDESA - 7 Piliers",
        'notable_cases': "Cas Remarquables",
        'key_findings': "Constats Clés par Localité",
        'partners': "Partenaires",
        'methodology': "Méthodologie",
        'previous_edition': "Édition Précédente"
    },
    'en': {
        'title': "RUC Survey Mission Report",
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
        'key_figures': "Key Figures",
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
        'far_from_health': "Families Far from Health Center (>10km)",
        'distribution_title': "Distribution by Locality",
        'recommendations': "Strategic Recommendations",
        'immediate_actions': "Immediate Actions (Sept-Dec 2025)",
        'long_term': "Long-Term Vision",
        'summary': "Executive Summary",
        'by_locality': "Data by Locality",
        'income_analysis': "Income Analysis",
        'low_income': "Families with Income < 25,000 FCFA/month",
        'avg_household': "Average Household Size",
        'people': "people",
        'about_ruc': "About RUC",
        'seedesa': "SEEDESA Strategy - 7 Pillars",
        'notable_cases': "Notable Cases",
        'key_findings': "Key Findings by Locality",
        'partners': "Partners",
        'methodology': "Methodology",
        'previous_edition': "Previous Edition"
    }
}

# Fonction pour obtenir les traductions
def t(key, lang='fr'):
    return TRANSLATIONS[lang].get(key, key)

# Sidebar pour la sélection de langue
st.sidebar.image("Logo RUC.png", use_container_width=True)
st.sidebar.markdown("---")
lang = st.sidebar.radio("Language / Langue", ['Français', 'English'])
lang_code = 'fr' if lang == 'Français' else 'en'

# En-tête
st.title(t('title', lang_code))
st.markdown(f"### {t('subtitle', lang_code)}")
st.markdown(f"**{t('region', lang_code)}**")
st.markdown(f"**{t('period', lang_code)}:** {data['project_info']['period']}")
st.markdown("---")

# Section Contexte
with st.expander(f"ℹ️ {t('mission_context', lang_code)}", expanded=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"### {t('context', lang_code)}")
        st.markdown(t('context_text', lang_code))
    with col2:
        st.markdown(f"### {t('team', lang_code)}")
        for member in data['team']:
            st.markdown(f"• {member}")

# Vue d'ensemble
st.header(f"📊 {t('overview', lang_code)}")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(t('families_surveyed', lang_code), f"{data['survey_data']['total_families']}")
with col2:
    st.metric(t('children_registered', lang_code), f"{data['survey_data']['total_children']}")
with col3:
    st.metric(t('boys', lang_code), f"{data['survey_data']['boys']}")
with col4:
    st.metric(t('girls', lang_code), f"{data['survey_data']['girls']}")

st.markdown("---")

# Carte géographique
st.header(f"🗺️ {t('localities_map', lang_code)}")

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
    color_continuous_scale='Reds',
    zoom=6,
    height=500
)

fig_map.update_layout(
    mapbox_style="open-street-map",
    margin={"r": 0, "t": 0, "l": 0, "b": 0}
)

st.plotly_chart(fig_map, use_container_width=True)

# Tableau des localités avec constats clés
st.subheader(f"{t('key_findings', lang_code)}")
for locality in data['localities']:
    with st.expander(f"📍 {locality['name']} - {locality['families']} {t('families', lang_code).lower()}, {locality['children']} {t('children', lang_code).lower()}"):
        st.markdown(f"**Date:** {locality['date']}")
        findings_key = 'key_findings_fr' if lang_code == 'fr' else 'key_findings_en'
        st.markdown(f"**{t('key_findings', lang_code)}:** {locality[findings_key]}")
        if 'quarters_visited' in locality:
            st.markdown(f"**Quartiers/Villages:** {', '.join(locality['quarters_visited'])}")

st.markdown("---")

# Résumé exécutif
st.header(f"📋 {t('summary', lang_code)}")
st.markdown(data['executive_summary'][lang_code])

st.markdown("---")

# Indicateurs critiques
st.header(f"⚠️ {t('critical_indicators', lang_code)}")

# Section Éducation
st.subheader(f"🎓 {t('education_section', lang_code)}")
col1, col2 = st.columns(2)

with col1:
    # Graphique abandon scolaire
    fig_abandon = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=data['key_statistics']['education']['primary_abandonment_rate'],
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': t('school_abandonment', lang_code)},
        delta={'reference': 20, 'increasing': {'color': "red"}},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkred"},
            'steps': [
                {'range': [0, 20], 'color': "lightgreen"},
                {'range': [20, 40], 'color': "yellow"},
                {'range': [40, 100], 'color': "salmon"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 45
            }
        }
    ))
    fig_abandon.update_layout(height=300)
    st.plotly_chart(fig_abandon, use_container_width=True)

with col2:
    # Graphique familles sacrifiant l'éducation
    fig_sacrifice = go.Figure(go.Indicator(
        mode="gauge+number",
        value=data['key_statistics']['critical_findings']['families_sacrificing_education_percent'],
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': t('families_sacrificing', lang_code)},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkred"},
            'steps': [
                {'range': [0, 30], 'color': "lightgreen"},
                {'range': [30, 60], 'color': "yellow"},
                {'range': [60, 100], 'color': "salmon"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 85
            }
        }
    ))
    fig_sacrifice.update_layout(height=300)
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

st.markdown("---")

# Conditions de vie
st.subheader(f"🏠 {t('living_conditions', lang_code)}")

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
        showscale=True
    ),
    text=[f"{v}%" for v in conditions_data.values()],
    textposition='auto'
))

fig_conditions.update_layout(
    title=t('living_conditions', lang_code),
    xaxis_title="Pourcentage (%)" if lang_code == 'fr' else "Percentage (%)",
    height=400,
    showlegend=False
)

st.plotly_chart(fig_conditions, use_container_width=True)

st.markdown("---")

# Distribution par localité
st.header(f"📍 {t('distribution_title', lang_code)}")

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
    # Graphique familles par localité
    fig_families = px.bar(
        df_localities,
        x=t('locality', lang_code),
        y=t('families', lang_code),
        title=t('families', lang_code),
        color=t('families', lang_code),
        color_continuous_scale='Blues'
    )
    fig_families.update_layout(showlegend=False)
    st.plotly_chart(fig_families, use_container_width=True)

with col2:
    # Graphique enfants par localité
    fig_children = px.bar(
        df_localities,
        x=t('locality', lang_code),
        y=t('children', lang_code),
        title=t('children', lang_code),
        color=t('children', lang_code),
        color_continuous_scale='Greens'
    )
    fig_children.update_layout(showlegend=False)
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
st.header(f"💰 {t('income_analysis', lang_code)}")

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
st.header(f"👥 {t('notable_cases', lang_code)}")
cols = st.columns(2)
for idx, case in enumerate(data['notable_cases']):
    with cols[idx % 2]:
        story_key = 'story_fr' if lang_code == 'fr' else 'story_en'
        with st.container():
            st.markdown(f"### {case['name']}")
            if 'age' in case:
                st.markdown(f"**Âge / Age:** {case['age']} ans / years")
            st.markdown(f"**{t('locality', lang_code)}:** {case['location']}")
            st.markdown(case[story_key])
            st.markdown("---")

st.markdown("---")

# Recommandations
st.header(f"💡 {t('recommendations', lang_code)}")

col1, col2 = st.columns(2)

with col1:
    st.subheader(t('immediate_actions', lang_code))
    for rec in data['recommendations']['immediate_actions']:
        action_key = 'action_fr' if lang_code == 'fr' else 'action_en'
        st.markdown(f"✓ {rec[action_key]}")

with col2:
    st.subheader(t('long_term', lang_code))
    for rec in data['recommendations']['long_term']:
        action_key = 'action_fr' if lang_code == 'fr' else 'action_en'
        st.markdown(f"• {rec[action_key]}")

st.markdown("---")

# À propos de RUC
st.header(f"ℹ️ {t('about_ruc', lang_code)}")

st.markdown(f"### {t('seedesa', lang_code)}")

# Créer 7 colonnes pour les 7 piliers
cols = st.columns(7)
for idx, pillar in enumerate(data['seedesa_pillars']):
    with cols[idx]:
        st.markdown(f"### {pillar['icon']}")
        name_key = 'name_fr' if lang_code == 'fr' else 'name_en'
        st.markdown(f"**{pillar[name_key]}**")

st.markdown("---")

# Édition précédente
st.subheader(f"📚 {t('previous_edition', lang_code)}")
prev = data['previous_edition']
st.markdown(f"**{prev['name']}** - {prev['year']}")
st.markdown(f"**Régions:** {', '.join(prev['regions'])}")
st.markdown(f"**Enfants aidés / Children helped:** {prev['children_helped']}")

# Footer
st.markdown("---")
slogan_key = 'slogan_fr' if lang_code == 'fr' else 'slogan_en'
st.markdown(
    f"""
    <div style='text-align: center; color: gray;'>
        <p>Raise-Up Cameroon (RUC) - {data['project_info']['founding_year']}</p>
        <p>"{data['project_info'][slogan_key]}"</p>
    </div>
    """,
    unsafe_allow_html=True
)
