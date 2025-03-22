import mysql.connector
import os
from dotenv import load_dotenv
from pathlib import Path
from tkinter import Tk, Canvas, Label, PhotoImage
import sys

# Charger l'ID du compte via les arguments de la ligne de commande
if len(sys.argv) > 1:
    account_id = sys.argv[1]  # L'ID du compte transmis en argument
    print(f"Dashboard ouvert pour l'ID du compte : {account_id}")
else:
    account_id = None  # Aucun ID fourni
    print("Aucun ID de compte fourni.")

# Charger les variables d'environnement
load_dotenv(".env")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

def get_account_balance(account_id):
    """Récupérer le solde du compte bancaire via son ID."""
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=DATABASE_PASSWORD,
            database="budget_buddy",
        )
        cursor = db.cursor()
        query = "SELECT account_balance FROM bank_account WHERE id = %s"
        cursor.execute(query, (account_id,))
        result = cursor.fetchone()
        return result[0] if result else "Compte introuvable"
    except mysql.connector.Error as e:
        return f"Erreur MySQL : {e}"
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals() and db.is_connected():
            db.close()

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/dashboard_assets")

# Vérifier si l'ID du compte est fourni
if account_id:
    # Récupérer le solde via la fonction
    account_balance = get_account_balance(account_id)
else:
    account_balance = "Aucun compte sélectionné"

# Initialiser la fenêtre Tkinter
window = Tk()
window.geometry("1280x720")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=720,
    width=1280,
    bd=0,
    highlightthickness=0,
    relief="ridge",
)
canvas.place(x=0, y=0)

# Fond noir
canvas.create_rectangle(0.0, 0.0, 1280.0, 720.0, fill="#1E1E1E", outline="")

# Logo
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
canvas.create_image(76.0, 71.0, image=image_image_1)

# Titre
canvas.create_text(
    290.0,
    8.0,
    anchor="nw",
    text="Budget Buddy",
    fill="#6AB9FF",
    font=("Italianno Regular", 128 * -1),
)

# Ligne sous le titre
canvas.create_rectangle(
    23.0, 159.0, 1256.0, 160.0, fill="#FFFFFF", outline=""
)

# Fond blanc principal
canvas.create_rectangle(
    24.0, 176.0, 1256.0, 691.0, fill="#FDFDFD", outline=""
)

# Titre du solde du compte
canvas.create_text(
    191.0,
    186.0,
    anchor="nw",
    text="Solde Compte",
    fill="#000000",
    font=("Roboto Medium", 36 * -1),
)

# Soulignement
canvas.create_rectangle(
    76.0, 228.0, 556.0, 230.0, fill="#262626", outline=""
)

# Étiquette affichant le solde du compte
entry_1 = Label(
    window,
    text=f"Solde du compte : {account_balance} €",  # Mettre à jour dynamiquement le solde
    bg="#EAEAEA",
    fg="#000716",
    font=("Roboto", 16),
)
entry_1.place(x=82.0, y=242.0, width=467.0, height=85.0)

# Ligne verticale
canvas.create_rectangle(
    639.0, 191.0, 640.0, 667.0, fill="#262626", outline=""
)

# Empêcher la redimension de la fenêtre
window.resizable(False, False)

# Lancer l'application
window.mainloop()
