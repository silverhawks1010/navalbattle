import tkinter as tk
from src.interface.mainmenu import MainMenu

if __name__ == '__main__':
    root = tk.Tk()
    main_menu = MainMenu(root)
    root.mainloop()