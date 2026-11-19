
# Map defini klas sa pou engredyan yo, li gen tout karakteristik m pral pran an kont yo tankou kantite, non ak inite  l ladan l lan

class Ingredient:
    """Li reprezante yon engredyan m pral itilize pou m fon reset."""

    def __init__(self, identifiant, nom, quantite, unite, seuil_min):
        self.__id = identifiant
        self.__nom = nom
        self.__quantite = quantite
        self.__unite = unite
        self.__seuil_min = seuil_min

    # M defini getter sa yo pou m ka rekipere valeur atribut yo san m pa deranje klas la 

    @property
    def id(self):
        return self.__id

    @property
    def nom(self):
        return self.__nom

    @property
    def quantite(self):
        return self.__quantite

    @property
    def unite(self):
        return self.__unite

    @property
    def seuil_min(self):
        return self.__seuil_min

    # M defini metod (fonksyon k asosye ak yon klas oswa yon objet) ki pral ede m jere stock yo

    def ajouter_stock(self, quantite):
       
        if quantite <= 0:
            return False, "M bezwen kantite yo pozitif."

        self.__quantite += quantite
        return True, 

    def retirer_stock(self, quantite):
      
        if quantite <= 0:
            return False, 

        if quantite > self.__quantite:
            return False, "Pa gen ase nan stock la"

        self.__quantite -= quantite
        return True, 

    def stock_faible(self):
        """M pa vle stock mwen vid, m defini yon seuil minimal"""

        return self.__quantite <= self.__seuil_min

    def __str__(self):
        return (
            f"[{self.__id}] {self.__nom} : "
            f"{self.__quantite} {self.__unite}"
        )


# Sa se klas pwodui m yo

class Produit:

    def __init__(self, identifiant, nom, prix, recette):
        self.__id = identifiant
        self.__nom = nom
        self.__prix = prix

        # Lap paret sou fom yon Dictionnaire :
        self.__recette = recette.copy()


    @property
    def id(self):
        return self.__id

    @property
    def nom(self):
        return self.__nom

    @property
    def prix(self):
        return self.__prix

    @property
    def recette(self):
        return self.__recette.copy()

    # --------Map defini metod pou m travay sou klas pwodui a --------

    def modifier_prix(self, nouveau_prix):
    
        if nouveau_prix < 0:
            return False, 

        self.__prix = nouveau_prix
        return True, 

    def afficher_recette(self):
        
        print(f"\nRecette de {self.__nom} :")

        if not self.__recette:
            print("Aucun ingrédient enregistré.")
            return

        for ingredient_id, quantite in self.__recette.items():
            print(
                f"Ingredient ID {ingredient_id} : "
                f"{quantite} nécessaire(s)"
            )

    def __str__(self):
        return (
            f"[{self.__id}] {self.__nom} - "
            f"{self.__prix:.2f}"
        )



# Sa se klas kliyan yo

class Client:

    def __init__(self, identifiant, nom):
        self.__id = identifiant
        self.__nom = nom

    @property
    def id(self):
        return self.__id

    @property
    def nom(self):
        return self.__nom

    def taux_reduction(self):
        """Tarif sa yo jus normal pou yon kliyan lamda"""

        return 0.0

    def calculer_prix(self, montant):
        
        reduction = montant * self.taux_reduction()
        return montant - reduction

    def type_client(self):
        return "Client"

    def __str__(self):
        return f"[{self.__id}] {self.__nom} ({self.type_client()})"



# Klas etidyan sa se yon heritage de klas mere la ki se kliyan. Li gen yon tarif spesyal rabais 10%


class Etudiant(Client):
    
    REDUCTION = 0.10  

    def __init__(self, identifiant, nom):
        super().__init__(identifiant, nom)

    def taux_reduction(self):
        return self.REDUCTION

    def type_client(self):
        return "Étudiant"



# M met yon pri spesyal tou pou moun kap travay anndan an, yon rabais 5%


class Personnel(Client):
    

    REDUCTION = 0.05  

    def __init__(self, identifiant, nom):
        super().__init__(identifiant, nom)

    def taux_reduction(self):
        return self.REDUCTION

    def type_client(self):
        return "Personnel"



# Klas sa konsene komand yo, nan ki stad yo ye ak tout operasyon n ka fe sou yo


class Commande:
    """Représente une commande passée par un client."""

    ETATS = [
        "en préparation",
        "prête",
        "livrée",
        "annulée"
    ]

    def __init__(
        self,
        identifiant,
        client_id,
        produits,
        montant_total
    ):
        self.__id = identifiant
        self.__client_id = client_id

        # Dictionnaire :
        # {produit_id: quantite}
        self.__produits = produits.copy()

        self.__montant_total = montant_total
        self.__etat = "en préparation"


    @property
    def id(self):
        return self.__id

    @property
    def client_id(self):
        return self.__client_id

    @property
    def produits(self):
        return self.__produits.copy()

    @property
    def montant_total(self):
        return self.__montant_total

    @property
    def etat(self):
        return self.__etat

    # -------- Méthodes --------

    def changer_etat(self, nouvel_etat):

        if nouvel_etat not in self.ETATS:
            return False, "Pou m evite eta envalid yo"

        if self.__etat == "annulée":
            return False, 

        if self.__etat == "livrée":
            return False, "M pa ka modifye sa m fin ba w la"
        
        if nouvel_etat == "en préparation":
            return False,  

        if nouvel_etat == "annulée":
            self.__etat = nouvel_etat
            return True, "komand lan ap anile"

        if self.__etat == "en préparation":
            if nouvel_etat in ["prête", "annulée"]:
                self.__etat = nouvel_etat
                return True, 

        if self.__etat == "prête":
            if nouvel_etat == "livrée":
                self.__etat = nouvel_etat
                return True, 

        return False, "Le sa w pa ka chanje eta"

    def __str__(self):
        return (
            f"Commande [{self.__id}] | "
            f"Client [{self.__client_id}] | "
            f"Total : {self.__montant_total:.2f} | "
            f"État : {self.__etat}"
        )
