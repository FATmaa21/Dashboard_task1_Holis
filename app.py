import pandas as pd
import streamlit as st
import plotly.express as px

#CONFIGURATION DE LA PAGE STREAMLIT
st.set_page_config(page_title="Dashboard de Fatimata", layout="wide")
st.title("🍀 Test technique Holis – Dashboard 🍀 ")

# CHARGEMENT DES DONNEES
procedes = pd.read_excel("Procedes_Details.xlsx", header=None)
impacts = pd.read_csv("Procedes_Impacts.csv", encoding="ISO-8859-1", sep=None, engine="python")
impacts = impacts.iloc[1:].copy() #Je retire les en-têtes qui sont à la prémière ligne.

# CONSTRUCTION PARTIE METADONNEE
# Je selectionne les informations clés pour l'identification des différents procédés.
proc_table = pd.DataFrame({
    "uuid": procedes.iloc[2, 2:].astype(str).str.strip(),#je mets tout au format string et je nettoie les espaces.
    "name_fr": procedes.iloc[3, 2:].astype(str).str.strip(),
    "name_en": procedes.iloc[4, 2:].astype(str).str.strip(),
    "cat_lvl1": procedes.iloc[9, 2:].astype(str).str.strip()
})

#CONSTRUCTION FILTRE CATEGORIES
st.sidebar.header("Filtres")

categories = sorted(proc_table["cat_lvl1"].dropna().unique()) #je retire les valeurs N/a,les doublons et rangement par ordre alphabétique.
cat_choice = st.sidebar.selectbox("Filtrer par catégorie (niveau 1)", ["Toutes"] + categories) #Je rajoute l'option "toutes" pour avoir une vue d'ensemble initiale. 

if cat_choice != "Toutes":
    filtered_proc = proc_table[proc_table["cat_lvl1"] == cat_choice] #Je conserve que les lignes concernées par la catégorie choisie par l'utilisateur.
else:
    filtered_proc = proc_table

#CONSTRUCTION FILTRE PROCEDES
choice_proc = st.sidebar.selectbox(
    "Choisir un procédé",
    sorted(filtered_proc["name_fr"].dropna().unique())
)

# LE TOP DES CONTRIBUTEURS
top_n = st.sidebar.slider("Top impacts à afficher", 5, 20, 10)

#EXTRACTION DU UUID DU PROCEDE CHOISI
uuid_proc = proc_table.loc[proc_table["name_fr"] == choice_proc, "uuid"].iloc[0]

#AFFICHAGE DES METADONNEES
st.subheader("1) Description du procédé (Métadonnées)")
row = proc_table[proc_table["uuid"] == uuid_proc].iloc[0] #Je récupère et je stocke ici la ligne entière réliée à l'uuid choisi.

st.write({
    "Nom FR": row["name_fr"],
    "Nom EN": row["name_en"],
    "Catégorie": row["cat_lvl1"],
    "UUID": row["uuid"]
})

# TOP IMPACTS PAR PROCEDE
st.divider()
st.subheader(f'2) Impacts principaux (Top {top_n})')

df = impacts[[impacts.columns[2], impacts.columns[3], uuid_proc]].copy() # à faire chécker
df.columns = ["Indicateur", "Unité", "Valeur"]

df["Valeur"] = pd.to_numeric(df["Valeur"], errors="coerce") #je transforme les valeurs en nombre et je remplace les vides par des n/a.
df = df.dropna(subset=["Valeur"]) #Je nettoie les n/a et en même temps la ligne qui va avec.

df["abs"] = df["Valeur"].abs() #Je crée une nouvelle colonne qui stocke les valeurs absolues.
df_top = df.sort_values("abs", ascending=False).head(top_n) #Je range dans l'ordre decroissant et je garde que les n prémières lignes. n est choisi grace à la slidebar.

st.dataframe(df_top[["Indicateur", "Valeur", "Unité"]], width="stretch")#Je fais l'affichage dans un tableau.

# AFFICHAGE DIAGRAMME EN BARRE
fig = px.bar(
    df_top.sort_values("Valeur"), # Affichage dans l'ordre décroissant des barres pour avoir l'effet escalier.
    x="Valeur",
    y="Indicateur",
    orientation="h",
    title=f"Top {top_n} impacts – {choice_proc}",
)

st.plotly_chart(fig, use_container_width=True)

#  COMPARAISON PROCEDES PAR INDICATEUR
st.divider()
st.subheader("3) Classement des procédés par indicateur")


indicator_list = sorted(impacts[impacts.columns[2]].unique())#Je récupère la liste des indicateurs.
selected_ind = st.selectbox("Sélectionner un indicateur pour comparer tous les procédés", indicator_list)#J'isole l'indicateur choisi.

# Je récupère toutes les colonnes à partir des uuid.
ind_line = impacts[impacts[impacts.columns[2]] == selected_ind].iloc[0]
values_only = ind_line.iloc[4:] 

# Je crée un petit tableau de classement.
rank_df = pd.DataFrame({
    "uuid": values_only.index,
    "Score": pd.to_numeric(values_only.values, errors="coerce")
}).dropna()

# Je trie pour avoir les 10 plus gros impacts.
rank_df = rank_df.sort_values("Score", ascending=False).head(10)

#Je fais une jointure pour récupérer les noms des procédés correspondants aux UUIDs trouvés pour le classement.
rank_df = rank_df.merge(proc_table[["uuid", "name_fr"]], on="uuid", how="left")

#Affichage dans un tableau des résultats.
st.write(f"Top 10 des procédés les plus impactants pour : **{selected_ind}**")
st.dataframe(rank_df[["name_fr", "Score"]], use_container_width=True)

st.divider() #
st.caption("Réalisé par Fatimata")