# Importation des Modules Graphiques
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import webbrowser

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
    """
    Affiche la Carte sur le Canvas.

    Entrée :
        map, de Type list, représente le Graphe à Afficher.
        canvas, de Type tkinter.Canvas, est le Canvas sur lequel la Carte va Être Dessinée.
    Sortie : Ajoute les Éléments Graphiques de la Carte sur le Canvas.
    """
    # Dictionnaire pour stocker les positions des nœuds sur la carte
    positions = {}
    # Dictionnaire pour stocker les identifiants des cercles dessinés sur le canevas
    circles = {}

    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            if cell:
                nom, voisins_str = cell
                voisins = voisins_str.strip('[]').replace('"', '').split(',')

                if nom.strip():
                    positions[nom] = (x, y)

                    # Détermination de la couleur de remplissage en fonction du nom du nœud
                    fill_color = "green" if nom == "Laboratoire" else "red" # On initialise le premier niveau
                    # Création d'un cercle sur le canevas
                    oval = canvas.create_oval(x*200+200, y*200+200, x*200+250, y*200+250, fill=fill_color)

                    circles[nom] = oval

                    # Dessiner des lignes pour relier les nœuds voisins
                    for voisin in voisins:
                        voisin = voisin.strip()
                        if voisin in positions:
                            voisin_x, voisin_y = positions[voisin]
                            canvas.create_line(x*200+225, y*200+225, voisin_x*200+225, voisin_y*200+225, fill="black")

                    # Ajout d'une balise avec le nom du nœud pour chaque cercle
                    canvas.itemconfig(oval, tags=nom)
                    # Liaison de l'événement de clic gauche à la fonction on_cercle_click avec des arguments spécifiques
                    canvas.tag_bind(nom, '<Button-1>', lambda e, nom=nom, voisins=voisins, positions=positions, circles=circles: on_cercle_click(nom, voisins, positions, circles))

def confirmer_changement_couleur(nom, canvas, circles, positions, voisins):
    """
    Change la Couleur du Cercle Cliqué et des Cercles des Niveaux Voisins.

    Entrée :
        nom, de Type str, est le Nom du Niveau Cliqué.
        canvas, de Type tkinter.Canvas, est le Canvas sur lequel la Carte est Dessinée.
        circles, de Type dict, est un Dictionnaire qui Contient les Identifiants des Cercles Dessinés sur le Canvas.
        positions, de Type dict, est un Dictionnaire qui Contient les Positions des Niveaux sur la Carte.
        voisins, de Type list, est la Liste des Voisins du Niveau Cliqué.
    Sortie : Change la Couleur des Cercles Cliqués et des Cercles des Niveaux Voisins.
    """
    # Vérification si un Joka Principal a été sélectionné
    if joka_principal is None:
        messagebox.showwarning("Attention", "Merci de Choisir un Joka Principal dans la Liste à Gauche avant de Lancer un Combat !")
    else:
        # Récupération des Jokas dans la zone sélectionnée
        jokas_ids = database.get_jokas_by_location(nom)
        jokas_names = [database.get_joka_name_by_id(joka_id) for joka_id in jokas_ids]

        confirmation_message = f"Joka(s) détecté(s) dans le secteur {nom}.\n\n"
        confirmation_message += "\n".join(jokas_names)
        confirmation_message += "\n\nS'y rendre ?"

        # Affichage d'une boîte de dialogue pour confirmer le déplacement vers la zone
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

            # Si le combat est réussi pour tous les jokas présents dans la zone
            if all(combat_results):
                # Changement de couleur pour le cercle sélectionné et les cercles voisins
                canvas.itemconfig(circle_id, fill="green")
                for voisin in voisins:
                    voisin = voisin.strip()
                    if voisin in positions and voisin in circles:
                        voisin_id = circles[voisin]
                        canvas.itemconfig(voisin_id, fill="green")
            else:
                messagebox.showinfo("Information", "Combat échoué. Impossible d'Explorer Plus Loin'")

def on_cercle_click(nom, voisins, positions, circles):
    """
    Gère l'événement lorsqu'un cercle est cliqué sur la carte.

    Entrée :
        nom, de Type str, est le nom du niveau cliqué.
        voisins, de Type list, est la liste des voisins du niveau cliqué.
        positions, de Type dict, est un dictionnaire contenant les positions des niveaux sur la carte.
        circles, de Type dict, est un dictionnaire contenant les identifiants des cercles dessinés sur le canvas.
    """
    if nom.strip() in circles:
        circle_id = circles[nom]
        fill_color = canvas.itemcget(circle_id, "fill")
        # Vérifier si le cercle peut être exploré en vérifiant sa couleur
        if fill_color == "green":
            # Confirmer le changement de couleur et déclencher les actions appropriées
            confirmer_changement_couleur(nom, canvas, circles, positions, voisins)
        else:
            messagebox.showinfo("Information", "Zone Inaccessible.\nMerci de Terminer les Précédentes")
    else:
        print(f"Nom Incorrect: {nom}")

root = tk.Tk()

def quitter():
    """
    Fonction pour quitter l'application après confirmation.
    """
    if messagebox.askokcancel("Quitter", "Êtes-vous sûr de vouloir Quitter ?"):
        root.destroy()

