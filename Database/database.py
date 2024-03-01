import sqlite3

def get_joka_table():
    """
    Récupère toutes les entrées de la table Joka dans la base de données.

    Sortie :
        tableJoka, de Type list, est la liste de tuples représentant chaque entrée de la table Joka.
    """
    conn = sqlite3.connect("Database/Database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Joka")
    tableJoka = cur.fetchall()
    conn.close()
    return tableJoka

def get_technique_table():
    """
    Récupère toutes les entrées de la table Technique dans la base de données.

    Sortie :
        tableTechnique, de Type list, est la liste de tuples représentant chaque entrée de la table Technique.
    """
    conn = sqlite3.connect("Database/Database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Technique")
    tableTechnique = list(cur.fetchall())
    conn.close()
    return tableTechnique

def get_graphe_table():
    """
    Récupère toutes les entrées de la table Graphe dans la base de données.

    Sortie :
        list : Liste de tuples représentant chaque entrée de la table Graphe.
    """
    conn = sqlite3.connect("Database/Database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Graphe")
    tableGraphe = list(cur.fetchall())
    conn.close()
    return tableGraphe

def get_jokas_by_location(location):
    """
    Récupère les identifiants des Jokas présents dans un lieu spécifique.

    Entrée :
        location, de Type str, est Le lieu à rechercher.

    Sortie :
        list : Liste des identifiants des Jokas présents dans le lieu donné.
    """
    conn = sqlite3.connect('Database/Database.db')
    c = conn.cursor()
    c.execute("SELECT ID_Joka FROM Apparition WHERE Lieu = ?", (location,))
    jokas = c.fetchall()
    conn.close()
    return [joka[0] for joka in jokas] if jokas else []

def get_joka_name_by_id(joka_id):
    """
    Récupère le nom d'un Joka en fonction de son identifiant.

    Entrée :
        joka_id, de Type int, est L'identifiant du Joka.

    Sortie :
        str : Le nom du Joka.
    """
    conn = sqlite3.connect('Database/Database.db')
    c = conn.cursor()
    c.execute("SELECT Nom FROM Joka WHERE ID_Joka = ?", (joka_id,))
    joka_name = c.fetchone()[0]
    conn.close()
    return joka_name

def get_joka_info_by_id(joka_id):
    """
    Récupère les informations d'un Joka en fonction de son identifiant.

    Entrée :
        joka_id, de Type int, est L'identifiant du Joka.

    Sortie :
        dict : Un dictionnaire contenant les informations du Joka (ID, Nom, Vie).
    """
    conn = sqlite3.connect("Database/Database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT ID_Joka, Nom, Vie FROM Joka WHERE ID_Joka = ?", (joka_id,))
    joka_info = cursor.fetchone()
    cursor.close()
    conn.close()
    if joka_info:
        return {
            "ID": joka_info[0],
            "Nom": joka_info[1],
            "Vie": joka_info[2]
        }
    else:
        return None
    
def get_jokas_by_status(status):
    """
    Récupère les noms des Jokas en fonction de leur statut.

    Entrée :
        status, de Type str, est Le statut des Jokas (capturé ("Oui") ou non ("Non")).

    Sortie :
        list : Liste des noms des Jokas correspondant au statut donné.
    """
    conn = sqlite3.connect("Database/Database.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT Joka.Nom FROM Joka INNER JOIN Statut ON Joka.ID_Joka = Statut.ID_Joka WHERE estCapturé = '{status}'")
    jokas = cursor.fetchall()
    cursor.close()
    conn.close()
    return [joka[0] for joka in jokas]

def get_joka_id_by_name(joka_name):
    """
    Récupère l'identifiant d'un Joka en fonction de son nom.

    Entrée :
        joka_name, de Type str, est Le nom du Joka.

    Sortie :
        id_joka, de Type int, est l'identifiant du Joka.
    """
    conn = sqlite3.connect("Database/Database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT ID_Joka FROM Joka WHERE Nom = ?", (joka_name,))
    id_joka = cursor.fetchone()
    cursor.close()
    conn.close()
    return id_joka

def get_puissance_technique(nom_technique, id_joka):
    """
    Récupère la puissance d'une technique pour un Joka donné.

    Entrée :
        nom_technique, de Type str, est Le nom de la technique.
        id_joka, de Type int, est L'identifiant du Joka.

    Sortie :
        puissance, de Type int, est la puissance de la technique.
    """
    conn = sqlite3.connect('Database/Database.db')
    curseur = conn.cursor()
    curseur.execute("""
        SELECT Puissance
        FROM Technique
        WHERE Nom = ?
    """, (nom_technique,))
    puissance = curseur.fetchone()[0]
    return puissance

