# app.py (Corrected)
import tkinter as tk
from Login import LoginScreen
from Register import RegisterScreen

class App(tk.Tk):
    def __init__(self):
        super().__init__() 
        self.title("Budget Buddy")
        self.geometry("864x558")
        self.configure(bg="#FFFFFF")

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)


        self.frames = {}

        for F in (LoginScreen, RegisterScreen):
            frame = F(parent=self.container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginScreen)

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()