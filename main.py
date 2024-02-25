import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import database

joka_principal = None

def choisir_joka_principal():
    root.withdraw()

    joka_principal_window = tk.Toplevel()
    joka_principal_window.title("Choisir le Joka Principal")
    
    window_width = 400
    window_height = 50
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    
    joka_principal_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    jokas = database.get_jokas_by_status("Oui")
    jokas_dropdown = ttk.Combobox(joka_principal_window, values=jokas)
    jokas_dropdown.pack()

    def valider_selection():
        global joka_principal
        joka_principal = jokas_dropdown.get()
        if joka_principal:
            joka_principal_window.destroy()
            root.deiconify()
        else:
            messagebox.showwarning("Attention", "Veuillez Sélectionner un Joka pour Commencer votre Service.")

    bouton_ok = tk.Button(joka_principal_window, text="OK", command=valider_selection)
    bouton_ok.pack()

    joka_principal_window.wait_window(joka_principal_window)

def generer_map(taille):
    return [[False for _ in range(taille)] for _ in range(taille)]

def inserer_niveau(map, position_x, position_y, nom, voisins):
    map[position_y][position_x] = (nom, voisins)

def creer_map(liste_niveaux, taille):
    map = generer_map(taille)
    for niveau in liste_niveaux:
        position_x, position_y, nom, voisins = niveau
        inserer_niveau(map, position_x, position_y, nom, voisins)
    return map

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
    jokas_ids = database.get_jokas_by_location(nom)
    jokas_names = [database.get_joka_name_by_id(joka_id) for joka_id in jokas_ids]
    
    confirmation_message = f"Joka(s) détecté(s) dans le secteur {nom}.\n\n"
    confirmation_message += "\n".join(jokas_names)
    confirmation_message += "\n\nS'y rendre ?"

    if messagebox.askyesno("Confirmation", confirmation_message):
        circle_id = circles[nom]
        canvas.itemconfig(circle_id, fill="green")
        for voisin in voisins:
            voisin = voisin.strip()
            if voisin in positions and voisin in circles:
                voisin_id = circles[voisin]
                canvas.itemconfig(voisin_id, fill="green")

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

choisir_joka_principal()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = int(screen_width * 0.75)
window_height = int(screen_height * 0.75)

x = (screen_width - window_width) / 2
y = (screen_height - window_height) / 2

root.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")

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

canvas = tk.Canvas(right_frame, width=800, height=800)
canvas.pack()

map = creer_map(database.get_graphe_table(), 5)
afficher_map(map, canvas)

root.mainloop()