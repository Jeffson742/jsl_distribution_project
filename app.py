import streamlit as st
from utils.database_setup import create_tables
from utils.data_queries import get_arrivages, get_clients, get_agences, get_importateurs, get_conteneurs

from utils.data_insertion import (
    insert_arrivage,
    insert_conteneur,
    insert_client,
    insert_agence,
    insert_importateur,
)
from utils.pdf_generator import generate_pdf
from utils.report_generator import fetch_validated_data, generate_validated_declarations_pdf
import pandas as pd

# Initialisation des tables de la base de données
create_tables()

# Désactiver le cache pour garantir des données actualisées
def fetch_importateurs():
    return get_importateurs()

def fetch_clients():
    return get_clients()

def fetch_agences():
    return get_agences()

def fetch_arrivages():
    return get_arrivages()

def main():
    st.title("Dashboard JSL Distribution")
    menu = st.sidebar.selectbox("Menu", ["Gestion des arrivages", "Déclarations validées", "Télécharger un rapport"])

    if menu == "Gestion des arrivages":
        manage_arrivages()
    elif menu == "Déclarations validées":
        manage_validated_declarations()
    elif menu == "Télécharger un rapport":
        download_reports()

def manage_arrivages():
    st.header("Gestion des arrivages et des conteneurs")

    # --- Liste des arrivages ---
    st.subheader("Liste des arrivages")
    arrivages_df = fetch_arrivages()
    if not arrivages_df.empty:
        st.dataframe(arrivages_df)
    else:
        st.warning("Aucun arrivage disponible.")

    # --- Ajouter un nouvel arrivage ---
    st.subheader("Ajouter un nouvel arrivage")
    date_arrivage = st.date_input("Date de l'arrivage")

    # Gestion de l'importateur
    importateurs_list = fetch_importateurs()

    # Ajouter une option pour un nouvel importateur
    options = importateurs_list + ["Ajouter un nouvel importateur..."]

    selected_importateur = st.selectbox("Nom de l'importateur", options)

    # Gestion de l'ajout d'un nouvel importateur
    if selected_importateur == "Ajouter un nouvel importateur...":
        new_importateur = st.text_input("Entrez le nom du nouvel importateur")
        add_importeur_button = st.button("Valider l'ajout de l'importateur")
        if add_importeur_button:
            if new_importateur.strip():
                try:
                    insert_importateur(new_importateur.strip())
                    st.success(f"Importateur '{new_importateur}' ajouté avec succès.")
                    importateurs_list = fetch_importateurs()  # Actualise la liste immédiatement
                except Exception as e:
                    st.error(f"Erreur lors de l'ajout de l'importateur : {e}")
            else:
                st.warning("Le nom de l'importateur ne peut pas être vide.")
            st.stop()  # Stoppe l'exécution après l'ajout pour recharger l'interface

    st.write(f"Importateur sélectionné : {selected_importateur}")

    # Quantité totale de conteneurs
    total_conteneurs = st.number_input("Quantité totale de conteneurs", min_value=1, step=1)
    bill = st.text_input("Numéro Bill")
    qte_cnts = st.number_input("Qté Conteneurs", min_value=1, step=1)

    # Sélection dynamique ou ajout pour le client
    clients_list = fetch_clients()
    selected_client = st.selectbox("Nom du client", clients_list + ["Ajouter un nouveau client..."])

    if selected_client == "Ajouter un nouveau client...":
        new_client = st.text_input("Entrez le nom du nouveau client")
        add_client_button = st.button("Ajouter le client")
        if add_client_button:
            if new_client.strip():
                try:
                    insert_client(new_client.strip())
                    st.success(f"Client '{new_client}' ajouté avec succès.")
                except Exception as e:
                    st.error(f"Erreur lors de l'ajout du client : {e}")
            else:
                st.warning("Le nom du client ne peut pas être vide.")
            st.stop()  # Stoppe l'exécution après l'ajout pour recharger l'interface

    # Sélection dynamique ou ajout pour l'agence
    agences_list = fetch_agences()
    selected_agence = st.selectbox("Nom de l'agence", agences_list + ["Ajouter une nouvelle agence..."])

    if selected_agence == "Ajouter une nouvelle agence...":
        new_agence = st.text_input("Entrez le nom de la nouvelle agence")
        add_agence_button = st.button("Ajouter l'agence")
        if add_agence_button:
            if new_agence.strip():
                try:
                    insert_agence(new_agence.strip())
                    st.success(f"Agence '{new_agence}' ajoutée avec succès.")
                except Exception as e:
                    st.error(f"Erreur lors de l'ajout de l'agence : {e}")
            else:
                st.warning("Le nom de l'agence ne peut pas être vide.")
            st.stop()  # Stoppe l'exécution après l'ajout pour recharger l'interface

    # Frais
    frais_doc = st.number_input("Frais DOC ($)", min_value=0.0, step=0.01)
    frais_cps = st.number_input("Frais CPS ($)", min_value=0.0, step=0.01)
    montant_total = frais_doc + (frais_cps * qte_cnts)
    st.write(f"Montant total pour le Bill : **${montant_total:.2f}**")

    # Bouton pour ajouter un nouvel arrivage
    if st.button("Ajouter l'arrivage et le Bill"):
        try:
            insert_arrivage(date_arrivage, selected_importateur, total_conteneurs, montant_total)
            st.success("Arrivage ajouté avec succès.")
        except Exception as e:
            st.error(f"Erreur lors de l'ajout : {e}")

