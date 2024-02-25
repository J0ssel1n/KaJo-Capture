import sqlite3
import random

class Combat:
    def __init__(self, id_joka1, id_joka2):
        self.id_joka1 = id_joka1
        self.id_joka2 = id_joka2
        self.conn = sqlite3.connect('Database.db')
        self.curseur = self.conn.cursor()

    def get_nom_joka(self, id_joka):
        self.curseur.execute("SELECT Nom FROM Joka WHERE ID_Joka = ?", (id_joka,))
        nom_joka = self.curseur.fetchone()[0]
        return nom_joka

    def get_vie_joka(self, nom_joka):
        self.curseur.execute("SELECT Vie FROM Joka WHERE Nom = ?", (nom_joka,))
        vie_joka = self.curseur.fetchone()[0]
        return vie_joka

    def get_attaques_disponibles(self, id_joka):
        self.curseur.execute("""
            SELECT Technique.Nom, Technique.Puissance, Technique.Type
            FROM Technique
            INNER JOIN Association ON Technique.ID_Technique = Association.ID_Technique
            WHERE Association.ID_Joka = ?
        """, (id_joka,))
        attaques = self.curseur.fetchall()
        return attaques

    def combat(self):
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
                print(f"\n{nom_joka2} choisit {attaque_choisie_joka2[0]} - Puissance: {attaque_choisie_joka2[1]} - Type: {attaque_choisie_joka2[2]} (automatique)")

            if attaque_choisie_joka1[2] == "Attaque":
                vie_joka2 -= attaque_choisie_joka1[1]
            elif attaque_choisie_joka1[2] == "Soin":
                if vie_joka1 < vie_max_joka1:
                    vie_joka1 = min(vie_max_joka1, vie_joka1 + attaque_choisie_joka1[1])

            if attaque_choisie_joka2[2] == "Attaque":
                vie_joka1 -= attaque_choisie_joka2[1]
            elif attaque_choisie_joka2[2] == "Soin":
                if vie_joka2 < vie_max_joka2:
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