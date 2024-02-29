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
            parent (tk.Tk): Fenêtre parente de l'interface.
            id_joka1 (int): Identifiant du premier Joka.
            id_joka2 (int): Identifiant du deuxième Joka.
        """
        self.parent = parent
        self.result = None
        self.parent.title("Combat de Jokas")
        
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()

        x = (screen_width - parent.winfo_reqwidth()) / 2
        y = (screen_height - parent.winfo_reqheight()) / 2

        parent.geometry("+%d+%d" % (x, y))

        self.id_joka1 = id_joka1
        self.id_joka2 = id_joka2

        self.nom_joka1 = get_nom_joka(self.id_joka1)
        self.nom_joka2 = get_nom_joka(self.id_joka2)

        self.vie_joka1 = get_vie_joka(self.id_joka1)
        self.vie_joka2 = get_vie_joka(self.id_joka2)

        self.vie_joka1_label = ttk.Label(parent, text=f"Vie {self.nom_joka1}: {self.vie_joka1}")
        self.vie_joka1_label.pack()

        self.vie_joka2_label = ttk.Label(parent, text=f"Vie {self.nom_joka2}: {self.vie_joka2}")
        self.vie_joka2_label.pack()

        self.techniques_joka1 = get_techniques_disponibles(self.id_joka1)

        self.technique_label = ttk.Label(parent, text="Choisir une technique:")
        self.technique_label.pack()

        self.technique_choisie = tk.StringVar()
        self.technique_menu = ttk.OptionMenu(parent, self.technique_choisie, self.techniques_joka1[0], *self.techniques_joka1)
        self.technique_menu.pack()

        self.confirm_button = ttk.Button(parent, text="Confirmer la technique", command=self.confirmer_technique)
        self.confirm_button.pack()

    def confirmer_technique(self):
        """
        Confirme la Technique choisie et gère le Déroulement du Combat.
        """
        technique_choisie = self.technique_choisie.get()
        puissance_technique = get_puissance_technique(technique_choisie, self.id_joka1)

        if get_type_technique(technique_choisie) == "Soin":
            self.appliquer_soin(self.id_joka1, puissance_technique)
            messagebox.showinfo("Mise à jour", f"{self.nom_joka1} utilise {technique_choisie} et regagne {puissance_technique} points de vie.")
        else:
            self.appliquer_technique(self.id_joka2, puissance_technique)
            messagebox.showinfo("Mise à jour", f"{self.nom_joka1} utilise {technique_choisie} et inflige {puissance_technique} points de dégâts à {self.nom_joka2}.")

        technique_choisie_adverse = random.choice(get_techniques_disponibles(self.id_joka2))
        puissance_technique_adverse = get_puissance_technique(technique_choisie_adverse, self.id_joka2)
        
        if get_type_technique(technique_choisie_adverse) == "Soin":
            self.appliquer_soin(self.id_joka2, puissance_technique_adverse)
            messagebox.showinfo("Mise à jour", f"{self.nom_joka2} utilise {technique_choisie_adverse} et regagne {puissance_technique_adverse} points de vie.")
        else:
            self.appliquer_technique(self.id_joka1, puissance_technique_adverse)
            messagebox.showinfo("Mise à jour", f"{self.nom_joka2} utilise {technique_choisie_adverse} et inflige {puissance_technique_adverse} points de dégâts à {self.nom_joka1}.")

        self.vie_joka1_label.config(text=f"Vie {self.nom_joka1}: {self.vie_joka1}")
        self.vie_joka2_label.config(text=f"Vie {self.nom_joka2}: {self.vie_joka2}")

        if self.vie_joka1 <= 0:
            messagebox.showinfo("Fin du combat", f"{self.nom_joka2} a gagné !")
            self.result = False
            self.parent.quit()
        
        elif self.vie_joka2 <= 0:
            messagebox.showinfo("Fin du combat", f"{self.nom_joka1} a gagné !")
            messagebox.showinfo("Enregistrement", f"{self.nom_joka2} peut maintenant être Choisi en tant que Joka Principal.")
            self.result = True
            self.parent.quit()

    def appliquer_technique(self, id_joka, puissance_technique):
        """
        Applique les dégâts d'une technique à un Joka.

        Entrée :
            id_joka (int): L'identifiant du Joka.
            puissance_technique (int): La puissance de la technique.
        """
        if id_joka == self.id_joka1:
            self.vie_joka1 = max(0, self.vie_joka1 - puissance_technique)
        else:
            self.vie_joka2 = max(0, self.vie_joka2 - puissance_technique)

    def appliquer_soin(self, id_joka, puissance_soin):
        """
        Applique les soins d'une technique à un Joka.

        Entrée :
            id_joka (int): L'identifiant du Joka.
            puissance_soin (int): La puissance des soins.
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
        ID_Joka1 (int): L'identifiant du premier Joka.
        ID_Joka2 (int): L'identifiant du deuxième Joka.
    """
    root = tk.Tk()
    app = CombatGUI(root, ID_Joka1, ID_Joka2)
    root.mainloop()

if __name__ == "__main__":
    Combat(0, 1)