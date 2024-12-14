import sqlite3
import pandas as pd

# Chemin vers la base de données
DATABASE_PATH = "data/jsl_distribution.db"

def _fetch_data(query, params=()):
    """
    Exécute une requête SQL et retourne les résultats sous forme de DataFrame.

    Args:
        query (str): Requête SQL à exécuter.
        params (tuple): Paramètres pour la requête SQL.

    Returns:
        pd.DataFrame: Résultats de la requête.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        df = pd.read_sql_query(query, conn, params=params)
    except sqlite3.Error as e:
        print(f"Erreur lors de l'exécution de la requête : {query} avec paramètres {params} : {e}")
        raise e
    finally:
        conn.close()
    return df

def get_conteneurs(date, importateur):
    """
    Récupère les conteneurs associés à une date et un importateur spécifiques.

    Args:
        date (str): Date d'arrivage (format YYYY-MM-DD).
        importateur (str): Nom de l'importateur.

    Returns:
        pd.DataFrame: Données des conteneurs.
    """
    # Afficher les valeurs des paramètres pour débogage
    print(f"Date sélectionnée : {date}")
    print(f"Importateur sélectionné : {importateur}")

    query = """
    SELECT 
        conteneurs.bill,
        conteneurs.qte_cnts,
        conteneurs.frais_doc,
        conteneurs.frais_cps,
        conteneurs.montant_total,
        conteneurs.agence
    FROM conteneurs
    JOIN arrivages ON conteneurs.id_arrivage = arrivages.id_arrivage
    WHERE arrivages.date_arrivage = ?
    AND arrivages.importateur = ?;
    """
    params = (date, importateur)
    return _fetch_data(query, params)

# Test avec des valeurs codées en dur pour la date et l'importateur
def test_get_conteneurs():
    date = "2024-12-14"  # Valeur codée en dur pour le test
    importateur = "JIMBO IMP. EXP."  # Valeur codée en dur pour le test

    # Appeler la fonction pour récupérer les conteneurs
    conteneurs = get_conteneurs(date, importateur)
    
    # Affichage des résultats
    print("Conteneurs récupérés :")
    print(conteneurs)

# Exécuter le test
test_get_conteneurs()
