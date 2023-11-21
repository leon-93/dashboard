import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from datetime import datetime, timedelta
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression
st.title('visualisation des données métrologiques par régions ')
url = "https://opendata.reseaux-energies.fr/explore/dataset/temperature-quotidienne-regionale/download/?format=csv&timezone=Europe/Berlin&use_labels_for_header=false"
data = pd.read_csv(url, sep=';')

temperature_data = data[['tmin', 'tmax', 'tmoy']]

plt.figure(figsize=(12, 6))
plt.scatter(data['region'], temperature_data['tmin'], label='Tmin', color='blue')
plt.scatter(data['region'], temperature_data['tmax'], label='Tmax', color='red')
plt.scatter(data['region'], temperature_data['tmoy'], label='Tmoy', color='green')

plt.xlabel('region')
plt.ylabel('Température (°C)')
plt.title('Température quotidienne')
plt.legend()
plt.grid()
plt.tight_layout()
plt.xticks(rotation=45)  
st.pyplot(plt)
 #Créez une liste des régions uniques
regions = data['region'].unique()
regions = ['Toutes'] + list(regions)  

# Créez une liste des années uniques
years = data['date'].str[:4].unique()
years = ['Toutes'] + list(years)  

# Créez une liste des mois uniques
months = data['date'].str[5:7].unique()
months = ['Tous'] + list(months)  # Ajoutez une option "Tous" pour tous les mois

# Titre de l'application
st.title("Visualisation des températures")

# Sélectionnez la région
selected_region = st.selectbox("Sélectionnez une région", regions)

# Sélectionnez l'année
selected_year = st.selectbox("Sélectionnez une année", years)

# Sélectionnez le mois
selected_month = st.selectbox("Sélectionnez un mois", months)

# Filtrage des données en fonction des sélections
filtered_data = data.copy()

if selected_region != 'Toutes':
    filtered_data = filtered_data[filtered_data['region'] == selected_region]

if selected_year != 'Toutes':
    filtered_data = filtered_data[filtered_data['date'].str[:4] == selected_year]

if selected_month != 'Tous':
    filtered_data = filtered_data[filtered_data['date'].str[5:7] == selected_month]
# Afficher les données filtrées
st.write(f"Données pour la région {selected_region} :")
st.write(filtered_data)
# Créez un nuage de points (scatter plot) en coloriant les températures maximales et minimales
fig, ax = plt.subplots()
ax.plot(
    filtered_data['date'],
    filtered_data['tmin'],
    c='blue',
    label='Température minimale (°C)',
    marker='o'
)

ax.plot(
    filtered_data['date'],
    filtered_data['tmax'],
    c='red',
    label='Température maximale (°C)',
    marker='^'
)

plt.xlabel('Date')
plt.ylabel('Température (°C)')
ax.set_title(f'Températures pour la région {selected_region}')
plt.xticks(rotation=100)
plt.legend()
# Affichez le nuage de points
st.pyplot(fig)


# Convertir la colonne 'date' en objets datetime
data['date'] = pd.to_datetime(data['date'])

# Créer une colonne pour le nombre de jours écoulés depuis la date minimale dans votre ensemble de données
data['days_since_min_date'] = (data['date'] - data['date'].min()).dt.days

# Séparer les caractéristiques en catégorielles et numériques
categorical_features = ['region']
numerical_features = ['days_since_min_date']

# Créer un préprocesseur avec ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(), categorical_features)
    ])

# Créer un pipeline avec le préprocesseur et le modèle
model = LinearRegression()
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', model)
])

# Ajuster le préprocesseur et le modèle avec les données d'entraînement
pipeline.fit(data.drop('tmoy', axis=1), data['tmoy'])

# Interface utilisateur Streamlit
st.title('Prédiction de Température')

# Sélection de la région
region_options = data['region'].unique()
selected_region = st.selectbox('Sélectionnez la région:', region_options)

# Sélection de la date

min_date = data['date'].min()
max_date = datetime(2026, 12, 31)
selected_date = st.date_input('Sélectionnez la date:', min_value=min_date.date(), max_value=max_date.date(), value=max_date.date())


# Calculer le nombre de jours depuis la date minimale
days_since_min_date = (selected_date - min_date.date()).days

# Préparer les données pour la prédiction
input_data = pd.DataFrame({
    'region': [selected_region],
    'days_since_min_date': [days_since_min_date]
})

# Prédiction de la température
predicted_temperature = pipeline.predict(input_data)

# Afficher la prédiction
st.write(f"Température prévue pour le {selected_date} en {selected_region}: {predicted_temperature[0]:.2f}°C")
import pydeck as pdk

# Définir les données pour la carte
data = {
    'region': ['Auvergne-Rhône-Alpes', 'Bourgogne-Franche-Comté', 'Bretagne', 'Centre-Val de Loire', 'Corse',
               'Grand Est', 'Hauts-de-France', 'Île-de-France', 'Normandie', 'Nouvelle-Aquitaine', 'Occitanie',
               'Pays de la Loire', 'Provence-Alpes-Côte d\'Azur'],
    'latitude': [45.75, 47.04, 48.11, 47.42, 42.26, 48.82, 50.53, 48.86, 49.46, 45.84, 43.59, 47.48, 43.93],
    'longitude': [4.85, 5.99, -1.68, 1.44, 9.18, 6.29, 2.39, 2.35, -0.36, 0.58, 3.26, -0.53, 5.24]
}

df = pd.DataFrame(data)

# Configurer la carte avec pydeck
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position='[longitude, latitude]',
    get_radius=50000,
    get_fill_color=[255, 0, 0],
    pickable=True,
    auto_highlight=True
)

view_state = pdk.ViewState(
    latitude=46.603354,
    longitude=1.888334,
    zoom=5,
    pitch=45
)

deck = pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=view_state,
    layers=[layer]
)

# Afficher la carte dans Streamlit
st.header("Géolocalisation des régions")
st.pydeck_chart(deck)

