# dashboard
# Application Streamlit de Visualisation des Données Météorologiques

## Description
Cette application Streamlit utilise les données météorologiques régionales pour permettre la visualisation, la prédiction de température, et la géolocalisation des régions en France.

## Fonctionnalités

### Visualisation des Données Météorologiques
- Affichage d'un nuage de points avec les températures minimales, maximales, et moyennes par région.
- Filtres disponibles : région, année, mois.

### Prédiction de Température
- Modélisation de la température moyenne en fonction de la région et de la date.
- Prédiction de la température pour une date sélectionnée.

### Géolocalisation des Régions
- Affichage d'une carte avec les emplacements géographiques des régions en France.

## Utilisation

1. Installez les dépendances en exécutant `pip install -r requirements.txt`.
2. Exécutez l'application avec la commande `streamlit run test.py`.
3. Ouvrez le lien généré dans votre navigateur.

## Structure du Projet

- `app.py`: Le script principal contenant le code de l'application Streamlit.
- `requirements.txt`: Liste des dépendances Python nécessaires.
- `README.md`: Ce fichier.



## Remarques
- Assurez-vous d'avoir une connexion Internet active pour charger les données en temps réel.
- Ce projet utilise Streamlit, Pandas, Scikit-learn, Matplotlib, Folium, Plotly, etc.

