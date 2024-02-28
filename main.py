# Importation des Modules Graphiques
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Importation du Gestionnaire de la Base de Données
import Database.database as database

# Importation de l'Interface Graphique de Combat
from Combat.gameGraphique import *

joka_principal = None # Variable Globale pour Stocker l'Identifiant du Joka Principal

def generer_map(taille):
    """
    Génère une Carte remplie de Cases Vides.

    Entrée : taille, de Type int, est le Nombre de Valeurs en Longueur et en Largeur de la Carte.
    Sortie : Une Liste de Tableau de Tableaux représentant une Matrice.
    """
    return [[False for _ in range(taille)] for _ in range(taille)]

def creer_map(liste_niveaux, taille):
    """
    Génère une Carte remplie de Valeurs sous Forme de Tuples.

    Entrée : 
        liste_niveaux, de Type list, est la Liste des Niveaux se Situant dans la Table Graphe de la Base de Données.
        taille, de Type int, est la Taille de la Carte qui va Être Générée (voir Fonction generer_map(taille)).
    Sortie : Retourne une Carte qui va Être Utilisé comme un Graphe.
    """
    map = generer_map(taille)
    for niveau in liste_niveaux:
        position_x, position_y, nom, voisins = niveau
        inserer_niveau(map, position_x, position_y, nom, voisins)
    return map

def inserer_niveau(map, position_x, position_y, nom, voisins):
    """
    Ajoute un Niveau dans le Graphe / dans la Carte.

    Entrée :
        map, de Type list, représente l'Ensemble du Graphe.
        position_x, de Type int, est la Position sur l'Axe X du Niveau sur le Graphe.
        position_y, de Type int, est la Position sur l'Axe Y du Niveau sur le Graphe.
        nom, de Type str, est le Nom du Niveau.
        voisins, de Type list, est la Liste des Voisins Connectés au Niveau en Cours de Création.
    Sortie : Mets à Jour la Carte map en y Ajoutant un Niveau.
    """
    map[position_y][position_x] = (nom, voisins)

def afficher_map(map, canvas):
    positions = {}
    circles = {}

    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            if cell:
                nom, voisins_str = cell
                voisins = voisins_str.strip('[]').replace('"', '').split(',')

                if nom.strip():
                    positions[nom] = (x, y)

                    fill_color = "green" if nom == "Laboratoire" else "red"
                    oval = canvas.create_oval(x*200+200, y*200+200, x*200+250, y*200+250, fill=fill_color)

                    circles[nom] = oval

                    for voisin in voisins:
                        voisin = voisin.strip()
                        if voisin in positions:
                            voisin_x, voisin_y = positions[voisin]
                            canvas.create_line(x*200+225, y*200+225, voisin_x*200+225, voisin_y*200+225, fill="black")

                    canvas.itemconfig(oval, tags=nom)

                    canvas.tag_bind(nom, '<Button-1>', lambda e, nom=nom, position=(x, y), voisins=voisins, positions=positions, circles=circles: on_cercle_click(nom, position, voisins, positions, circles))

def confirmer_changement_couleur(nom, canvas, circles, positions, voisins):
    if joka_principal is None:
        messagebox.showwarning("Attention", "Merci de Choisir un Joka Principal dans la Liste à Gauche avant de Lancer un Combat !")
    else:
        jokas_ids = database.get_jokas_by_location(nom)
        jokas_names = [database.get_joka_name_by_id(joka_id) for joka_id in jokas_ids]

        confirmation_message = f"Joka(s) détecté(s) dans le secteur {nom}.\n\n"
        confirmation_message += "\n".join(jokas_names)
        confirmation_message += "\n\nS'y rendre ?"

        if messagebox.askyesno("Confirmation", confirmation_message):
            circle_id = circles[nom]
            combat_results = []
            for joka_id in jokas_ids:
                root.withdraw()
                combat_window = tk.Toplevel()
                app = CombatGUI(combat_window, joka_principal, joka_id)
                combat_window.lift()
                combat_window.mainloop()
                combat_results.append(app.result)
                root.deiconify()
                combat_window.destroy()

                if app.result:
                    database.update_statut(joka_id, "Oui")

            if all(combat_results):
                canvas.itemconfig(circle_id, fill="green")
                for voisin in voisins:
                    voisin = voisin.strip()
                    if voisin in positions and voisin in circles:
                        voisin_id = circles[voisin]
                        canvas.itemconfig(voisin_id, fill="green")
            else:
                messagebox.showinfo("Information", "Combat échoué. Impossible d'Explorer Plus Loin'")

