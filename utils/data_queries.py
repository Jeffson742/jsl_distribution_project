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
    WHERE strftime('%Y-%m-%d', arrivages.date_arrivage) = ?
    AND arrivages.importateur = ?;
    """
    
    # Passer la date et l'importateur dans les paramètres
    params = (date, importateur)
    
    # Exécuter la requête et récupérer les données
    return _fetch_data(query, params)

def get_arrivages():
    """
    Récupère tous les arrivages depuis la base de données.

    Returns:
        pd.DataFrame: Données des arrivages.
    """
    query = "SELECT * FROM arrivages;"
    return _fetch_data(query)
def get_clients():
    """
    Récupère tous les clients uniques depuis la base de données.

    Returns:
        list: Liste des noms des clients.
    """
    query = "SELECT DISTINCT client FROM clients;"  # Exemple de requête SQL pour obtenir les clients
    df = _fetch_data(query)
    return df["client"].tolist() if not df.empty else []
def get_agences():
    """
    Récupère toutes les agences uniques depuis la base de données.

    Returns:
        list: Liste des noms des agences.
    """
    query = "SELECT DISTINCT agence FROM conteneurs WHERE agence IS NOT NULL;"
    df = _fetch_data(query)
    return df["agence"].tolist() if not df.empty else []
def get_importateurs():
    """
    Récupère tous les importateurs uniques depuis la base de données.

    Returns:
        list: Liste des noms des importateurs.
    """
    query = "SELECT DISTINCT importateur FROM importateurs;"  # Exemple de requête SQL pour obtenir les importateurs
    df = _fetch_data(query)
    return df["importateur"].tolist() if not df.empty else []
