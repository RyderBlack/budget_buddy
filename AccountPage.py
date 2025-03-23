import customtkinter as ctk

class AccountPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()
    
    def create_widgets(self):
        ctk.CTkLabel(self, text="Bienvenue sur votre espace !").pack()
        ctk.CTkButton(self, text="Ajouter un compte", command=self.master.show_dashboard).pack()
        ctk.CTkButton(self, text="Accéder aux comptes", command=self.master.show_dashboard).pack()
