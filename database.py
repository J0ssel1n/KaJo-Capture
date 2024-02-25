import sqlite3

def get_joka_table():
    conn = sqlite3.connect("Database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Joka")
    tableJoka = cur.fetchall()
    conn.close()
    return tableJoka

def get_technique_table():
    conn = sqlite3.connect("Database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Technique")
    tableTechnique = list(cur.fetchall())
    conn.close()
    return tableTechnique

def get_graphe_table():
    conn = sqlite3.connect("Database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Graphe")
    tableGraphe = list(cur.fetchall())
    conn.close()
    return tableGraphe

def get_jokas_by_location(location):
    conn = sqlite3.connect('Database.db')
    c = conn.cursor()
    c.execute("SELECT ID_Joka FROM Apparition WHERE Lieu = ?", (location,))
    jokas = c.fetchall()
    conn.close()
    return [joka[0] for joka in jokas] if jokas else []

def get_joka_name_by_id(joka_id):
    conn = sqlite3.connect('Database.db')
    c = conn.cursor()
    c.execute("SELECT Nom FROM Joka WHERE ID_Joka = ?", (joka_id,))
    joka_name = c.fetchone()[0]
    conn.close()
    return joka_name

def get_joka_info_by_id(joka_id):
    conn = sqlite3.connect("Database.db")
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
    conn = sqlite3.connect("Database.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT Joka.Nom FROM Joka INNER JOIN Statut ON Joka.ID_Joka = Statut.ID_Joka WHERE estCapturé = '{status}'")
    jokas = cursor.fetchall()
    return [joka[0] for joka in jokas]

def get_type_attaque(self, nom_attaque, id_joka):
    self.curseur.execute("""
        SELECT Type
        FROM Technique
        WHERE Nom = ? AND ID_Joka = ?
    """, (nom_attaque, id_joka))
    type_attaque = self.curseur.fetchone()[0]
    return type_attaque