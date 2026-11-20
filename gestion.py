
from models import Ingredient, Produit, Client, Etudiant, Personnel, Commande
# Pati sa pemet mwen lye fichier gestion m nan ak sa k gen model yo. Se rezon sa k fe m te fe fichier model la anvan.
# Hiearchie sa ede m evite rantre nan yon boucle kote plizye nan fichier m yo ap chache done youn nan lot la

class GestionCafeteria:
    """Pati sa pral pemet m jere tout objet k nan programme mwen an tankou ingredyan yo, kliyan yo ak komand kap pase yo."""

    def __init__(self):
        self.ingredients = []
        self.produits = []
        self.clients = []
        self.commandes = []

        # M initialize tout compteur mwen yo a 1 pou m ka jere idantifyan pou yo chak par incrementation
        self.prochain_id_ingredient = 1
        self.prochain_id_produit = 1
        self.prochain_id_client = 1
        self.prochain_id_commande = 1

        # Sa se pou m ka stoke istorik transaction yo
        self.historique = []

    # HISTORIQUE
    
    def enregistrer_historique(self, operation):
        """Fonksyon sa pral ede m jere tout operasyon k gen nan kafeterya a"""
        self.historique.append(operation)

    def afficher_historique(self):
        print("\n===== HISTORIQUE =====")

        if not self.historique:
            print("Aucune opération enregistrée.")
            return

        for operation in self.historique:
            print(operation)

   
    # Pati sa se pou m ka jere tout operasyon k ka fet sou engredyan yo

    def trouver_ingredient(self, identifiant):
        """Sa ap pemet mwen jwenn engredyan yo apati idantifyan m te atribuye yo a"""
        for ingredient in self.ingredients:
            if ingredient.id == identifiant:
                return ingredient

        return None

    def ajouter_ingredient(self, nom, quantite, unite, seuil):
        """Fonksyon sa ap pemet m ajoute engredyan, map tou profite elimine tout ka erreur ki ka prezante yo"""

        if not nom.strip():
            raise ValueError("Le nom de l'ingrédient est obligatoire.")

        if quantite < 0:
            raise ValueError("La quantité ne peut pas être négative.")

        if seuil < 0:
            raise ValueError("Le seuil ne peut pas être négatif.")

        ingredient = Ingredient(
            self.prochain_id_ingredient,
            nom,
            quantite,
            unite,
            seuil
        )

        self.ingredients.append(ingredient)

        self.prochain_id_ingredient += 1

        self.enregistrer_historique(
            f"Ajout de l'ingrédient : {nom}"
        )

        print("Ingrédient ajouté avec succès.")

    def afficher_ingredients(self):
        """Pou n ka we tout engredyan ki disponib yo"""

        print("\n===== LISTE DES INGREDIENTS =====")

        if not self.ingredients:
            print("Aucun ingrédient disponible.")
            return

        for ingredient in self.ingredients:
            print(
                f"ID : {ingredient.id} | "
                f"Nom : {ingredient.nom} | "
                f"Stock : {ingredient.quantite} {ingredient.unite} | "
                f"Seuil : {ingredient.seuil_min}"
            )

    def afficher_alertes_stock(self):
        """Lap enpotan pou n konnen le yon pwodui insuffisant, fonksyon sa ap bay yon alerte"""

        print("\n===== ALERTES DE STOCK =====")

        alertes = [
            ingredient
            for ingredient in self.ingredients
            if ingredient.stock_faible()
        ]

        if not alertes:
            print("Aucune alerte. Tous les stocks sont suffisants.")
            return

        for ingredient in alertes:
            print(
                f"ALERTE : {ingredient.nom} - "
                f"Stock restant : {ingredient.quantite} "
                f"{ingredient.unite}"
            )

    
    # Jesyon pou pwodui yo (recherche, ajout, afichaj...)
    
    def trouver_produit(self, identifiant):
        """Recherche a partir de yon identifiant."""

        for produit in self.produits:
            if produit.id == identifiant:
                return produit

        return None

    def ajouter_produit(self, nom, prix, recette):
       

        if not nom.strip():
            raise ValueError("Le nom du produit est obligatoire.")

        if prix <= 0:
            raise ValueError("Le prix doit être supérieur à zéro.")

        if not recette:
            raise ValueError("La recette doit contenir des ingrédients.")

        # Nap verifye engredyan pou yon reset
        for id_ingredient, quantite in recette.items():

            ingredient = self.trouver_ingredient(id_ingredient)

            if ingredient is None:
                raise ValueError(
                    f"L'ingrédient ID {id_ingredient} n'existe pas."
                )

            if quantite <= 0:
                raise ValueError(
                    "Les quantités de la recette doivent être positives."
                )

        produit = Produit(
            self.prochain_id_produit,
            nom,
            prix,
            recette
        )

        self.produits.append(produit)

        self.prochain_id_produit += 1

        self.enregistrer_historique(
            f"Ajout du produit : {nom}"
        )

        print("Produit ajouté avec succès.")

    def afficher_produits(self):
        """Sa ap ede n we pwodui k disponib yo"""

        print("\n===== LISTE DES PRODUITS =====")

        if not self.produits:
            print("Aucun produit disponible.")
            return

        for produit in self.produits:
            print(
                f"ID : {produit.id} | "
                f"Nom : {produit.nom} | "
                f"Prix : {produit.prix}"
            )

    def rechercher_produit(self, recherche):
        """Sa ap ede n cheche engredyan yo ak non yo"""

        recherche = recherche.lower()

        resultats = [
            produit
            for produit in self.produits
            if recherche in produit.nom.lower()
        ]

        print("\n===== RESULTATS DE LA RECHERCHE =====")

        if not resultats:
            print("Aucun produit trouvé.")
            return

        for produit in resultats:
            print(
                f"ID : {produit.id} | "
                f"Nom : {produit.nom} | "
                f"Prix : {produit.prix}"
            )

    
    # Jesyon kliyan yo (recherche, ajout et affichage)
   

    def trouver_client(self, identifiant):
        """Pou n ka jwenn kliyan yo ak ID yo"""

        for client in self.clients:
            if client.id == identifiant:
                return client

        return None

    def ajouter_client(self, nom, type_client):
        """Sa se pou m ajoute kliyan, tout pandan map diferansye de eritaj nou te genyen yo: personnel ak etudyan """

        if not nom.strip():
            raise ValueError("Le nom du client est obligatoire.")

        if type_client == "etudiant":
            client = Etudiant(
                self.prochain_id_client,
                nom
            )

        elif type_client == "personnel":
            client = Personnel(
                self.prochain_id_client,
                nom
            )

        else:
            raise ValueError("Type de client invalide.")

        self.clients.append(client)

        self.prochain_id_client += 1

        self.enregistrer_historique(
            f"Ajout du client : {nom} ({type_client})"
        )

        print("Client ajouté avec succès.")

    def afficher_clients(self):
        

        print("\n===== LISTE DES CLIENTS =====")

        if not self.clients:
            print("Aucun client enregistré.")
            return

        for client in self.clients:
            print(
                f"ID : {client.id} | "
                f"Nom : {client.nom} | "
                f"Type : {client.type_client()}"
            )

   
    # Jere komand yo
   

    def creer_commande(self, client_id, lignes):
        """Pati sa se pou m ka pase yon komand apre m fin verifye tout pwodui ak stok yap bezwen an"""

        client = self.trouver_client(client_id)

        if client is None:
            raise ValueError("Client introuvable.")

        if not lignes:
            raise ValueError("La commande est vide.")

        # Kantite total engredyan nap bezwen
        besoins_totaux = {}

        # Pri anvan m aplike reduksyon an
        montant_brut = 0

        # Verifikasyon pwodui yo
        for id_produit, quantite in lignes.items():

            produit = self.trouver_produit(id_produit)

            if produit is None:
                raise ValueError(
                    f"Produit ID {id_produit} introuvable."
                )

            if quantite <= 0:
                raise ValueError(
                    "La quantité commandée doit être positive."
                )

            montant_brut += produit.prix * quantite

            # Calcul engredyan n bezwen yo
            for id_ingredient, besoin_unitaire in produit.recette.items():

                besoin_total = besoin_unitaire * quantite

                besoins_totaux[id_ingredient] = (
                    besoins_totaux.get(id_ingredient, 0)
                    + besoin_total
                )

        # Map verifye tout stock mwen AVAN m fe qq soit modifikasyon an 
        for id_ingredient, besoin in besoins_totaux.items():

            ingredient = self.trouver_ingredient(id_ingredient)

            if ingredient is None:
                raise ValueError(
                    f"Ingrédient ID {id_ingredient} introuvable."
                )

            if ingredient.quantite < besoin:
                raise ValueError(
                    f"Stock insuffisant pour {ingredient.nom}. "
                    f"Stock disponible : {ingredient.quantite} "
                    f"{ingredient.unite}. "
                    f"Quantité nécessaire : {besoin} "
                    f"{ingredient.unite}."
                )

        # Sa se pri apre reduction
        montant_final = client.calculer_prix(montant_brut)

        # Kounya m ka kreye komand mwen an
        commande = Commande(
            self.prochain_id_commande,
            client.id,
            lignes.copy(),
            montant_final
        )

        # Le tout bagay fin valide map retire sa m itilize yo nan stock la
        for id_ingredient, besoin in besoins_totaux.items():

            ingredient = self.trouver_ingredient(id_ingredient)

            ingredient.retirer_stock(besoin)

        self.commandes.append(commande)

        self.prochain_id_commande += 1

        self.enregistrer_historique(
            f"Création de la commande {commande.id} "
            f"pour le client {client.nom}. "
            f"Montant : {montant_final}"
        )

        print(
            f"Commande créée avec succès. "
            f"Montant total : {montant_final}"
        )

    def afficher_commandes(self):
        """Affiche toutes les commandes."""

        print("\n===== LISTE DES COMMANDES =====")

        if not self.commandes:
            print("Aucune commande enregistrée.")
            return

        for commande in self.commandes:

            client = self.trouver_client(commande.client_id)

            nom_client = (
                client.nom if client is not None
                else "Client inconnu"
            )

            print(
                f"Commande ID : {commande.id} | "
                f"Client : {nom_client} | "
                f"Montant : {commande.montant_total} | "
                f"État : {commande.etat}"
            )

    def trouver_commande(self, identifiant):
        

        for commande in self.commandes:
            if commande.id == identifiant:
                return commande

        return None

    def changer_etat_commande(self, commande_id, nouvel_etat):
        """Modifye eta komand yo."""

        commande = self.trouver_commande(commande_id)

        if commande is None:
            raise ValueError("Commande introuvable.")

        ancien_etat = commande.etat

        # Klas commande sa ede m verifye operasyon k otorize yo
        commande.changer_etat(nouvel_etat)

        # Si komand lan anile, map reyajoute engredyan yo nan stock la
        if nouvel_etat == "annulée":

            for id_produit, quantite in commande.produits.items():

                produit = self.trouver_produit(id_produit)

                if produit is None:
                    continue

                for id_ingredient, besoin_unitaire in produit.recette.items():

                    ingredient = self.trouver_ingredient(id_ingredient)

                    if ingredient is not None:

                        quantite_a_restituer = (
                            besoin_unitaire * quantite
                        )

                        ingredient.ajouter_stock(
                            quantite_a_restituer
                        )

        self.enregistrer_historique(
            f"Commande {commande.id} : "
            f"{ancien_etat} -> {nouvel_etat}"
        )

        print("État de la commande modifié avec succès.")

    
    # Statistik ak istorik
   

    def afficher_ventes(self):
        """Pou n kontrole lajan k rantre apati de komand ki te LIVRE yo."""

        print("\n===== STATISTIQUES DES VENTES =====")

        commandes_livrees = [
            commande
            for commande in self.commandes
            if commande.etat == "livrée"
        ]

        total_ventes = sum(
            commande.montant_total
            for commande in commandes_livrees
        )

        print(
            f"Nombre de commandes livrées : "
            f"{len(commandes_livrees)}"
        )

        print(
            f"Montant total des ventes : "
            f"{total_ventes:.2f}"
        )

    def afficher_produits_populaires(self):
        """Klasifikasyon sa fet sou enpotans kantite n te komande a."""

        print("\n===== PRODUITS POPULAIRES =====")

        if not self.produits:
            print("Aucun produit disponible.")
            return

        popularite = {}

        for produit in self.produits:
            popularite[produit.id] = 0

        for commande in self.commandes:

            if commande.etat == "annulée":
                continue

            for id_produit, quantite in commande.produits.items():

                if id_produit in popularite:
                    popularite[id_produit] += quantite

        classement = sorted(
            self.produits,
            key=lambda produit: popularite[produit.id],
            reverse=True
        )

        for produit in classement:

            print(
                f"{produit.nom} : "
                f"{popularite[produit.id]} vendu(s)"
            )
