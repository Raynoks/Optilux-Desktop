"""
Couche base de données pour OPTILUX Desktop.
Utilise SQLite (fichier local optilux.db) - aucune connexion internet requise.
"""
import sqlite3
import os
import datetime
from auth import hash_password

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "optilux.db")
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
PRODUCT_IMAGES_DIR = os.path.join(ASSETS_DIR, "products")
FACTURE_FILES_DIR = os.path.join(ASSETS_DIR, "factures_stockees")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    nom TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('admin','employee'))
);

CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    tel TEXT
);

CREATE TABLE IF NOT EXISTS prescriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    date TEXT,
    type TEXT,
    vl_od_sph TEXT, vl_od_cyl TEXT, vl_od_axe TEXT,
    vl_og_sph TEXT, vl_og_cyl TEXT, vl_og_axe TEXT,
    vp_od TEXT, vp_og TEXT
);

CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_nom TEXT,
    date TEXT,
    heure TEXT,
    service TEXT,
    statut TEXT
);

CREATE TABLE IF NOT EXISTS stock (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    categorie TEXT,
    marque TEXT,
    qte INTEGER DEFAULT 0,
    prix_achat REAL DEFAULT 0,
    prix_vente REAL DEFAULT 0,
    seuil INTEGER DEFAULT 3
);

CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER REFERENCES clients(id) ON DELETE SET NULL,
    date TEXT,
    monture REAL DEFAULT 0,
    verres REAL DEFAULT 0,
    vente REAL DEFAULT 0,
    avance REAL DEFAULT 0,
    mutuelle REAL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    libelle TEXT,
    categorie TEXT,
    montant REAL DEFAULT 0,
    recurrent INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT,
    user TEXT,
    action TEXT
);

CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT
);

CREATE TABLE IF NOT EXISTS types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categorie TEXT NOT NULL,
    valeur TEXT NOT NULL,
    UNIQUE(categorie, valeur)
);

CREATE TABLE IF NOT EXISTS commandes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER REFERENCES clients(id) ON DELETE SET NULL,
    description TEXT,
    date_commande TEXT,
    date_prevue TEXT,
    statut TEXT DEFAULT 'En attente'
);

