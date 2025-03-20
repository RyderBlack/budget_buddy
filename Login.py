from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage



OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/login_assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("864x558")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 558,
    width = 864,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)

# Image Left Side
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    216.0,
    279.0,
    image=image_image_1
)

# Right Side Color
canvas.create_rectangle(
    432.0001220703125,
    0.0,
    864.0001220703125,
    558.5,
    fill="#1E1E1E",
    outline="")

#  Title text
canvas.create_text(
    445.0,
    20,
    anchor="nw",
    text="Budget Buddy",
    fill="#6AB9FF",
    font=("Comic Sans MS", 64 * -1)
)


# Label for email input
canvas.create_text(
    475.5003662109375,
    138.4996337890625,
    anchor="nw",
    text="Adresse Email",
    fill="#FFFFFF",
    font=("Inter Italic", 20 * -1)
)


#  Textbox for email
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    653.7503662109375,
    189.4998779296875,
    image=entry_image_1
)
entry_1 = Entry(
    font="Inter 20",
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=475.5003662109375,
    y=162.4998779296875,
    width=356.5,
    height=52.0
)

# Label Password input
canvas.create_text(
    475.5003662109375,
    245.9996337890625,
    anchor="nw",
    text="Mot de Passe",
    fill="#FFFFFF",
    font=("Inter Italic", 20 * -1)
)

#  Textbox for password
entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    653.7503662109375,
    297.0,
    image=entry_image_2
)
entry_2 = Entry(
    font="Inter  20",
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0, 
    show="*"
)
entry_2.place(
    x=475.5003662109375,
    y=270.0,
    width=356.5,
    height=52.0
)

# Submit button
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat",
    cursor="hand2"
)

button_1.place(
    x=541.5003662109375,
    y=423.9996337890625,
    width=220.0,
    height=73.0
)

button_image_hover_1 = PhotoImage(
    file=relative_to_assets("button_hover_1.png"))

def button_1_hover(e):
    button_1.config(
        image=button_image_hover_1
    )
def button_1_leave(e):
    button_1.config(
        image=button_image_1
    )

button_1.bind('<Enter>', button_1_hover)
button_1.bind('<Leave>', button_1_leave)

canvas.create_text(
    500.00,
    500.00,
    anchor="nw",
    text="Pas de compte? Cliquez ici pour vous enregistrer",
    fill="#FFFFFF",
    font=("Inter Italic", 14 * -1)
)

window.resizable(True, True)  
window.mainloop()