def get_type_technique(nom_technique):
    """
    Récupère le type d'une technique.

    Entrée :
        nom_technique, de Type str, est Le nom de la technique.

    Sortie :
        type_technique, de Type str, est le type de la technique.
    """
    conn = sqlite3.connect('Database/Database.db')
    curseur = conn.cursor()
    curseur.execute("""
        SELECT Type
        FROM Technique
        WHERE Nom = ?
    """, (nom_technique,))
    type_technique = curseur.fetchone()[0]
    return type_technique

def get_techniques_disponibles(id_joka):
    """
    Récupère les techniques disponibles pour un Joka donné.

    Entrée :
        id_joka, de Type int, est L'identifiant du Joka.

    Sortie :
        list : Liste des noms des techniques disponibles pour le Joka.
    """
    conn = sqlite3.connect('Database/Database.db')
    curseur = conn.cursor()
    curseur.execute("""
        SELECT Technique.Nom
        FROM Technique
        INNER JOIN Association ON Technique.ID_Technique = Association.ID_Technique
        WHERE Association.ID_Joka = ?
    """, (id_joka,))
    techniques = curseur.fetchall()
    return [technique[0] for technique in techniques]

def get_nom_joka(id_joka):
    """
    Récupère le nom d'un Joka en fonction de son identifiant.

    Entrée :
        id_joka, de Type int, est L'identifiant du Joka.

    Sortie :
        nom, de Type str, est le nom du Joka.
    """
    conn = sqlite3.connect('Database/Database.db')
    curseur = conn.cursor()
    curseur.execute("SELECT Nom FROM Joka WHERE ID_Joka = ?", (id_joka,))
    nom = curseur.fetchone()[0]
    return nom

def get_vie_joka(id_joka):
    """
    Récupère le nombre de points de vie d'un Joka en fonction de son identifiant.

    Entrée :
        id_joka, de Type int, est L'identifiant du Joka.

    Sortie :
        vie, de Type int, est le nombre de points de vie du Joka.
    """
    conn = sqlite3.connect('Database/Database.db')
    curseur = conn.cursor()
    curseur.execute("SELECT Vie FROM Joka WHERE ID_Joka = ?", (id_joka,))
    vie = curseur.fetchone()[0]
    return vie

def update_statut(joka_id, est_capturé):
    """
    Met à jour le statut d'un Joka dans la base de données.

    Entrée :
        joka_id, de Type int, est L'identifiant du Joka à mettre à jour.
        est_capturé, de Type bool, est le nouveau statut du Joka (Oui pour Capturé, Non sinon).
    """
    conn = sqlite3.connect('Database/Database.db')
    curseur = conn.cursor()
    curseur.execute("UPDATE Statut SET estCapturé = ? WHERE ID_Joka = ?", (est_capturé, joka_id))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    # Test pour get_joka_table()
    assert len(get_joka_table()) == 10

    # Test pour get_technique_table()
    assert len(get_technique_table()) == 16

    # Test pour get_graphe_table()
    assert len(get_graphe_table()) == 5

    # Test pour get_jokas_by_location(location)
    assert len(get_jokas_by_location("Laboratoire")) == 1

    # Test pour get_joka_name_by_id(joka_id)
    assert get_joka_name_by_id(0) == "Savir"

    # Test pour get_joka_info_by_id(joka_id)
    assert get_joka_info_by_id(0) == {'ID': 0, 'Nom': 'Savir', 'Vie': 75}

    # Test pour get_jokas_by_status(status)
    assert len(get_jokas_by_status("Oui")) == 3

    # Test pour get_joka_id_by_name(joka_name)
    assert get_joka_id_by_name("Savir") == (0,)

    # Test pour get_puissance_technique(nom_technique, id_joka)
    assert get_puissance_technique("Coup de Poing", 0) == 10

    # Test pour get_type_technique(nom_technique)
    assert get_type_technique("Coup de Poing") == "Attaque"

    # Test pour get_techniques_disponibles(id_joka)
    assert len(get_techniques_disponibles(0)) == 3

    # Test pour get_nom_joka(id_joka)
    assert get_nom_joka(0) == "Savir"

    # Test pour get_vie_joka(id_joka)
    assert get_vie_joka(0) == 75

    # Test pour update_statut(joka_id, est_capturé)
    update_statut(0, "Non")
    assert get_jokas_by_status("Non")[0] == "Savir"
    update_statut(0, "Oui")