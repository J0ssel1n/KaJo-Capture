import sqlite3
import random

class Combat:
    def __init__(self, id_joka1, id_joka2):
        """
        Initialise une instance de Combat.

        Entrée :
            id_joka1, de Type int, est L'identifiant du premier Joka.
            id_joka2, de Type int, est L'identifiant du deuxième Joka.
        """
        self.id_joka1 = id_joka1
        self.id_joka2 = id_joka2
        self.conn = sqlite3.connect('Database/Database.db') # Connexion à la Base de Données
        self.curseur = self.conn.cursor() # Initialisation du curseur pour exécuter les requêtes SQL

    def get_nom_joka(self, id_joka):
        """
        Récupère le nom d'un Joka en fonction de son identifiant.

        Entrée :
            id_joka, de Type int, est L'identifiant du Joka.

        Sortie :
            str: Le nom du Joka.
        """
        self.curseur.execute("SELECT Nom FROM Joka WHERE ID_Joka = ?", (id_joka,))
        nom_joka = self.curseur.fetchone()[0]
        return nom_joka

    def get_vie_joka(self, nom_joka):
        """
        Récupère le nombre de points de vie d'un Joka en fonction de son nom.

        Entrée :
            nom_joka, de Type str, est Le nom du Joka.

        Sortie :
            int: Le nombre de points de vie du Joka.
        """
        self.curseur.execute("SELECT Vie FROM Joka WHERE Nom = ?", (nom_joka,))
        vie_joka = self.curseur.fetchone()[0]
        return vie_joka

    def get_attaques_disponibles(self, id_joka):
        """
        Récupère les attaques disponibles pour un Joka donné.

        Entrée :
            id_joka, de Type int, est L'identifiant du Joka.

        Sortie :
            list: Liste des attaques disponibles pour le Joka. Chaque attaque est un tuple (Nom, Puissance, Type).
        """
        self.curseur.execute("""
            SELECT Technique.Nom, Technique.Puissance, Technique.Type
            FROM Technique
            INNER JOIN Association ON Technique.ID_Technique = Association.ID_Technique
            WHERE Association.ID_Joka = ?
        """, (id_joka,))
        attaques = self.curseur.fetchall()
        return attaques

    def combat(self):
        """
        Lance le combat entre deux Jokas en utilisant leurs attaques respectives jusqu'à ce qu'un Joka perde tous ses points de vie.
        """
        nom_joka1 = self.get_nom_joka(self.id_joka1)
        nom_joka2 = self.get_nom_joka(self.id_joka2)
        vie_joka1 = self.get_vie_joka(nom_joka1)
        vie_joka2 = self.get_vie_joka(nom_joka2)
        vie_max_joka1 = vie_joka1
        vie_max_joka2 = vie_joka2

        print(f"\nCombat entre {nom_joka1} (Vie: {vie_joka1}) et {nom_joka2} (Vie: {vie_joka2})")

        attaques_joka1 = self.get_attaques_disponibles(self.id_joka1)
        attaques_joka2 = self.get_attaques_disponibles(self.id_joka2)

        while vie_joka1 > 0 and vie_joka2 > 0:
            print(f"\n{nom_joka1} peut utiliser les attaques suivantes:")
            # Utilisation de enumerate pour obtenir l'index et l'attaque correspondante dans la liste attaques_joka1
            # Enumerate permet de parcourir les éléments de la liste en leur associant un index
            # Cela permet d'afficher les attaques avec leur numéro de manière ordonnée
            for index, attaque in enumerate(attaques_joka1):
                print(f"{index + 1}. {attaque[0]} - Puissance: {attaque[1]} - Type: {attaque[2]}")

            choix_attaque_joka1 = int(input(f"\nChoisissez une attaque pour {nom_joka1} : "))
            attaque_choisie_joka1 = attaques_joka1[choix_attaque_joka1 - 1]
            print(f"\nVous avez choisi {attaque_choisie_joka1[0]} - Puissance: {attaque_choisie_joka1[1]} - Type: {attaque_choisie_joka1[2]}")

            if vie_joka2 < vie_max_joka2:
                attaque_choisie_joka2 = random.choice(attaques_joka2)
                print(f"\n{nom_joka2} choisit {attaque_choisie_joka2[0]} - Puissance: {attaque_choisie_joka2[1]} - Type: {attaque_choisie_joka2[2]}")
            else:
                attaque_choisie_joka2 = random.choice([attaque for attaque in attaques_joka2 if attaque[2] == "Attaque"])
                print(f"\n{nom_joka2} choisit {attaque_choisie_joka2[0]} - Puissance: {attaque_choisie_joka2[1]} - Type: {attaque_choisie_joka2[2]}")

            # Si la technique choisie par joka1 est une attaque
            if attaque_choisie_joka1[2] == "Attaque":
                # Réduire les points de vie du joka2 par la puissance de l'attaque
                vie_joka2 -= attaque_choisie_joka1[1]
            # Si la technique choisie par joka1 est un soin
            elif attaque_choisie_joka1[2] == "Soin":
                # Vérifier si les points de vie actuels du joka1 sont inférieurs à ses points de vie maximum
                if vie_joka1 < vie_max_joka1:
                    # Ajouter les points de vie de l'attaque au joka1, en prenant soin de ne pas dépasser ses points de vie maximum
                    vie_joka1 = min(vie_max_joka1, vie_joka1 + attaque_choisie_joka1[1])

            # Si la technique choisie par joka2 est une attaque
            if attaque_choisie_joka2[2] == "Attaque":
                # Réduire les points de vie du joka1 par la puissance de l'attaque
                vie_joka1 -= attaque_choisie_joka2[1]
            # Si l'attaque choisie par joka2 est un soin
            elif attaque_choisie_joka2[2] == "Soin":
                # Vérifier si les points de vie actuels du joka2 sont inférieurs à ses points de vie maximum
                if vie_joka2 < vie_max_joka2:
                    # Ajouter les points de vie de l'attaque au joka2, en prenant soin de ne pas dépasser ses points de vie maximum
                    vie_joka2 = min(vie_max_joka2, vie_joka2 + attaque_choisie_joka2[1])

            print(f"\nVie restante de {nom_joka1}: {vie_joka1}")
            print(f"Vie restante de {nom_joka2}: {vie_joka2}")

        if vie_joka1 <= 0:
            print(f"\n{nom_joka2} remporte le combat !")
        elif vie_joka2 <= 0:
            print(f"\n{nom_joka1} remporte le combat !")

        self.conn.close()

if __name__ == '__main__':
    combat_instance = Combat(0, 1)
    combat_instance.combat()