# --- Gestion des déclarations validées ---
def manage_validated_declarations():
    st.header("Déclarations Validées")

    start_date = st.date_input("Date de début")
    end_date = st.date_input("Date de fin")

    importateurs_list = fetch_importateurs()
    selected_importateur = st.selectbox("Nom de l'importateur", importateurs_list)

    if st.button("Générer un rapport PDF"):
        try:
            validated_data = fetch_validated_data(start_date, end_date, selected_importateur)

            if not validated_data.empty:
                pdf_path = generate_validated_declarations_pdf(
                    start_date, end_date, selected_importateur, validated_data
                )
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        "Télécharger le rapport des déclarations validées",
                        data=pdf_file,
                        file_name=f"rapport_validations_{start_date}_to_{end_date}.pdf",
                        mime="application/pdf",
                    )
            else:
                st.warning("Aucune déclaration validée trouvée pour cette période.")
        except Exception as e:
            st.error(f"Erreur lors de la génération du rapport : {e}")

# --- Gestion des rapports ---
def download_reports():
    st.header("Télécharger un rapport")

    arrivages_df = fetch_arrivages()
    if not arrivages_df.empty:
        st.write("Arrivages disponibles :", arrivages_df)
        selected_date = st.selectbox("Sélectionnez une date d'arrivage", arrivages_df["date_arrivage"].unique())
        
        # Vérifiez si des importateurs sont disponibles
        importateurs_list = fetch_importateurs()
        if importateurs_list:
            selected_importateur = st.selectbox("Nom de l'importateur", importateurs_list)
        else:
            st.warning("Aucun importateur disponible.")
            return

        if st.button("Télécharger le PDF"):
            try:
                # Debug : Affichez les sélections
                st.write(f"Date sélectionnée : {selected_date}")
                st.write(f"Importateur sélectionné : {selected_importateur}")

                # Récupérer les données
                pdf_data = get_conteneurs(date=selected_date, importateur=selected_importateur)
                st.write("Données récupérées pour le PDF :", pdf_data)

                if not pdf_data.empty:
                    # Générer le PDF si des données existent
                    pdf_path = generate_pdf(selected_date, selected_importateur, pdf_data.values.tolist())
                    with open(pdf_path, "rb") as pdf_file:
                        st.download_button(
                            label="Télécharger le rapport PDF",
                            data=pdf_file,
                            file_name=f"rapport_{selected_importateur}_{selected_date}.pdf",
                            mime="application/pdf",
                        )
                else:
                    st.warning(f"Aucune donnée trouvée pour l'importateur '{selected_importateur}' à la date '{selected_date}'.")
            except Exception as e:
                st.error(f"Erreur lors de la génération ou du téléchargement du PDF : {e}")
    else:
        st.warning("Aucun arrivage disponible pour générer un rapport.")

# Fonction principale
if __name__ == "__main__":
    st.title("Dashboard JSL Distribution")
    menu = st.sidebar.selectbox("Menu", ["Gestion des arrivages", "Télécharger un rapport"])

    if menu == "Gestion des arrivages":
        manage_arrivages()
    elif menu == "Télécharger un rapport":
        download_reports()