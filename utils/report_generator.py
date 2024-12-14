import sqlite3
import pandas as pd
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image


DATABASE_PATH = "data/jsl_distribution.db"


def fetch_validated_data(start_date, end_date, importateur):
    """
    Récupère les déclarations validées depuis la base de données.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        query = '''
        SELECT 
            arrivages.importateur AS "IMPORTATEUR", 
            conteneurs.bill AS "No D'ENREGISTREMENT",
            conteneurs.qte_cnts AS "QTE CONT.",
            arrivages.date_arrivage AS "DATE VALIDÉ"
        FROM arrivages
        JOIN conteneurs ON arrivages.id_arrivage = conteneurs.id_arrivage
        WHERE arrivages.date_arrivage BETWEEN ? AND ?
        AND arrivages.importateur = ?;
        '''
        params = (start_date, end_date, importateur)
        data = pd.read_sql_query(query, conn, params=params)
        if data.empty:
            raise ValueError("Aucune donnée trouvée pour cette période et cet importateur.")
        return data
    except sqlite3.Error as e:
        print(f"Erreur SQLite : {e}")
        raise
    finally:
        conn.close()



def generate_validated_declarations_pdf(start_date, end_date, importateur, data, logo_path="assets/logo_jsl_converted.png"):
    """
    Génère un rapport PDF pour les déclarations validées.
    """
    from tempfile import NamedTemporaryFile

    temp_file = NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf_path = temp_file.name

    # Styles
    styles = getSampleStyleSheet()
    centered_title_style = ParagraphStyle(
        name="CenteredTitle",
        fontSize=30,
        fontName="Helvetica-Bold",
        alignment=1,  # Centré
        textColor=colors.black,
        spaceAfter=20,
    )
    centered_subtitle_style = ParagraphStyle(
        name="CenteredSubtitle",
        fontSize=14,
        fontName="Helvetica",
        alignment=1,  # Centré
        textColor=colors.grey,
        spaceAfter=10,
    )
    table_header_style = ParagraphStyle(
        name="TableHeader",
        fontSize=14,
        fontName="Helvetica-Bold",
        alignment=1,  # Centré
        textColor=colors.black,
        spaceAfter=15,
    )

    pdf = SimpleDocTemplate(
        pdf_path, pagesize=landscape(letter), rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20
    )
    elements = []

    # Logo
    try:
        logo = Image(logo_path, width=150, height=75)
        logo.hAlign = "CENTER"
        elements.append(logo)
    except Exception as e:
        print(f"Erreur lors de l'ajout du logo : {e}")

    # Titre et Informations
    title = Paragraph("JSL DISTRIBUTION", centered_title_style)
    elements.append(title)

    slogan = Paragraph("Votre partenaire fiable pour des solutions de logistique et de dédouanement.", centered_subtitle_style)
    elements.append(slogan)

    report_info = Paragraph(
        f"Rapport des Déclarations Validées<br/>Importateur : {importateur}<br/>Période : {start_date} à {end_date}",
        centered_subtitle_style,
    )
    elements.append(report_info)

    # Tableau
    elements.append(Spacer(1, 20))
    table_data = [["IMPORTATEUR", "No D'ENREGISTREMENT", "QTE CONT.", "DATE VALIDÉ"]] + data.values.tolist()
    table = Table(table_data, colWidths=[150, 150, 100, 150])

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 12),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
                ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
            ]
        )
    )
    elements.append(table)

    pdf.build(elements)

    return pdf_path
