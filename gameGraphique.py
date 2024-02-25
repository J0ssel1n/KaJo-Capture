import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import random

class CombatGUI:
    def __init__(self, parent, id_joka1, id_joka2):
        self.parent = parent
        self.parent.title("Combat de Jokas")
        
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()

        x = (screen_width - parent.winfo_reqwidth()) / 2
        y = (screen_height - parent.winfo_reqheight()) / 2

        parent.geometry("+%d+%d" % (x, y))

        self.conn = sqlite3.connect('Database.db')
        self.curseur = self.conn.cursor()

        self.id_joka1 = id_joka1
        self.id_joka2 = id_joka2

        self.nom_joka1 = self.get_nom_joka(self.id_joka1)
        self.nom_joka2 = self.get_nom_joka(self.id_joka2)

        self.vie_joka1 = self.get_vie_joka(self.id_joka1)
        self.vie_joka2 = self.get_vie_joka(self.id_joka2)

        self.vie_joka1_label = ttk.Label(parent, text=f"Vie {self.nom_joka1}: {self.vie_joka1}")
        self.vie_joka1_label.pack()

        self.vie_joka2_label = ttk.Label(parent, text=f"Vie {self.nom_joka2}: {self.vie_joka2}")
        self.vie_joka2_label.pack()

        self.techniques_joka1 = self.get_techniques_disponibles(self.id_joka1)

        self.technique_label = ttk.Label(parent, text="Choisir une technique:")
        self.technique_label.pack()

        self.technique_choisie = tk.StringVar()
        self.technique_menu = ttk.OptionMenu(parent, self.technique_choisie, self.techniques_joka1[0], *self.techniques_joka1)
        self.technique_menu.pack()

        self.confirm_button = ttk.Button(parent, text="Confirmer la technique", command=self.confirmer_technique)
        self.confirm_button.pack()

    def get_nom_joka(self, id_joka):
        self.curseur.execute("SELECT Nom FROM Joka WHERE ID_Joka = ?", (id_joka,))
        nom = self.curseur.fetchone()[0]
        return nom

    def get_vie_joka(self, id_joka):
        self.curseur.execute("SELECT Vie FROM Joka WHERE ID_Joka = ?", (id_joka,))
        vie = self.curseur.fetchone()[0]
        return vie

    def get_techniques_disponibles(self, id_joka):
        self.curseur.execute("""
            SELECT Technique.Nom
            FROM Technique
            INNER JOIN Association ON Technique.ID_Technique = Association.ID_Technique
            WHERE Association.ID_Joka = ?
        """, (id_joka,))
        techniques = self.curseur.fetchall()
        return [technique[0] for technique in techniques]

    def confirmer_technique(self):
        technique_choisie = self.technique_choisie.get()
        puissance_technique = self.get_puissance_technique(technique_choisie, self.id_joka1)

        if self.get_type_technique(technique_choisie) == "Soin":
            self.appliquer_soin(self.id_joka1, puissance_technique)
            messagebox.showinfo("Mise à jour", f"{self.nom_joka1} utilise {technique_choisie} et regagne {puissance_technique} points de vie.")
        else:
            self.appliquer_technique(self.id_joka2, puissance_technique)
            messagebox.showinfo("Mise à jour", f"{self.nom_joka1} utilise {technique_choisie} et inflige {puissance_technique} points de dégâts à {self.nom_joka2}.")

        technique_choisie_adverse = random.choice(self.get_techniques_disponibles(self.id_joka2))
        puissance_technique_adverse = self.get_puissance_technique(technique_choisie_adverse, self.id_joka2)
        
        if self.get_type_technique(technique_choisie_adverse) == "Soin":
            self.appliquer_soin(self.id_joka2, puissance_technique_adverse)
            messagebox.showinfo("Mise à jour", f"{self.nom_joka2} utilise {technique_choisie_adverse} et regagne {puissance_technique_adverse} points de vie.")
        else:
            self.appliquer_technique(self.id_joka1, puissance_technique_adverse)
            messagebox.showinfo("Mise à jour", f"{self.nom_joka2} utilise {technique_choisie_adverse} et inflige {puissance_technique_adverse} points de dégâts à {self.nom_joka1}.")

        self.vie_joka1_label.config(text=f"Vie {self.nom_joka1}: {self.vie_joka1}")
        self.vie_joka2_label.config(text=f"Vie {self.nom_joka2}: {self.vie_joka2}")

        if self.vie_joka1 <= 0:
            messagebox.showinfo("Fin du combat", f"{self.nom_joka2} a gagné !")
            self.parent.quit()
            return False
        
        elif self.vie_joka2 <= 0:
            messagebox.showinfo("Fin du combat", f"{self.nom_joka1} a gagné !")
            self.parent.quit()
            return True

    def get_puissance_technique(self, nom_technique, id_joka):
        self.curseur.execute("""
            SELECT Puissance
            FROM Technique
            WHERE Nom = ?
        """, (nom_technique,))
        puissance = self.curseur.fetchone()[0]
        return puissance

    def get_type_technique(self, nom_technique):
        self.curseur.execute("""
            SELECT Type
            FROM Technique
            WHERE Nom = ?
        """, (nom_technique,))
        type_technique = self.curseur.fetchone()[0]
        return type_technique

    def appliquer_technique(self, id_joka, puissance_technique):
        self.curseur.execute("SELECT Vie FROM Joka WHERE ID_Joka = ?", (id_joka,))

        if id_joka == self.id_joka1:
            self.vie_joka1 = max(0, self.vie_joka1 - puissance_technique)
        else:
            self.vie_joka2 = max(0, self.vie_joka2 - puissance_technique)

    def appliquer_soin(self, id_joka, puissance_soin):
        if id_joka == self.id_joka1:
            vie_max = self.get_vie_joka(self.id_joka1)
            self.vie_joka1 = min(vie_max, self.vie_joka1 + puissance_soin)
        else:
            vie_max = self.get_vie_joka(self.id_joka2)
            self.vie_joka2 = min(vie_max, self.vie_joka2 + puissance_soin)

def Combat(ID_Joka1, ID_Joka2):
    root = tk.Tk()
    app = CombatGUI(root, ID_Joka1, ID_Joka2)
    root.mainloop()

if __name__ == "__main__":
    Combat(0, 1)