def open_database_link():
    """
    Fonction pour ouvrir le lien vers la base de données dans un navigateur web.
    """
    webbrowser.open("https://colab.research.google.com/drive/1ZjbpvETwnX6evFEP1EMoqe3I823bBU86?usp=sharing")

def show_about_window():
    """
    Fonction pour afficher la fenêtre "À Propos" avec les informations sur l'application.
    """
    about_window = tk.Toplevel(root)
    about_window.title("À Propos")

    logo_image = Image.open("Ressources/logo.png")
    logo_image = logo_image.resize((200, 200), Image.Resampling.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_image)

    about_window.logo_photo = logo_photo

    logo_label = tk.Label(about_window, image=logo_photo)
    logo_label.pack(pady=(10, 20))

    title_label = tk.Label(about_window, text="KaJo Capture", font=("Arial", 16, "bold"))
    title_label.pack()

    created_by_label = tk.Label(about_window, text="Créé par\nJosselin LE TALLEC\nKamal KANAAN", font=("Arial", 12))
    created_by_label.pack(pady=(10, 20))

    github_link_label = tk.Label(about_window, text="GitHub\n", font=("Arial", 12, "underline"), cursor="hand2")
    github_link_label.pack()
    github_link_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/J0ssel1n/KaJo-Capture"))

# Récupération de la largeur et de la hauteur de l'écran
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calcul de la largeur et de la hauteur de la fenêtre en fonction de la taille de l'écran
window_width = int(screen_width * 0.75)
window_height = int(screen_height * 0.75)

# Définition de la fenêtre en mode plein écran
root.attributes('-fullscreen', True)

# Définition du titre de la fenêtre principale
root.title("KaJo Capture")

# Création d'un conteneur de mise en page en utilisant un PanedWindow
paned_window = tk.PanedWindow(root, orient="horizontal", sashrelief="raised", sashwidth=15)
paned_window.pack(fill="both", expand=True)

# Création d'un cadre gauche pour afficher la liste des Jokas
left_frame = tk.Frame(paned_window)
paned_window.add(left_frame)

# Création d'un cadre droit pour afficher la carte du jeu
right_frame = tk.Frame(paned_window)
paned_window.add(right_frame)

# Configuration des tailles minimales des cadres gauche et droit dans le PanedWindow
paned_window.paneconfig(left_frame, minsize=window_width / 4)
paned_window.paneconfig(right_frame, minsize=window_width / 2)

# Création d'un widget Treeview pour afficher la liste des Jokas
tree = ttk.Treeview(left_frame)
tree["columns"]=("id","nom","vie")
tree.column("#0", width=0, stretch=False)
tree.column("id", width=100)
tree.column("nom", width=100)
tree.column("vie", width=100)
tree.heading("id", text="ID_Joka")
tree.heading("nom", text="Nom")
tree.heading("vie", text="Vie")

# Insertion des données des Jokas dans le Treeview à partir de la base de données
for row in database.get_joka_table():
    tree.insert("", "end", values=row)

# Affichage du Treeview dans le cadre gauche
tree.pack(fill='both', expand=True)

# Création d'une barre de menu
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)

# Ajout des options du menu avec leurs commandes associées
file_menu.add_command(label="À Propos", command=show_about_window)
file_menu.add_command(label="Télécharger Base de Données", command=open_database_link)
file_menu.add_command(label="Quitter", command=quitter)
menu_bar.add_cascade(label="Fichier", menu=file_menu)

# Configuration de la barre de menu pour la fenêtre principale
root.config(menu=menu_bar)

def afficher_details_joka(event):
    """
    Affiche les détails du Joka sélectionné dans la liste de gauche.

    Entrée :
        event : L'événement déclenché par un double clic sur un élément de la liste.
    """
    # Récupération de l'élément sélectionné dans le Treeview
    item = tree.selection()[0]
    joka_id = tree.item(item, "values")[0]

    # Récupération du nom, des informations, du statut et des techniques du Joka à partir de la base de données
    joka_name = database.get_joka_name_by_id(joka_id)
    joka_info = database.get_joka_info_by_id(joka_id)
    joka_status = database.get_jokas_by_status("Oui") if joka_name in database.get_jokas_by_status("Oui") else None
    joka_techniques = database.get_techniques_disponibles(joka_id)

    # Création d'un dictionnaire des techniques avec leur puissance
    techniques_puissance = {}
    for technique in joka_techniques:
        puissance = database.get_puissance_technique(technique, joka_id)
        techniques_puissance[technique] = puissance

    # Affichage des détails du Joka dans une fenêtre Toplevel
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

        # Gestion de l'affichage du statut de Joka Principal et du bouton pour le sélectionner
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
        # Affichage d'un avertissement si les détails du Joka ne sont pas trouvés dans la base de données
        messagebox.showwarning("Attention", "Détails du Joka Non Trouvés dans la Base de Données.")

def set_joka_principal(joka_id, joka_window):
    """
    Définit le Joka sélectionné comme Joka principal.

    Entrée :
        joka_id, de Type int, est l'identifiant du Joka sélectionné.
        joka_window : La fenêtre des détails du Joka.
    """
    global joka_principal
    joka_principal = joka_id
    joka_window.destroy()

tree.bind("<Double-1>", afficher_details_joka)

canvas = tk.Canvas(right_frame, width=800, height=800)
canvas.pack()

map = creer_map(database.get_graphe_table(), 5)
afficher_map(map, canvas)

root.mainloop()