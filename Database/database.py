import sqlite3

def get_joka_table():
    conn = sqlite3.connect("Database/Database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Joka")
    tableJoka = cur.fetchall()
    conn.close()
    return tableJoka

def get_technique_table():
    conn = sqlite3.connect("Database/Database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Technique")
    tableTechnique = list(cur.fetchall())
    conn.close()
    return tableTechnique

def get_graphe_table():
    conn = sqlite3.connect("Database/Database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Graphe")
    tableGraphe = list(cur.fetchall())
    conn.close()
    return tableGraphe

def get_jokas_by_location(location):
    conn = sqlite3.connect('Database/Database.db')
    c = conn.cursor()
    c.execute("SELECT ID_Joka FROM Apparition WHERE Lieu = ?", (location,))
    jokas = c.fetchall()
    conn.close()
    return [joka[0] for joka in jokas] if jokas else []

def get_joka_name_by_id(joka_id):
    conn = sqlite3.connect('Database/Database.db')
    c = conn.cursor()
    c.execute("SELECT Nom FROM Joka WHERE ID_Joka = ?", (joka_id,))
    joka_name = c.fetchone()[0]
    conn.close()
    return joka_name

def get_joka_info_by_id(joka_id):
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
    conn = sqlite3.connect("Database/Database.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT Joka.Nom FROM Joka INNER JOIN Statut ON Joka.ID_Joka = Statut.ID_Joka WHERE estCapturé = '{status}'")
    jokas = cursor.fetchall()
    cursor.close()
    conn.close()
    return [joka[0] for joka in jokas]

def get_joka_id_by_name(joka_name):
    conn = sqlite3.connect("Database/Database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT ID_Joka FROM Joka WHERE Nom = ?", (joka_name,))
    id_joka = cursor.fetchone()
    cursor.close()
    conn.close()
    return id_joka

def get_puissance_technique(nom_technique, id_joka):
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
    conn = sqlite3.connect('Database/Database.db')
    curseur = conn.cursor()
    curseur.execute("SELECT Nom FROM Joka WHERE ID_Joka = ?", (id_joka,))
    nom = curseur.fetchone()[0]
    return nom

def get_vie_joka(id_joka):
    conn = sqlite3.connect('Database/Database.db')
    curseur = conn.cursor()
    curseur.execute("SELECT Vie FROM Joka WHERE ID_Joka = ?", (id_joka,))
    vie = curseur.fetchone()[0]
    return vie

def update_statut(joka_id, est_capturé):
    conn = sqlite3.connect('Database/Database.db')
    c = conn.cursor()
    c.execute("UPDATE Statut SET estCapturé = ? WHERE ID_Joka = ?", (est_capturé, joka_id))
    conn.commit()
    conn.close()