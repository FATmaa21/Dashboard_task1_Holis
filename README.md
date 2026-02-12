# Dashboard_task1_Holis
Test technique de visualisation de données

## Description 

Ce tableau de bord permet : 

- D'explorer les impacts environnementaux d'un procédé choisi.
- De visualiser les principaux indicateurs d'impact.
- D'afficher les métadonnées associées au procédé
- D'obtenir une comparaison entre les procédés pour un indicateur d'impact.
  
## Outils utilisés

- Python (sous VScode)
- Pandas
- Streamlit
- Plotly

## Sources de données

Ce dashboard utilise deux fichiers indispensables :
- Procedes_Details.xlsx : Contient les métadonnées des procédés.
- Procedes_Impacts.csv : Contient l'ensemble des scores d'impacts environnementaux.

Note : Stocker ces fichiers dans le même répertoire que le fichier app.py pour assurer le bon chargement des données.

## Lancer le dashboard

```bash
pip install -r requirements.txt
streamlit run app.py
