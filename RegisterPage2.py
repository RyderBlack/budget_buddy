from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
import customtkinter as ctk


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/register_assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)    


# Initialize CustomTkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

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
    relief="ridge"
)
canvas.place(x=0, y=0)


image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(640.0, 360.0, image=image_image_1)

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(103.0, 623.0, image=image_image_2)

# Title
canvas.create_text(
    300.0,
    25.0,
    anchor="nw",
    text="Budget Buddy",
    fill="#6AB9FF",
    font=("Dune Rise", 64 * -1) 
)

#  Label Nom
canvas.create_text(
    461.0,
    173.0,
    anchor="nw",
    text="Nom",
    fill="#FFFFFF",
    font=("Inter Italic", 20 * -1)
)

# TextBox Nom
frame1 = ctk.CTkFrame(window, fg_color="transparent", width=362, height=40)
frame1.place(x=458.0, y=194.0)
frame1.pack_propagate(False)

entry_1 = ctk.CTkEntry(
    frame1,
    corner_radius=15,
    border_width=0,
    fg_color="#FFFFFF",
    text_color="#000716",
    width=360,
    height=40
)
entry_1.pack(fill="both", expand=True)


#  Label Prenom
canvas.create_text(
    461.0,
    261.0,
    anchor="nw",
    text="Prenom",
    fill="#FFFFFF",
    font=("Inter Italic", 20 * -1)
)

# TextBox Prenom
frame2 = ctk.CTkFrame(window, fg_color="transparent", width=362, height=40)
frame2.place(x=458.0, y=282.0)
frame2.pack_propagate(False)

entry_2 = ctk.CTkEntry(
    frame2,
    corner_radius=15,
    border_width=0,
    fg_color="#FFFFFF",
    text_color="#000716",
    width=360,
    height=40
)
entry_2.pack(fill="both", expand=True)


# Label Email
canvas.create_text(
    461.0,
    349.0,
    anchor="nw",
    text="Adresse Email",
    fill="#FFFFFF",
    font=("Inter Italic", 20 * -1)
)

# TextBox Email
frame3 = ctk.CTkFrame(window, fg_color="transparent", width=362, height=40)
frame3.place(x=459.0, y=370.0)
frame3.pack_propagate(False)

entry_3 = ctk.CTkEntry(
    frame3,
    corner_radius=15,
    border_width=0,
    fg_color="#FFFFFF",
    text_color="#000716",
    width=360,
    height=40
)
entry_3.pack(fill="both", expand=True)

# Label Password
canvas.create_text(
    461.0,
    437.0,
    anchor="nw",
    text="Mot de Passe",
    fill="#FFFFFF",
    font=("Inter Italic", 20 * -1)
)

# TextBox Password
frame4 = ctk.CTkFrame(window, fg_color="transparent", width=362, height=40)
frame4.place(x=459.0, y=458.0)
frame4.pack_propagate(False)

entry_4 = ctk.CTkEntry(
    frame4,
    corner_radius=15,
    border_width=0,
    fg_color="#FFFFFF",
    text_color="#000716",
    width=360,
    height=40,
    show="•"
)
entry_4.pack(fill="both", expand=True)


# Register Button
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
    x=538.0,
    y=524.0,
    width=204.0,
    height=55.0
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

# Link to Login Page
login_text_id = canvas.create_text(
    535.00,
    600.00,
    anchor="nw",
    text="Cliquez-ici pour vous connecter",
    fill="#FFFFFF",
    font=("Inter Italic", 16 * -1)
)

def on_login_text_click(event):
    print("Redirection vers la page de connexion")
    # Ici code redirection vers login page

def on_login_text_enter(event):
    canvas.config(cursor="hand2")
    canvas.itemconfig(login_text_id, fill="#6AB9FF")

def on_login_text_leave(event):
    canvas.config(cursor="")
    canvas.itemconfig(login_text_id, fill="#FFFFFF")

canvas.tag_bind(login_text_id, "<Button-1>", on_login_text_click)
canvas.tag_bind(login_text_id, "<Enter>", on_login_text_enter)
canvas.tag_bind(login_text_id, "<Leave>", on_login_text_leave)



window.resizable(False, False)
window.mainloop()