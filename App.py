import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import mysql.connector
from dotenv import load_dotenv
import os
from passlib.hash import bcrypt
import re
from LoginPage import LoginPage
from RegisterPage import RegisterPage
from AccountPage import AccountPage
from Dashboard import Dashboard
from DashboardCharts import DashboardCharts


load_dotenv(".env")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

def validate_email(email):
    return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email))

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1280x720")
        self.title("Budget Buddy")
        self.resizable(False, False)
        self.show_login_page()
    
    def show_login_page(self):
        self.clear_window()
        self.page = LoginPage(self)
        self.page.pack(fill="both", expand=True)
    
    def show_register_page(self):
        self.clear_window()
        self.page = RegisterPage(self)
        self.page.pack(fill="both", expand=True)
    
    def show_account_page(self, user_id):
        self.clear_window()
        self.page = AccountPage(self, user_id)
        self.page.pack(fill="both", expand=True)

    def show_dashboard(self, user_id):
        self.clear_window()
        self.page = Dashboard(self, user_id)
        self.page.pack(fill="both", expand=True)

    def show_dashboard_charts(self, user_id):
        self.clear_window()
        self.page = DashboardCharts(self, user_id)
        self.page.pack(fill="both", expand=True)
        
    def show_dashboard_transactions(self, user_id):
        self.clear_window()
        from DashboardTransactions import DashboardTransactions
        self.page = DashboardTransactions(self, user_id)
        self.page.pack(fill="both", expand=True)
    
    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()
