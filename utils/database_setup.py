import sqlite3

DATABASE_PATH = "data/jsl_distribution.db"

def create_tables():
    """
    Crée les tables nécessaires dans la base de données.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Table des importateurs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS importateurs (
            id_importateur INTEGER PRIMARY KEY AUTOINCREMENT,
            importateur TEXT NOT NULL UNIQUE
        );
    ''')

    # Table des clients
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id_client INTEGER PRIMARY KEY AUTOINCREMENT,
            client TEXT NOT NULL UNIQUE
        );
    ''')

    # Table des agences
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agences (
            id_agence INTEGER PRIMARY KEY AUTOINCREMENT,
            agence TEXT NOT NULL UNIQUE
        );
    ''')

    # Table des arrivages
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS arrivages (
            id_arrivage INTEGER PRIMARY KEY AUTOINCREMENT,
            date_arrivage TEXT NOT NULL,
            importateur TEXT NOT NULL,
            total_conteneurs INTEGER NOT NULL,
            total_cout REAL NOT NULL
        );
    ''')

    # Table des conteneurs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conteneurs (
            id_conteneur INTEGER PRIMARY KEY AUTOINCREMENT,
            bill TEXT NOT NULL,
            qte_cnts INTEGER NOT NULL,
            id_arrivage INTEGER NOT NULL,
            id_client INTEGER NOT NULL,
            frais_doc REAL NOT NULL,
            frais_cps REAL NOT NULL,
            montant_total REAL NOT NULL,
            agence TEXT NOT NULL,
            FOREIGN KEY (id_arrivage) REFERENCES arrivages (id_arrivage),
            FOREIGN KEY (id_client) REFERENCES clients (id_client)
        );
    ''')

    conn.commit()
    conn.close()
