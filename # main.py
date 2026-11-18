# main.py

from gestion import GestionCafeteria


# Création de l'objet principal de gestion
cafeteria = GestionCafeteria()



# Fonksyon m pral itilize nan res kod la pou m evite fe anpil repetisyon


def lire_entier(message):
    """Demande un nombre entier à l'utilisateur."""
    while True:
        try:
            valeur = int(input(message))
            return valeur
        except ValueError:
            print("Erreur : veuillez entrer un nombre entier.")


def lire_nombre(message):
    """Demande un nombre positif ou nul."""
    while True:
        try:
            valeur = float(input(message))

            if valeur < 0:
                print("Erreur : le nombre doit être positif ou nul.")
            else:
                return valeur

        except ValueError:
            print("Erreur : veuillez entrer un nombre valide.")


def afficher_message(resultat):
    """Affiche le résultat d'une opération de gestion."""
    succes, message = resultat

    if succes:
        print(f"\nSUCCÈS : {message}")
    else:
        print(f"\nERREUR : {message}")



# Pati sa se pou m jere engredyan yo


def menu_ingredients():
    while True:
        print("\n===== GESTION DES INGREDIENTS =====")
        print("1. Ajouter un ingrédient")
        print("2. Afficher les ingrédients")
        print("3. Afficher les alertes de stock")
        print("0. Retour au menu principal")

        choix = input("Votre choix : ")

        if choix == "1":
            nom = input("Nom de l'ingrédient : ").strip()
            quantite = lire_nombre("Quantité disponible : ")
            unite = input("Unité (kg, L, unité...) : ").strip()
            seuil = lire_nombre("Seuil minimal de stock : ")

            resultat = cafeteria.ajouter_ingredient(
                nom, quantite, unite, seuil
            )
            afficher_message(resultat)

        elif choix == "2":
            cafeteria.afficher_ingredients()

        elif choix == "3":
            cafeteria.afficher_alertes_stock()

        elif choix == "0":
            break

        else:
            print("Choix invalide.")



# Pati sa jere pwodui yo (ajoute yo, afiche ak gad kisa k disponib)


def menu_produits():
    while True:
        print("\n===== GESTION DES PRODUITS =====")
        print("1. Ajouter un produit")
        print("2. Afficher les produits")
        print("3. Rechercher un produit")
        print("0. Retour au menu principal")

        choix = input("Votre choix : ")

        if choix == "1":
            nom = input("Nom du produit : ").strip()
            prix = lire_nombre("Prix de vente : ")

            recette = {}

            print("\nAjoutez les ingrédients de la recette.")
            print("Entrez 0 comme identifiant pour terminer.")

            while True:
                identifiant = lire_entier(
                    "Identifiant de l'ingrédient (0 pour terminer) : "
                )

                if identifiant == 0:
                    break

                quantite = lire_nombre(
                    "Quantité nécessaire pour ce produit : "
                )

                recette[identifiant] = quantite

            resultat = cafeteria.ajouter_produit(
                nom, prix, recette
            )
            afficher_message(resultat)

        elif choix == "2":
            cafeteria.afficher_produits()

        elif choix == "3":
            recherche = input("Nom du produit à rechercher : ").strip()
            cafeteria.rechercher_produit(recherche)

        elif choix == "0":
            break

        else:
            print("Choix invalide.")



# Pati jesyon kliyan yo


def menu_clients():
    while True:
        print("\n===== GESTION DES CLIENTS =====")
        print("1. Ajouter un client")
        print("2. Afficher les clients")
        print("0. Retour au menu principal")

        choix = input("Votre choix : ")

        if choix == "1":
            nom = input("Nom du client : ").strip()

            print("\nType de client :")
            print("1. Étudiant")
            print("2. Personnel")

            type_choisi = input("Votre choix : ")

            if type_choisi == "1":
                type_client = "etudiant"
            elif type_choisi == "2":
                type_client = "personnel"
            else:
                print("Type de client invalide.")
                continue

            resultat = cafeteria.ajouter_client(
                nom, type_client
            )
            afficher_message(resultat)

        elif choix == "2":
            cafeteria.afficher_clients()

        elif choix == "0":
            break

        else:
            print("Choix invalide.")



