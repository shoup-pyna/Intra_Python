
import json
import os

from models import Ingredient, Produit, Client, Etudiant, Personnel, Commande


class Sauvegarde:
    """Sa se pou n anrejistre done nap itilize yo"""

    FICHIER = "donnees.json"

    
    # SAUVEGARDE

    @staticmethod
    def sauvegarder(gestion):
        """Pou m pa pedi done m yo a chak redemarrage, fichier sa ap ede m ajoute yo (tout objet m yo tankou kliyan, engredyan, produits...) nan yon fichier json"""

        donnees = {
            "ingredients": [],
            "produits": [],
            "clients": [],
            "commandes": [],
            "historique": gestion.historique,

            "identifiants": {
                "ingredient": gestion.prochain_id_ingredient,
                "produit": gestion.prochain_id_produit,
                "client": gestion.prochain_id_client,
                "commande": gestion.prochain_id_commande
            }
        }

        # Anrejistreman pou engredyan yo
        for ingredient in gestion.ingredients:

            donnees["ingredients"].append({
                "id": ingredient.id,
                "nom": ingredient.nom,
                "quantite": ingredient.quantite,
                "unite": ingredient.unite,
                "seuil_min": ingredient.seuil_min
            })

        # Anrejistreman pou pwodui yo
        for produit in gestion.produits:

            donnees["produits"].append({
                "id": produit.id,
                "nom": produit.nom,
                "prix": produit.prix,
                "recette": produit.recette
            })

        # Anrejistreman kliyan yo
        for client in gestion.clients:

            if isinstance(client, Etudiant):
                type_client = "etudiant"

            elif isinstance(client, Personnel):
                type_client = "personnel"

            else:
                type_client = "client"

            donnees["clients"].append({
                "id": client.id,
                "nom": client.nom,
                "type": type_client
            })

        # Anrejistreman komand yo
        for commande in gestion.commandes:

            donnees["commandes"].append({
                "id": commande.id,
                "client_id": commande.client_id,
                "produits": commande.produits,
                "montant_total": commande.montant_total,
                "etat": commande.etat
            })

        # Pati sa ap ede m ekri done m yo nan fichier JSON an
        try:
            with open(
                Sauvegarde.FICHIER,
                "w",
                encoding="utf-8"
            ) as fichier:

                json.dump(
                    donnees,
                    fichier,
                    indent=4,
                    ensure_ascii=False
                )

            print("Sauvegarde effectuée avec succès.")

        except OSError as erreur:
            print(f"Erreur lors de la sauvegarde : {erreur}")

   
    # Pati sa ap ede n load done yo nan fichier JSON nan
   
    @staticmethod
    def charger(gestion):

        if not os.path.exists(Sauvegarde.FICHIER):
            print("Aucun fichier de sauvegarde trouvé.")
            return

        try:
            with open(
                Sauvegarde.FICHIER,
                "r",
                encoding="utf-8"
            ) as fichier:

                donnees = json.load(fichier)

        except json.JSONDecodeError:
            print("Erreur : le fichier JSON est corrompu.")
            print("Les données existantes n'ont pas été modifiées.")
            return

        except OSError as erreur:
            print(f"Erreur lors de la lecture : {erreur}")
            return

        try:
            # Nap itilize done JSON yo pou n ka kreye objet nou yo

            ingredients = []

            for element in donnees.get("ingredients", []):

                ingredient = Ingredient(
                    element["id"],
                    element["nom"],
                    element["quantite"],
                    element["unite"],
                    element["seuil_min"]
                )

                ingredients.append(ingredient)

            produits = []

            for element in donnees.get("produits", []):

                produit = Produit(
                    element["id"],
                    element["nom"],
                    element["prix"],
                    {
                        int(id_ingredient): quantite
                        for id_ingredient, quantite
                        in element["recette"].items()
                    }
                )

                produits.append(produit)

            clients = []

            for element in donnees.get("clients", []):

                if element["type"] == "etudiant":

                    client = Etudiant(
                        element["id"],
                        element["nom"]
                    )

                elif element["type"] == "personnel":

                    client = Personnel(
                        element["id"],
                        element["nom"]
                    )

                else:

                    client = Client(
                        element["id"],
                        element["nom"]
                    )

                clients.append(client)

            commandes = []

            for element in donnees.get("commandes", []):

                commande = Commande(
                    element["id"],
                    element["client_id"],
                    {
                        int(id_produit): quantite
                        for id_produit, quantite
                        in element["produits"].items()
                    },
                    element["montant_total"]
                )

                #Eta komand yo
                etat = element["etat"]

                if etat == "prête":
                    commande.changer_etat("prête")

                elif etat == "livrée":
                    commande.changer_etat("prête")
                    commande.changer_etat("livrée")

                elif etat == "annulée":
                    commande.changer_etat("annulée")

                commandes.append(commande)

            historique = donnees.get("historique", [])

            identifiants = donnees.get("identifiants", {})

            # Nap ranplase done yo le n fin rekontwi objet yo
           
            gestion.ingredients = ingredients
            gestion.produits = produits
            gestion.clients = clients
            gestion.commandes = commandes
            gestion.historique = historique

            gestion.prochain_id_ingredient = identifiants.get(
                "ingredient",
                max([i.id for i in ingredients], default=0) + 1
            )

            gestion.prochain_id_produit = identifiants.get(
                "produit",
                max([p.id for p in produits], default=0) + 1
            )

            gestion.prochain_id_client = identifiants.get(
                "client",
                max([c.id for c in clients], default=0) + 1
            )

            gestion.prochain_id_commande = identifiants.get(
                "commande",
                max([c.id for c in commandes], default=0) + 1
            )

            print("Données chargées avec succès.")

        except (KeyError, TypeError, ValueError) as erreur:

            print("Erreur : les données du fichier sont invalides.")
            print(f"Détail : {erreur}")
            print("Les données existantes n'ont pas été modifiées.")
