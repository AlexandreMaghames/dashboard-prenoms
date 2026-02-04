# 📊 Visualisation de l’évolution des prénoms en France

Cette application Streamlit permet d’explorer l’évolution du nombre de naissances d’un prénom en France au fil des années. Les données peuvent être filtrées par prénom et, si disponibles, par sexe. Les graphiques interactifs sont générés avec Plotly pour une expérience utilisateur optimale.

## 📝 Fonctionnalités
- Filtrage des données par prénom.
- Agrégation des naissances par sexe, et par année.
- Graphiques interactifs avec Plotly Express.
- Interface simple et intuitive via Streamlit.

## 📂 Structure du projet
```
project/
│
├─ data/
│  └─ geojson/                 # Fichiers GeoJSON (optionnels pour la géolocalisation)
│
├─ src/
│  ├─ data_preprocessing/
│  │    └─ process_data.py     # Script pour traiter et préparer les données
│  ├─ filter_aggregate/        # Fonctions pour filtrer et agréger les données
│  └─ visualisation/           # Fonctions pour générer les graphiques
│
├─ home.py                      # Script principal Streamlit
├─ requirements.txt             # Dépendances Python
└─ README.md
```

Pour lancer le projet en local : 
- Télécharger les données depuis [data.gouv](https://www.insee.fr/fr/statistiques/7633685)
- Mettre les données dans le dossier ```data/```
- Prétraiter les données avec : 
```python
python src/data_preprocessing/process_data.py
```

Lancer l'interface avec :
```python
streamlit run home.py
```


## Contributors
[MAGHAMES Alexandre](https://github.com/AlexandreMaghames)