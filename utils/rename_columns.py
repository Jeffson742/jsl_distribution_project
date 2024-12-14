import sqlite3

def rename_columns():
    """
    Renomme les colonnes de la table 'conteneurs' en créant une nouvelle table,
    en copiant les données et en renommant la table.
    """
    try:
        # Connexion à la base SQLite
        conn = sqlite3.connect('jsl_distribution.db')
        cursor = conn.cursor()

        # 1. Créer une nouvelle table avec les noms modifiés
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS new_conteneurs (
            id_conteneur INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_conteneur TEXT NOT NULL,
            id_arrivage INTEGER NOT NULL,
            id_client INTEGER NOT NULL,
            frais_doc REAL NOT NULL,
            frais_cps REAL NOT NULL,
            montant_total REAL NOT NULL,
            FOREIGN KEY (id_arrivage) REFERENCES arrivages(id_arrivage),
            FOREIGN KEY (id_client) REFERENCES clients(id_client)
        );
        ''')

        # 2. Copier les données existantes vers la nouvelle table
        cursor.execute('''
        INSERT INTO new_conteneurs (id_conteneur, numero_conteneur, id_arrivage, id_client, frais_doc, frais_cps, montant_total)
        SELECT id_conteneur, numero_conteneur, id_arrivage, id_client, montant_unitaire, montant_frais, montant_total
        FROM conteneurs;
        ''')

        # 3. Supprimer l'ancienne table
        cursor.execute('DROP TABLE conteneurs;')

        # 4. Renommer la nouvelle table en 'conteneurs'
        cursor.execute('ALTER TABLE new_conteneurs RENAME TO conteneurs;')

        # Sauvegarder les modifications
        conn.commit()
        print("Les colonnes ont été renommées avec succès.")

    except sqlite3.Error as e:
        print(f"Erreur lors du renommage des colonnes : {e}")
    finally:
        if conn:
            conn.close()

# Appel de la fonction
rename_columns()