def on_cercle_click(nom, position, voisins, positions, circles):
    if nom.strip() in circles:
        circle_id = circles[nom]
        fill_color = canvas.itemcget(circle_id, "fill")
        if fill_color == "green":
            confirmer_changement_couleur(nom, canvas, circles, positions, voisins)
        else:
            messagebox.showinfo("Information", "Zone Inaccessible.\nMerci de Terminer les Précédentes")
    else:
        print(f"Nom Incorrect: {nom}")

root = tk.Tk()

def quitter():
    if messagebox.askokcancel("Quitter", "Êtes-vous sûr de vouloir Quitter ?"):
        root.destroy()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = int(screen_width * 0.75)
window_height = int(screen_height * 0.75)

root.attributes('-fullscreen', True)

root.title("KaJo Capture")

paned_window = tk.PanedWindow(root, orient="horizontal", sashrelief="raised", sashwidth=15)
paned_window.pack(fill="both", expand=True)

left_frame = tk.Frame(paned_window)
paned_window.add(left_frame)
right_frame = tk.Frame(paned_window)
paned_window.add(right_frame)

paned_window.paneconfig(left_frame, minsize=window_width / 4)
paned_window.paneconfig(right_frame, minsize=window_width / 2)

tree = ttk.Treeview(left_frame)
tree["columns"]=("id","nom","vie")
tree.column("#0", width=0, stretch=False)
tree.column("id", width=100)
tree.column("nom", width=100)
tree.column("vie", width=100)
tree.heading("id", text="ID_Joka")
tree.heading("nom", text="Nom")
tree.heading("vie", text="Vie")

for row in database.get_joka_table():
    tree.insert("", "end", values=row)

tree.pack(fill='both', expand=True)

menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Quitter", command=quitter)
menu_bar.add_cascade(label="Fichier", menu=file_menu)
root.config(menu=menu_bar)

def afficher_details_joka(event):
    item = tree.selection()[0]
    joka_id = tree.item(item, "values")[0]

    joka_name = database.get_joka_name_by_id(joka_id)
    joka_info = database.get_joka_info_by_id(joka_id)
    joka_status = database.get_jokas_by_status("Oui") if joka_name in database.get_jokas_by_status("Oui") else None
    joka_techniques = database.get_techniques_disponibles(joka_id)

    techniques_puissance = {}
    for technique in joka_techniques:
        puissance = database.get_puissance_technique(technique, joka_id)
        techniques_puissance[technique] = puissance

    if joka_name and joka_info:
        joka_window = tk.Toplevel()
        joka_window.title("Détails du Joka")

        label_nom = tk.Label(joka_window, text="Nom du Joka : " + joka_name)
        label_nom.pack()

        label_vie = tk.Label(joka_window, text="Vie du Joka : " + str(joka_info["Vie"]))
        label_vie.pack()

        label_statut = tk.Label(joka_window, text="Statut : " + ("Capturé" if joka_status else "Non Capturé"))
        label_statut.pack()

        techniques_label = tk.Label(joka_window, text="\nTechniques : ")
        techniques_label.pack()

        for technique, puissance in techniques_puissance.items():
            label_technique = tk.Label(joka_window, text=f"{technique} [{puissance}]")
            label_technique.pack()

        if joka_principal and joka_id == joka_principal[0]:
            label_principal = tk.Label(joka_window, text="\nJoka Principal : Oui")
            button_text = "Choisir en Joka Principal"
            button_selectionner = tk.Button(joka_window, text=button_text, state="disabled")
        elif joka_status:
            label_principal = tk.Label(joka_window, text="\nJoka Principal : Non")
            button_text = "Choisir en Joka Principal"
            button_selectionner = tk.Button(joka_window, text=button_text, command=lambda: set_joka_principal(joka_id, joka_window))
        else:
            label_principal = tk.Label(joka_window, text="Joka Principal : Non")
            button_text = "Choisir en Joka Principal"
            joka_id = None
            button_selectionner = tk.Button(joka_window, text=button_text, state="disabled")

        label_principal.pack()
        button_selectionner.pack()

    else:
        messagebox.showwarning("Attention", "Détails du Joka Non Trouvés dans la Base de Données.")

def set_joka_principal(joka_id, joka_window):
    global joka_principal
    joka_principal = joka_id
    joka_window.destroy()

tree.bind("<Double-1>", afficher_details_joka)

canvas = tk.Canvas(right_frame, width=800, height=800)
canvas.pack()

map = creer_map(database.get_graphe_table(), 5)
afficher_map(map, canvas)

root.mainloop()