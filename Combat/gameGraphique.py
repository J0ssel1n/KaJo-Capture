# Importation des Modules Graphiques
import tkinter as tk
from tkinter import ttk, messagebox

# Importation du Module se Chargeant de l'Aléatoire
import random

# Importation Bien Compliquée pour Importer les Fonction de ./Database/database.py dans ./Combat/gameGraphique.py
import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from Database.database import *

class CombatGUI:
    def __init__(self, parent, id_joka1, id_joka2):
        """
        Initialise l'interface graphique pour le combat de Jokas.

        Entrée :
            parent, de Type tk.Tk, est la Fenêtre parente de l'interface.
            id_joka1, de Type int, est l'Identifiant du premier Joka.
            id_joka2, de Type int, est l'Identifiant du deuxième Joka.
        """
        # Stockage de la fenêtre parente et initialisation de la variable de résultat
        self.parent = parent
        self.result = None
        self.parent.title("Combat de Jokas")  # Définition du titre de la fenêtre

        # Récupération de la taille de l'écran et calcul des coordonnées pour centrer la fenêtre
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        x = (screen_width - parent.winfo_reqwidth()) / 2
        y = (screen_height - parent.winfo_reqheight()) / 2
        parent.geometry("+%d+%d" % (x, y))

        # Stockage des identifiants et noms des Jokas ainsi que de leurs points de vie
        self.id_joka1 = id_joka1
        self.id_joka2 = id_joka2
        self.nom_joka1 = get_nom_joka(self.id_joka1)
        self.nom_joka2 = get_nom_joka(self.id_joka2)
        self.vie_joka1 = get_vie_joka(self.id_joka1)
        self.vie_joka2 = get_vie_joka(self.id_joka2)

        # Création des labels pour afficher les points de vie des Jokas
        self.vie_joka1_label = ttk.Label(parent, text=f"Vie {self.nom_joka1}: {self.vie_joka1}")
        self.vie_joka1_label.pack()
        self.vie_joka2_label = ttk.Label(parent, text=f"Vie {self.nom_joka2}: {self.vie_joka2}")
        self.vie_joka2_label.pack()

        # Récupération des techniques disponibles pour le premier Joka et création des éléments d'interface correspondants
        self.techniques_joka1 = get_techniques_disponibles(self.id_joka1)
        self.technique_label = ttk.Label(parent, text="Choisir une technique:")
        self.technique_label.pack()
        self.technique_choisie = tk.StringVar()
        self.technique_menu = ttk.OptionMenu(parent, self.technique_choisie, self.techniques_joka1[0], *self.techniques_joka1)
        self.technique_menu.pack()

        # Création du bouton de confirmation pour choisir une technique
        self.confirm_button = ttk.Button(parent, text="Confirmer la technique", command=self.confirmer_technique)
        self.confirm_button.pack()

    def confirmer_technique(self):
        """
        Confirme la Technique choisie et gère le Déroulement du Combat.
        """
        # Récupération de la technique choisie par le joueur et de sa puissance
        technique_choisie = self.technique_choisie.get()
        puissance_technique = get_puissance_technique(technique_choisie, self.id_joka1)

        # Application de la technique choisie par le joueur sur l'adversaire
        if get_type_technique(technique_choisie) == "Soin":
            self.appliquer_soin(self.id_joka1, puissance_technique)
            messagebox.showinfo("Mise à jour", f"{self.nom_joka1} utilise {technique_choisie} et regagne {puissance_technique} points de vie.")
        else:
            self.appliquer_technique(self.id_joka2, puissance_technique)
            messagebox.showinfo("Mise à jour", f"{self.nom_joka1} utilise {technique_choisie} et inflige {puissance_technique} points de dégâts à {self.nom_joka2}.")

        # Sélection aléatoire d'une technique pour l'adversaire et récupération de sa puissance
        technique_choisie_adverse = random.choice(get_techniques_disponibles(self.id_joka2))
        puissance_technique_adverse = get_puissance_technique(technique_choisie_adverse, self.id_joka2)
        
        # Application de la technique adverse sur le joueur
        if get_type_technique(technique_choisie_adverse) == "Soin":
            self.appliquer_soin(self.id_joka2, puissance_technique_adverse)
            messagebox.showinfo("Mise à jour", f"{self.nom_joka2} utilise {technique_choisie_adverse} et regagne {puissance_technique_adverse} points de vie.")
        else:
            self.appliquer_technique(self.id_joka1, puissance_technique_adverse)
            messagebox.showinfo("Mise à jour", f"{self.nom_joka2} utilise {technique_choisie_adverse} et inflige {puissance_technique_adverse} points de dégâts à {self.nom_joka1}.")

        # Mise à jour des labels affichant les points de vie
        self.vie_joka1_label.config(text=f"Vie {self.nom_joka1}: {self.vie_joka1}")
        self.vie_joka2_label.config(text=f"Vie {self.nom_joka2}: {self.vie_joka2}")

        # Vérification de la condition de fin du combat
        if self.vie_joka1 <= 0:
            # Affichage du vainqueur et arrêt de l'application
            messagebox.showinfo("Fin du combat", f"{self.nom_joka2} a gagné !")
            self.result = False
            self.parent.quit()
        
        elif self.vie_joka2 <= 0:
            # Affichage du vainqueur et possibilité de choisir le vainqueur comme Joka Principal
            messagebox.showinfo("Fin du combat", f"{self.nom_joka1} a gagné !")
            messagebox.showinfo("Enregistrement", f"{self.nom_joka2} peut maintenant être Choisi en tant que Joka Principal.")
            self.result = True
            self.parent.quit()

    def appliquer_technique(self, id_joka, puissance_technique):
        """
        Applique les dégâts d'une technique à un Joka.

        Entrée :
            id_joka, de Type int, est L'identifiant du Joka.
            puissance_technique, de Type int, est La puissance de la technique.
        """
        if id_joka == self.id_joka1:
            self.vie_joka1 = max(0, self.vie_joka1 - puissance_technique)
        else:
            self.vie_joka2 = max(0, self.vie_joka2 - puissance_technique)

    def appliquer_soin(self, id_joka, puissance_soin):
        """
        Applique les soins d'une technique à un Joka.

        Entrée :
            id_joka, de Type int, est L'identifiant du Joka.
            puissance_soin, de Type int, est la Puissance des soins.
        """
        if id_joka == self.id_joka1:
            vie_max = get_vie_joka(self.id_joka1)
            self.vie_joka1 = min(vie_max, self.vie_joka1 + puissance_soin)
        else:
            vie_max = get_vie_joka(self.id_joka2)
            self.vie_joka2 = min(vie_max, self.vie_joka2 + puissance_soin)

def Combat(ID_Joka1, ID_Joka2):
    """
    Lance le combat entre deux Jokas.

    Entrée :
        ID_Joka1, de Type int, est L'identifiant du premier Joka.
        ID_Joka2, de Type int, est L'identifiant du deuxième Joka.
    """
    root = tk.Tk()
    app = CombatGUI(root, ID_Joka1, ID_Joka2)
    root.mainloop()

if __name__ == "__main__":
    Combat(0, 1)