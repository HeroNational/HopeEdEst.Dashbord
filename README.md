# Dashboard RUC - Rapport d'Enquête Région de l'Est

Dashboard interactif pour le rapport de mission d'enquête de Raise-Up Cameroon (RUC) dans la région de l'Est du Cameroun.

## Projet "1 Cameroun, 10 Régions : Hope-édition Soleil Levant"

Ce dashboard présente les résultats de l'enquête menée du 26 août au 8 septembre 2025 dans cinq localités de la région de l'Est : Bertoua, Batouri, Garoua-Boulaï, Bétaré-Oya et Atok.

## Fonctionnalités

- **Interface bilingue** : Français et Anglais
- **Visualisations interactives** : Graphiques, cartes géographiques, indicateurs
- **Données complètes** : 199 familles, 1093 enfants enquêtés
- **Indicateurs clés** : Éducation, conditions de vie, recommandations
- **Carte géographique** : Localisation des zones d'enquête

## Installation

1. Assurez-vous d'avoir Python 3.8 ou supérieur installé

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Lancement de l'application

```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur par défaut à l'adresse `http://localhost:8501`

## Déploiement

### Déploiement sur Streamlit Cloud

1. Créez un compte sur [Streamlit Cloud](https://streamlit.io/cloud)
2. Connectez votre repository GitHub
3. Sélectionnez le fichier `app.py` comme point d'entrée
4. Déployez l'application

### Déploiement sur d'autres plateformes

Le dashboard peut également être déployé sur :
- Heroku
- Google Cloud Run
- AWS
- Azure

## Structure du projet

```
Dashbord RUC/
├── app.py                          # Application principale
├── requirements.txt                # Dépendances Python
├── Logo RUC.png                    # Logo de l'association
├── README.md                       # Documentation
└── Rapport d'enquete RUC copie.docx  # Rapport source
```

## À propos de Raise-Up Cameroon (RUC)

Raise-Up Cameroon est une association fondée en 2023 par Manuella Kengne, rassemblant les Camerounais patriotes du monde entier. L'association compte 69 membres actifs au Cameroun et est représentée dans 9 pays à l'international.

**Slogan** : "Apporte ton fruit au développement de ton pays"

**Stratégie SEEDESA - 7 piliers** :
- Social
- Économique
- Éducation
- Digital, NTIC & IA
- Environnemental
- Santé
- Art et Culture

## Contact

Pour plus d'informations sur Raise-Up Cameroon ou ce projet, veuillez contacter l'association.

---

**© 2025 Raise-Up Cameroon (RUC)**
