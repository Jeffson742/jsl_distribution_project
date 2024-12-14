 Auteur : Jeffson Saint-louis
# Ce projet consiste a creer une base de donnees pour mon entreprise JSL DISTRIBUTION.
from fpdf import FPDF
import streamlit as st
import pandas as pd
from datetime import datetime
import altair as alt

# Titre de l'application
st.title("JSL Distribution : Votre partenaire de confiance pour un dédouanement rapide et efficace.")
st.write("Bienvenue dans notre application interactive 🎉")

# Formulaire d'entrée
st.header("Saisissez vos informations :")
numero = st.text_input("Numéro de déclaration")
conteneurs = st.number_input("Nombre de conteneurs", min_value=1, step=1)
importateur = st.text_input("Nom de l'importateur")

# Sélection des dates de la période
st.subheader("Sélectionnez la période")
start_date = st.date_input("Date de début de la période", value=datetime(2024, 10, 28).date())
end_date = st.date_input("Date de fin de la période", value=datetime(2024, 12, 15).date())

# Validation des dates
if start_date > end_date:
    st.error("La date de début doit être antérieure ou égale à la date de fin.")

# Soumission des données
if st.button("Soumettre"):
    if numero and importateur and start_date and end_date:
        # Préparer les données pour le CSV
        periode = f"{start_date.strftime('%d %B %Y')} - {end_date.strftime('%d %B %Y')}"
        data = {
            'Numéro': [numero],
            'Conteneurs': [conteneurs],
            'Importateur': [importateur],
            'Date': [datetime.now().strftime('%Y-%m-%d')],
            'Période': [periode]
        }
        df = pd.DataFrame(data)

        try:
            # Ajouter les données au fichier CSV existant
            df.to_csv('declarations.csv', mode='a', header=False, index=False)
        except FileNotFoundError:
            # Créer le fichier avec les en-têtes si inexistant
            df.to_csv('declarations.csv', index=False)

        st.success(f"Déclaration {numero} enregistrée avec succès pour {importateur} sous la période '{periode}'.")
    else:
        st.error("Veuillez remplir tous les champs.")

# Section : Déclarations enregistrées
st.header("Déclarations enregistrées")
try:
    # Lire les données depuis le fichier CSV
    df = pd.read_csv('declarations.csv', names=['Numéro', 'Conteneurs', 'Importateur', 'Date', 'Période'])
    st.dataframe(df)  # Afficher le tableau des données
except FileNotFoundError:
    st.write("Aucune déclaration enregistrée pour le moment.")

# Section : Générer des fichiers PDF par importateur et période
st.header("Générer des fichiers PDF par importateur et période")
try:
    if not df.empty:
        importateurs = df['Importateur'].unique()
        selected_importateur_pdf = st.selectbox("Choisissez un importateur pour le PDF :", importateurs)

        # Filtrer les données par importateur
        filtered_by_importer_pdf = df[df['Importateur'] == selected_importateur_pdf]

        # Générer un PDF pour l'importateur et la période sélectionnés
        if st.button(f"Générer un PDF pour {selected_importateur_pdf}"):
            class PDF(FPDF):
                def header(self):
                    # Ajouter une image en arrière-plan (logo)
                    self.image('logo_jsl_converted.png', x=0, y=0, w=210, h=297)  # Taille A4 en mm (portrait)

                    # Ajouter "JSL DISTRIBUTION" à la ligne 30 avec taille 30
                    self.set_font("Arial", "B", 30self.set_y(30)  # Positionner à la ligne 30
                    self.cell(0, 10, "JSL DISTRIBUTION", ln=True, align="C")

                    # Ajouter "Votre partenaire de confiance pour un dédouanement rapide et efficace." à la taille 14
                    self.set_font("Arial", size=14)  # Taille 14 pour cette ligne
                    self.cell(0, 10, "Votre partenaire de confiance pour un dédouanement rapide et efficace.", ln=True, align="C")
                    self.ln(20)

            pdf = PDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            # Statistiques globales (centrées)
            total_declarations = len(df)
            total_conteneurs = df['Conteneurs'].sum()

            # Positionner le texte au centre de la page
            pdf.set_y(60)  # Ajuster la position verticale pour centrer
            pdf.set_font("Arial", "B", 14)
            pdf.cell(200, 10, txt="Statistiques globales", ln=True, align="C")
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Total des déclarations : {total_declarations}", ln=True, align="C")
            pdf.cell(200, 10, txt=f"Total des conteneurs : {total_conteneurs}", ln=True, align="C")
            pdf.ln(20)

            # Ajouter un titre pour la section "Rapport des déclarations en douanes"
            pdf.set_font("Arial", "B", 14)
            pdf.cell(200, 10, txt="Rapport des déclarations en douanes", ln=True, align="C")
            pdf.ln(10)

            # Calculer la largeur totale du tableau
            total_width = 50 * 3  # Largeur totale pour 3 colonnes (Numéro, Conteneurs, Date)
            margin = (210 - total_width) / 2  # Calcule le décalage pour centrer le tableau horizontalement

            # Ajouter l'en-tête du tableau (centré)
            pdf.set_font("Arial", "B", 10)
            pdf.set_x(margin)  # Positionner horizontalement au centre
            pdf.cell(50, 10, "Numéro", 1, 0, "C")
            pdf.cell(50, 10, "Conteneurs", 1, 0, "C")
            pdf.cell(50, 10, "Date", 1, 1, "C")

            # Ajouter les données du tableau
            pdf.set_font("Arial", size=10)
            for index, row in filtered_by_importer_pdf.iterrows():
                pdf.set_x(margin)  # Repositionner horizontalement pour chaque ligne
                pdf.cell(50, 10, str(row['Numéro']), 1, 0, "C")
                pdf.cell(50, 10, str(row['Conteneurs']), 1, 0, "C")
                pdf.cell(50, 10, str(row['Date']), 1, 1, "C")

            # Sauvegarder le PDF
            pdf_output = f"declarations_{selected_importateur_pdf}_{start_date.strftime('%Y-%m-%d')}_to_{end_date.strftime('%Y-%m-%d')}.pdf"
            pdf.output(pdf_output)

            with open(pdf_output, "rb") as file:
                st.download_button(
                    label=f"Télécharger le PDF pour {selected_importateur_pdf}",
                    data=file,
                    file_name=pdf_output,
                    mime="application/pdf"
                )
except KeyError:
    st.write("Aucune donnée disponible pour générer des PDF."))