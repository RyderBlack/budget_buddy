from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH /Path(r"./assets/dashboard_assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1280x720")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 720,
    width = 1280,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)

# Black BG
canvas.create_rectangle(
    0.0,
    0.0,
    1280.0,
    720.0,
    fill="#1E1E1E",
    outline="")

# Logo
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    76.0,
    71.0,
    image=image_image_1
)

# Title
canvas.create_text(
    290.0,
    8.0,
    anchor="nw",
    text="Budget Buddy",
    fill="#6AB9FF",
    font=("Italianno Regular", 128 * -1)
)

# Line under Title
canvas.create_rectangle(
    23.0,
    158.99995582038537,
    1256.0,
    160.1302490234375,
    fill="#FFFFFF",
    outline="")

# Main White BG
canvas.create_rectangle(
    24.0,
    176.0,
    1256.0,
    691.0,
    fill="#FDFDFD",
    outline="")

# Solde Compte Title
canvas.create_text(
    191.0,
    186.0,
    anchor="nw",
    text="Solde Compte",
    fill="#000000",
    font=("Roboto Medium", 36 * -1)
)

# Solde Compte Underline
canvas.create_rectangle(
    76.0,
    228.0,
    555.9999812222486,
    229.99999995777125,
    fill="#262626",
    outline="")

#  Solde Compte TextBox
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    315.5,
    285.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#EAEAEA",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=82.0,
    y=242.0,
    width=467.0,
    height=85.0
)

# Side line
canvas.create_rectangle(
    639.0,
    191.0,
    640.0,
    667.0,
    fill="#262626",
    outline="")




window.resizable(False, False)
window.mainloop()