CREATE TABLE IF NOT EXISTS factures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT DEFAULT 'client',
    titre TEXT,
    date TEXT,
    montant REAL DEFAULT 0,
    fichier_path TEXT,
    notes TEXT,
    sale_id INTEGER REFERENCES sales(id) ON DELETE SET NULL
);
"""

# Colonnes ajoutées après la version initiale — appliquées via ALTER TABLE (idempotent,
# les erreurs "duplicate column" sont ignorées) pour ne jamais perdre les données existantes.
MIGRATIONS = [
    "ALTER TABLE clients ADD COLUMN prenom TEXT",
    "ALTER TABLE clients ADD COLUMN date_naissance TEXT",
    "ALTER TABLE clients ADD COLUMN ville TEXT",
    "ALTER TABLE clients ADD COLUMN remise INTEGER DEFAULT 0",

    "ALTER TABLE stock ADD COLUMN image_path TEXT",
    "ALTER TABLE stock ADD COLUMN lentille_type TEXT",
    "ALTER TABLE stock ADD COLUMN lentille_duree TEXT",

    "ALTER TABLE sales ADD COLUMN paiement TEXT DEFAULT 'Espèces'",
    "ALTER TABLE sales ADD COLUMN remise INTEGER DEFAULT 0",

    "ALTER TABLE expenses ADD COLUMN personnelle INTEGER DEFAULT 0",
    "ALTER TABLE expenses ADD COLUMN date_echeance TEXT",

    # Fiche client complète (copie 1:1 du formulaire papier)
    "ALTER TABLE prescriptions ADD COLUMN vl INTEGER DEFAULT 0",
    "ALTER TABLE prescriptions ADD COLUMN vp INTEGER DEFAULT 0",
    "ALTER TABLE prescriptions ADD COLUMN pg INTEGER DEFAULT 0",
    "ALTER TABLE prescriptions ADD COLUMN arx_od TEXT",
    "ALTER TABLE prescriptions ADD COLUMN arx_og TEXT",
    "ALTER TABLE prescriptions ADD COLUMN av_od TEXT",
    "ALTER TABLE prescriptions ADD COLUMN av_og TEXT",
    "ALTER TABLE prescriptions ADD COLUMN av_odg TEXT",
    "ALTER TABLE prescriptions ADD COLUMN prescripteur TEXT",
    "ALTER TABLE prescriptions ADD COLUMN date_prescription TEXT",
    "ALTER TABLE prescriptions ADD COLUMN mutuelle_oui INTEGER DEFAULT 0",
    "ALTER TABLE prescriptions ADD COLUMN mutuelle_texte TEXT",
    "ALTER TABLE prescriptions ADD COLUMN maladie_oui INTEGER DEFAULT 0",
    "ALTER TABLE prescriptions ADD COLUMN maladie_texte TEXT",
    "ALTER TABLE prescriptions ADD COLUMN montage_oui INTEGER DEFAULT 0",
    "ALTER TABLE prescriptions ADD COLUMN od_sph TEXT",
    "ALTER TABLE prescriptions ADD COLUMN od_cyl TEXT",
    "ALTER TABLE prescriptions ADD COLUMN od_axe TEXT",
    "ALTER TABLE prescriptions ADD COLUMN od_add TEXT",
    "ALTER TABLE prescriptions ADD COLUMN od_ep TEXT",
    "ALTER TABLE prescriptions ADD COLUMN od_ht TEXT",
    "ALTER TABLE prescriptions ADD COLUMN og_sph TEXT",
    "ALTER TABLE prescriptions ADD COLUMN og_cyl TEXT",
    "ALTER TABLE prescriptions ADD COLUMN og_axe TEXT",
    "ALTER TABLE prescriptions ADD COLUMN og_add TEXT",
    "ALTER TABLE prescriptions ADD COLUMN og_ep TEXT",
    "ALTER TABLE prescriptions ADD COLUMN og_ht TEXT",
    "ALTER TABLE prescriptions ADD COLUMN verres_texte TEXT",
    "ALTER TABLE prescriptions ADD COLUMN verres_check INTEGER DEFAULT 0",
    "ALTER TABLE prescriptions ADD COLUMN firme_texte TEXT",
    "ALTER TABLE prescriptions ADD COLUMN firme_check INTEGER DEFAULT 0",
    "ALTER TABLE prescriptions ADD COLUMN monture_texte TEXT",
    "ALTER TABLE prescriptions ADD COLUMN monture_check INTEGER DEFAULT 0",
    "ALTER TABLE prescriptions ADD COLUMN prix TEXT",
    "ALTER TABLE prescriptions ADD COLUMN avance TEXT",
    "ALTER TABLE prescriptions ADD COLUMN jour_livraison TEXT",
    "ALTER TABLE prescriptions ADD COLUMN r_texte TEXT",

    "ALTER TABLE commandes ADD COLUMN type TEXT DEFAULT 'client'",
    "ALTER TABLE commandes ADD COLUMN fournisseur TEXT",
]

DEFAULT_TYPES = {
    "stock_categorie": ["Monture optique", "Monture solaire", "Verres", "Solaire", "Lentilles", "Accessoire"],
    "stock_marque": ["Ray-Ban", "Indo", "CIOM"],
    "depense_categorie": ["Loyer", "Parking", "CNSS", "Amendis", "Téléphone / Wifi", "Essence", "Voiture", "Salaire", "Autre"],
    "lentille_type": ["Souples", "Rigides", "Couleur", "Correctrices"],
    "lentille_duree": ["1 Jour", "2 Semaines", "1 Mois", "3 Mois", "1 An"],
}

DISCOUNT_OPTIONS = [0, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 100]


def init_db():
    first_run = not os.path.exists(DB_PATH)
    conn = get_connection()
    conn.executescript(SCHEMA)
    conn.commit()
    for stmt in MIGRATIONS:
        try:
            conn.execute(stmt)
        except sqlite3.OperationalError:
            pass  # colonne déjà présente
    conn.commit()
    if first_run:
        _seed(conn)
        _seed_types(conn)
    else:
        _seed_types(conn, only_if_empty=True)
    conn.close()
    os.makedirs(PRODUCT_IMAGES_DIR, exist_ok=True)
    os.makedirs(FACTURE_FILES_DIR, exist_ok=True)


def _seed_types(conn, only_if_empty=False):
    for categorie, valeurs in DEFAULT_TYPES.items():
        existing = conn.execute("SELECT COUNT(*) n FROM types WHERE categorie=?", (categorie,)).fetchone()["n"]
        if only_if_empty and existing > 0:
            continue
        for v in valeurs:
            conn.execute("INSERT OR IGNORE INTO types (categorie, valeur) VALUES (?,?)", (categorie, v))
    conn.commit()


def get_types(categorie):
    conn = get_connection()
    rows = conn.execute("SELECT valeur FROM types WHERE categorie=? ORDER BY valeur", (categorie,)).fetchall()
    conn.close()
    return [r["valeur"] for r in rows]


def add_type(categorie, valeur):
    conn = get_connection()
    conn.execute("INSERT OR IGNORE INTO types (categorie, valeur) VALUES (?,?)", (categorie, valeur))
    conn.commit()
    conn.close()


def delete_type(type_id):
    conn = get_connection()
    conn.execute("DELETE FROM types WHERE id=?", (type_id,))
    conn.commit()
    conn.close()


def get_setting(key, default=None):
    conn = get_connection()
    row = conn.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
    conn.close()
    return row["value"] if row else default


def set_setting(key, value):
    conn = get_connection()
    conn.execute("INSERT INTO settings (key, value) VALUES (?, ?) "
                 "ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key, value))
    conn.commit()
    conn.close()


def _seed(conn):
    admin_hash, admin_salt = hash_password("admin123")
    emp_hash, emp_salt = hash_password("employe123")
    conn.execute(
        "INSERT INTO users (username,password_hash,salt,nom,role) VALUES (?,?,?,?,?)",
        ("admin", admin_hash, admin_salt, "Sanae Haourir", "admin"),
    )
    conn.execute(
        "INSERT INTO users (username,password_hash,salt,nom,role) VALUES (?,?,?,?,?)",
        ("employe1", emp_hash, emp_salt, "Employé Comptoir", "employee"),
    )

    c1 = conn.execute("INSERT INTO clients (nom, prenom, tel, remise) VALUES (?,?,?,?)",
                       ("HZIMAR", "Boutaina", "", 0)).lastrowid
    c2 = conn.execute("INSERT INTO clients (nom, prenom, tel, remise) VALUES (?,?,?,?)",
                       ("HAOURIR", "Afaf", "", 0)).lastrowid
    conn.execute("INSERT INTO clients (nom, prenom, tel, remise) VALUES (?,?,?,?)",
                 ("AABOUD", "Farah", "", 0))

    conn.execute("""INSERT INTO prescriptions
        (client_id,date,vl,od_sph,od_cyl,od_axe,og_sph,og_cyl,og_axe)
        VALUES (?,?,?,?,?,?,?,?,?)""",
        (c1, "2023-03-30", 1, "-4,50", "-0,25", "9", "-5,25", "-0,25", "23"))
    conn.execute("""INSERT INTO prescriptions
        (client_id,date,vl,od_sph,od_cyl,od_axe,og_sph,og_cyl,og_axe)
        VALUES (?,?,?,?,?,?,?,?,?)""",
        (c2, "2023-04-07", 1, "-0,25", "-0,75", "8", "-0,50", "-0,50", "168"))

    today = datetime.date.today().isoformat()
    conn.execute("INSERT INTO appointments (client_nom,date,heure,service,statut) VALUES (?,?,?,?,?)",
                 ("AABOUD FARAH", today, "11:00", "Consultation de contrôle", "Prévu"))
    conn.execute("INSERT INTO appointments (client_nom,date,heure,service,statut) VALUES (?,?,?,?,?)",
                 ("HZIMAR BOUTAINA", today, "15:30", "Essayage monture", "Confirmé"))

    conn.execute("""INSERT INTO stock (nom,categorie,marque,qte,prix_achat,prix_vente,seuil)
                     VALUES (?,?,?,?,?,?,?)""",
                 ("Monture Ray-Ban", "Monture optique", "Ray-Ban", 2, 350, 700, 3))
    conn.execute("""INSERT INTO stock (nom,categorie,marque,qte,prix_achat,prix_vente,seuil)
                     VALUES (?,?,?,?,?,?,?)""",
                 ("Verres Indo (paire)", "Verres", "Indo", 6, 180, 390, 4))
    conn.execute("""INSERT INTO stock (nom,categorie,marque,qte,prix_achat,prix_vente,seuil)
                     VALUES (?,?,?,?,?,?,?)""",
                 ("Solaire CIOM", "Solaire", "CIOM", 1, 250, 450, 3))

    conn.execute("""INSERT INTO sales (client_id,date,monture,verres,vente,avance,mutuelle,paiement)
                     VALUES (?,?,?,?,?,?,?,?)""",
                 (c1, "2023-03-30", 700, 780, 1480, 1480, 0, "Espèces"))
    conn.execute("""INSERT INTO sales (client_id,date,monture,verres,vente,avance,mutuelle,paiement)
                     VALUES (?,?,?,?,?,?,?,?)""",
                 (c2, "2023-04-07", 700, 700, 1400, 1400, 0, "TPE"))

    conn.execute("""INSERT INTO expenses (date,libelle,categorie,montant,recurrent,personnelle)
                     VALUES (?,?,?,?,?,?)""",
                 (today, "Loyer (x2)", "Loyer", 7000, 1, 0))
    conn.execute("""INSERT INTO expenses (date,libelle,categorie,montant,recurrent,personnelle)
                     VALUES (?,?,?,?,?,?)""",
                 (today, "Amendis magasin", "Amendis", 480, 1, 0))
    conn.execute("""INSERT INTO expenses (date,libelle,categorie,montant,recurrent,personnelle)
                     VALUES (?,?,?,?,?,?)""",
                 (today, "CNSS", "CNSS", 416, 1, 0))
    conn.execute("""INSERT INTO expenses (date,libelle,categorie,montant,recurrent,personnelle)
                     VALUES (?,?,?,?,?,?)""",
                 (today, "Essence", "Essence", 300, 0, 0))

    conn.execute("""INSERT INTO commandes (client_id,description,date_commande,date_prevue,statut)
                     VALUES (?,?,?,?,?)""",
                 (c1, "Verres progressifs sur commande", today,
                  (datetime.date.today() + datetime.timedelta(days=3)).isoformat(), "En attente"))

    conn.commit()


def log_action(user, action):
    conn = get_connection()
    conn.execute("INSERT INTO audit_log (ts, user, action) VALUES (?,?,?)",
                 (datetime.datetime.now().isoformat(timespec="seconds"), user, action))
    conn.commit()
    conn.close()
