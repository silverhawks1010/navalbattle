import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageTk

class MainMenu:
    def __init__(self, master):
        self.master = master
        master.title("Menu Principal")
        master.attributes('-fullscreen', True)  # Set fullscreen

        # Load and resize background image
        image_path = os.path.abspath(os.path.join(os.getcwd(), 'assets', 'materials', 'main_menu.png'))
        image = Image.open(image_path)
        self.background_image = ImageTk.PhotoImage(image.resize((master.winfo_screenwidth(), master.winfo_screenheight()), Image.LANCZOS))
        self.background_label = tk.Label(master, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        # Load and resize logo image
        logo_path = os.path.abspath(os.path.join(os.getcwd(), 'assets', 'materials', 'logo.png'))
        logo_image = Image.open(logo_path)
        self.logo_image = ImageTk.PhotoImage(logo_image.resize((150, 200), Image.LANCZOS))  # Resize logo to be taller
        self.logo_label = tk.Label(master, image=self.logo_image, bg='white') 
        self.logo_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)  # Center logo at the top

        # Center buttons
        button_frame = tk.Frame(master)
        button_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center buttons on the screen
        self.play_button = tk.Button(button_frame, text="Jouer", command=self.play)
        self.play_button.pack(pady=5)

        self.options_button = tk.Button(button_frame, text="Options", command=self.options)
        self.options_button.pack(pady=5)

        self.quit_button = tk.Button(button_frame, text="Quitter", command=master.quit)
        self.quit_button.pack(pady=5)

    def play(self):
        messagebox.showinfo("Jouer", "Vous avez cliqué sur Jouer!")

    def options(self):
        messagebox.showinfo("Options", "Vous avez cliqué sur Options!")

if __name__ == '__main__':
    root = tk.Tk()
    main_menu = MainMenu(root)
    root.mainloop()
