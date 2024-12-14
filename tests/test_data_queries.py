from data_queries import (
    get_arrivages,
    get_clients,
    get_agences,
    get_importateurs,
    get_conteneurs,
    get_validated_declarations,
)

def run_tests():
    print("=== Test : Récupération des arrivages ===")
    try:
        arrivages = get_arrivages()
        print("Résultats des arrivages :", arrivages)
    except Exception as e:
        print("Erreur lors de la récupération des arrivages :", e)

    print("\n=== Test : Récupération des clients ===")
    try:
        clients = get_clients()
        print("Résultats des clients :", clients)
    except Exception as e:
        print("Erreur lors de la récupération des clients :", e)

    print("\n=== Test : Récupération des agences ===")
    try:
        agences = get_agences()
        print("Résultats des agences :", agences)
    except Exception as e:
        print("Erreur lors de la récupération des agences :", e)

    print("\n=== Test : Récupération des importateurs ===")
    try:
        importateurs = get_importateurs()
        print("Résultats des importateurs :", importateurs)
    except Exception as e:
        print("Erreur lors de la récupération des importateurs :", e)

    print("\n=== Test : Récupération des conteneurs pour une date et un importateur ===")
    try:
        date = "2024-12-13"
        importateur = "CARINA"
        conteneurs = get_conteneurs(date, importateur)
        print(f"Résultats des conteneurs pour la date {date} et l'importateur {importateur} :", conteneurs)
    except Exception as e:
        print("Erreur lors de la récupération des conteneurs :", e)

    print("\n=== Test : Récupération des déclarations validées ===")
    try:
        start_date = "2024-12-01"
        end_date = "2024-12-31"
        importateur = "CARINA"
        declarations = get_validated_declarations(start_date, end_date, importateur)
        print(f"Résultats des déclarations validées pour {importateur} entre {start_date} et {end_date} :", declarations)
    except Exception as e:
        print("Erreur lors de la récupération des déclarations validées :", e)

if __name__ == "__main__":
    run_tests()
