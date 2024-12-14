import sqlite3

DATABASE_PATH = "data/jsl_distribution.db"

def insert_arrivage(date_arrivage, importateur, total_conteneurs, total_cout):
    query = '''
    INSERT INTO arrivages (date_arrivage, importateur, total_conteneurs, total_cout)
    VALUES (?, ?, ?, ?);
    '''
    _execute_query(query, (date_arrivage, importateur, total_conteneurs, total_cout))

def insert_client(client):
    query = '''
    INSERT OR IGNORE INTO clients (client)
    VALUES (?);
    '''
    _execute_query(query, (client,))

def insert_agence(agence):
    query = '''
    INSERT OR IGNORE INTO agences (agence)
    VALUES (?);
    '''
    _execute_query(query, (agence,))

def insert_importateur(importateur):
    query_check = "SELECT COUNT(*) FROM importateurs WHERE importateur = ?;"
    query_insert = "INSERT INTO importateurs (importateur) VALUES (?);"
    
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Vérifier si l'importateur existe déjà
        cursor.execute(query_check, (importateur,))
        if cursor.fetchone()[0] > 0:
            print(f"L'importateur '{importateur}' existe déjà.")
            return

        # Insérer le nouvel importateur
        cursor.execute(query_insert, (importateur,))
        conn.commit()
        print(f"Importateur '{importateur}' ajouté avec succès.")
    except sqlite3.Error as e:
        print(f"Erreur SQLite : {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def insert_conteneur(bill, qte_cnts, id_arrivage, id_client, frais_doc, frais_cps, montant_total, agence):
    query = '''
    INSERT INTO conteneurs (bill, qte_cnts, id_arrivage, id_client, frais_doc, frais_cps, montant_total, agence)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    '''
    _execute_query(query, (bill, qte_cnts, id_arrivage, id_client, frais_doc, frais_cps, montant_total, agence))

def update_arrivage(id_arrivage, date_arrivage, importateur, total_conteneurs, total_cout):
    query = '''
    UPDATE arrivages
    SET date_arrivage = ?, importateur = ?, total_conteneurs = ?, total_cout = ?
    WHERE id_arrivage = ?;
    '''
    _execute_query(query, (date_arrivage, importateur, total_conteneurs, total_cout, id_arrivage))

def delete_arrivage(id_arrivage):
    query = '''
    DELETE FROM arrivages WHERE id_arrivage = ?;
    '''
    _execute_query(query, (id_arrivage,))

def delete_conteneur(id_conteneur):
    query = '''
    DELETE FROM conteneurs WHERE id_conteneur = ?;
    '''
    _execute_query(query, (id_conteneur,))

def _execute_query(query, params):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Erreur d'intégrité : {e}")
        raise e
    except sqlite3.OperationalError as e:
        print(f"Erreur opérationnelle SQLite : {e}")
        raise e
    except sqlite3.Error as e:
        print(f"Erreur SQLite : {e}")
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
