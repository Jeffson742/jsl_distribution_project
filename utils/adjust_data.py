import sqlite3

DATABASE_PATH = "data/jsl_distribution.db"

def add_conteneur(numero_conteneur, id_arrivage, id_client, montant_unitaire, montant_frais, montant_total):
    """
    Ajoute un nouveau conteneur dans la table `conteneurs`.

    Args:
        numero_conteneur (int): Numéro unique du conteneur.
        id_arrivage (int): ID de l'arrivage associé.
        id_client (int): ID du client associé.
        montant_unitaire (float): Montant unitaire.
        montant_frais (float): Frais associés au conteneur.
        montant_total (float): Montant total (calculé ou donné directement).
    """
    query = '''
    INSERT INTO conteneurs (numero_conteneur, id_arrivage, id_client, montant_unitaire, montant_frais, montant_total)
    VALUES (?, ?, ?, ?, ?, ?);
    '''
    _execute_query(query, (numero_conteneur, id_arrivage, id_client, montant_unitaire, montant_frais, montant_total))


def update_conteneur_frais(numero_conteneur, nouveau_montant_frais):
    """
    Met à jour les frais pour un conteneur existant.

    Args:
        numero_conteneur (int): Numéro unique du conteneur à mettre à jour.
        nouveau_montant_frais (float): Nouveau montant des frais.
    """
    query = '''
    UPDATE conteneurs
    SET montant_frais = ?
    WHERE numero_conteneur = ?;
    '''
    _execute_query(query, (nouveau_montant_frais, numero_conteneur))


def delete_conteneur(numero_conteneur):
    """
    Supprime un conteneur de la table `conteneurs`.

    Args:
        numero_conteneur (int): Numéro unique du conteneur à supprimer.
    """
    query = '''
    DELETE FROM conteneurs
    WHERE numero_conteneur = ?;
    '''
    _execute_query(query, (numero_conteneur,))


def _execute_query(query, params):
    """
    Exécute une requête SQL avec gestion des erreurs.

    Args:
        query (str): La requête SQL à exécuter.
        params (tuple): Les paramètres de la requête.
    """
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erreur SQLite : {e}")
        raise e
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    # Exemple d'utilisation des fonctions
    try:
        print("Ajout d'un nouveau conteneur...")
        add_conteneur(397139, 1, 1, 1040.00, 500.00, 1540.00)

        print("Mise à jour des frais d'un conteneur...")
        update_conteneur_frais(352842, 550.00)

        print("Suppression d'un conteneur obsolète...")
        delete_conteneur(352855)

        print("Données ajustées avec succès.")
    except Exception as e:
        print(f"Erreur lors des ajustements des données : {e}")
