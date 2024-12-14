from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
import tempfile


def generate_pdf(arrivage_date, importateur, data, logo_path="assets/logo_jsl_converted.png"):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf_path = temp_file.name

    # Préparer les styles
    styles = getSampleStyleSheet()
    centered_title_style = ParagraphStyle(
        name="CenteredTitle",
        fontSize=30,
        fontName="Helvetica-Oblique",
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
    centered_text_style = ParagraphStyle(
        name="CenteredText",
        fontSize=12,
        fontName="Helvetica",
        alignment=1,  # Centré
        textColor=colors.black,
        spaceAfter=15,
    )

    # Initialiser le document PDF
    pdf = SimpleDocTemplate(
        pdf_path, pagesize=landscape(letter), rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20
    )
    elements = []

    # Ajouter le logo
    try:
        logo = Image(logo_path, width=200, height=100)  # Ajustez les dimensions du logo
        logo.hAlign = "CENTER"
        elements.append(logo)
    except Exception as e:
        print(f"Erreur lors de l'ajout du logo : {e}")

    # Ajouter les sections centrées
    title = Paragraph("JSL DISTRIBUTION", centered_title_style)
    elements.append(title)

    slogan = Paragraph("Votre partenaire fiable pour des solutions de logistique et de dédouanement.", centered_subtitle_style)
    elements.append(slogan)

    report_info = Paragraph(
        f"Rapport pour l'importateur : {importateur}<br/>Date de l'arrivage : {arrivage_date}", centered_text_style
    )
    elements.append(report_info)

    # Espacer avant le tableau
    elements.append(Spacer(1, 20))

    # Créer le tableau
    table_data = [["Bill", "Qté Cnts", "Frais Doc", "Frais CPS", "Montant Total", "Client", "Agence"]] + data
    table = Table(table_data, colWidths=[90, 80, 80, 80, 100, 100, 100])

    # Définir les styles du tableau
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

    # Construire le document PDF
    pdf.build(elements)

    return pdf_path