# Jere komand yo


def menu_commandes():
    while True:
        print("\n===== GESTION DES COMMANDES =====")
        print("1. Créer une commande")
        print("2. Afficher les commandes")
        print("3. Modifier l'état d'une commande")
        print("0. Retour au menu principal")

        choix = input("Votre choix : ")

        if choix == "1":
            cafeteria.afficher_clients()

            client_id = lire_entier(
                "\nIdentifiant du client : "
            )

            lignes = {}

            print("\nAjoutez les produits à la commande.")
            print("Entrez 0 comme identifiant pour terminer.")

            while True:
                produit_id = lire_entier(
                    "Identifiant du produit (0 pour terminer) : "
                )

                if produit_id == 0:
                    break

                quantite = lire_entier("Quantité commandée : ")

                if quantite <= 0:
                    print("La quantité doit être supérieure à zéro.")
                    continue

                lignes[produit_id] = (
                    lignes.get(produit_id, 0) + quantite
                )

            if not lignes:
                print("Commande vide : création annulée.")
                continue

            print("\nRésumé de la commande :")
            print("Client :", client_id)
            print("Produits :", lignes)

            confirmation = input(
                "Confirmer la commande ? (o/n) : "
            ).lower()

            if confirmation == "o":
                resultat = cafeteria.creer_commande(
                    client_id, lignes
                )
                afficher_message(resultat)
            else:
                print("Création de la commande annulée.")

        elif choix == "2":
            cafeteria.afficher_commandes()

        elif choix == "3":
            cafeteria.afficher_commandes()

            commande_id = lire_entier(
                "\nIdentifiant de la commande : "
            )

            print("\nNouvel état de la commande :")
            print("1. En préparation")
            print("2. Prête")
            print("3. Livrée")
            print("4. Annulée")

            etats = {
                "1": "en préparation",
                "2": "prête",
                "3": "livrée",
                "4": "annulée"
            }

            choix_etat = input("Votre choix : ")

            if choix_etat in etats:
                resultat = cafeteria.changer_etat_commande(
                    commande_id, etats[choix_etat]
                )
                afficher_message(resultat)
            else:
                print("État invalide.")

        elif choix == "0":
            break

        else:
            print("Choix invalide.")



# Statistik ak istorik


def menu_statistiques():
    while True:
        print("\n===== STATISTIQUES =====")
        print("1. Afficher les ventes")
        print("2. Afficher les produits les plus demandés")
        print("3. Afficher l'historique des opérations")
        print("0. Retour au menu principal")

        choix = input("Votre choix : ")

        if choix == "1":
            cafeteria.afficher_ventes()

        elif choix == "2":
            cafeteria.afficher_produits_populaires()

        elif choix == "3":
            cafeteria.afficher_historique()

        elif choix == "0":
            break

        else:
            print("Choix invalide.")


# Menu prensipal. M mete l an denye psk fo m te defini fonksyon l pral itilize pou al nan diferan menu yo anvan.


def menu_principal():
    while True:
        print("\n")
        print("=" * 45)
        print("       CAFÉTÉRIA UNIVERSITAIRE")
        print("=" * 45)

        print("1. Gestion des ingrédients")
        print("2. Gestion des produits et recettes")
        print("3. Gestion des clients")
        print("4. Gestion des commandes")
        print("5. Statistiques et historique")
        print("0. Quitter")

        choix = input("\nEntrez votre choix : ")

        if choix == "1":
            menu_ingredients()

        elif choix == "2":
            menu_produits()

        elif choix == "3":
            menu_clients()

        elif choix == "4":
            menu_commandes()

        elif choix == "5":
            menu_statistiques()

        elif choix == "0":
            print("\nMerci d'avoir utilisé notre application.")
            print("Au revoir !")
            break

        else:
            print("\nChoix invalide. Veuillez réessayer.")



# Starting point of the application


if __name__ == "__main__":
    try:
        menu_principal()

    except KeyboardInterrupt:
        print("\n\nArrêt du programme.")