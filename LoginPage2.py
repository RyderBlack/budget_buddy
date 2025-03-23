from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
import customtkinter as ctk


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/login_assets")

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

# Label Email
canvas.create_text(
    565.0,
    220.0,
    anchor="nw",
    text="Adresse Email",
    fill="#FFFFFF",
    font=("Inter Italic", 22 * -1)
)

# TextBox Email
frame1 = ctk.CTkFrame(window, fg_color="transparent", width=362, height=40)
frame1.place(x=459.0, y=250.0)
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

# Label Password
canvas.create_text(
    565.0,
    320.0,
    anchor="nw",
    text="Mot de Passe",
    fill="#FFFFFF",
    font=("Inter Italic", 22 * -1)
)

# TextBox Password
frame2 = ctk.CTkFrame(window, fg_color="transparent", width=362, height=40)
frame2.place(x=459.0, y=350.0)
frame2.pack_propagate(False)

entry_2 = ctk.CTkEntry(
    frame2,
    corner_radius=15,
    border_width=0,
    fg_color="#FFFFFF",
    text_color="#000716",
    width=360,
    height=40,
    show="•"
)
entry_2.pack(fill="both", expand=True)


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
    x=542.0,
    y=401.0,
    width=195.0,
    height=46.0
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

register_text_id = canvas.create_text(
    480.00,
    460.00,
    anchor="nw",
    text="Pas de compte? Cliquez-ici pour vous inscrire",
    fill="#FFFFFF",
    font=("Inter Italic", 16 * -1)
)
def on_register_text_click(event):
    print("Redirection vers la page d'inscription")
    # Ici rediriger vers register

def on_register_text_enter(event):
    canvas.config(cursor="hand2")
    canvas.itemconfig(register_text_id, fill="#6AB9FF")

def on_register_text_leave(event):
    canvas.config(cursor="")
    canvas.itemconfig(register_text_id, fill="#FFFFFF")

canvas.tag_bind(register_text_id, "<Button-1>", on_register_text_click)
canvas.tag_bind(register_text_id, "<Enter>", on_register_text_enter)
canvas.tag_bind(register_text_id, "<Leave>", on_register_text_leave)

# Option "Mot de passe oublié"
forgot_password_text_id = canvas.create_text(
    560.00,
    500.00,
    anchor="nw",
    text="Mot de passe oublié ?",
    fill="#FFFFFF",
    font=("Inter Italic", 16 * -1)
)

def on_forgot_password_click(event):
    print("Redirection vers la page de récupération de mot de passe")
    # Ici code recup password 
    
def on_forgot_password_enter(event):
    canvas.config(cursor="hand2")
    canvas.itemconfig(forgot_password_text_id, fill="#6AB9FF")

def on_forgot_password_leave(event):
    canvas.config(cursor="")
    canvas.itemconfig(forgot_password_text_id, fill="#FFFFFF")

canvas.tag_bind(forgot_password_text_id, "<Button-1>", on_forgot_password_click)
canvas.tag_bind(forgot_password_text_id, "<Enter>", on_forgot_password_enter)
canvas.tag_bind(forgot_password_text_id, "<Leave>", on_forgot_password_leave)



window.resizable(False, False)
window.mainloop()