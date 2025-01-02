import tkinter as tk
from tkinter import ttk
from .game_window import GameWindow

class MainMenu:
    """
    Représente le menu principal du jeu de bataille navale.
    
    Cette classe gère l'interface du menu principal, permettant au joueur
    de démarrer une nouvelle partie, choisir la difficulté, et quitter le jeu.
    
    Attributes:
        master (tk.Tk): La fenêtre principale de l'application
        difficulty (str): Le niveau de difficulté choisi
        main_frame (tk.Frame): Le conteneur principal pour les widgets du menu
    """
    
    def __init__(self, master):
        """
        Initialise le menu principal.
        
        Args:
            master (tk.Tk): La fenêtre principale de l'application
        """
        self.master = master
        self.master.title("Bataille Navale - Menu Principal")
        
        # Centrer la fenêtre
        window_width = 400
        window_height = 300
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.master.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # Frame principale
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(expand=True)
        
        # Titre
        self.title_label = tk.Label(
            self.main_frame,
            text="Bataille Navale",
            font=('Arial', 24, 'bold'),
            pady=20
        )
        self.title_label.pack()
        
        # Sélecteur de difficulté
        self.difficulty_frame = tk.Frame(self.main_frame)
        self.difficulty_frame.pack(pady=20)
        
        self.difficulty_label = tk.Label(
            self.difficulty_frame,
            text="Difficulté :",
            font=('Arial', 12)
        )
        self.difficulty_label.pack()
        
        self.difficulty = tk.StringVar(value="moyen")
        
        difficulties = [
            ("Facile", "facile"),
            ("Moyen", "moyen"),
            ("Difficile", "difficile")
        ]
        
        self.difficulty_buttons = []
        for text, value in difficulties:
            rb = ttk.Radiobutton(
                self.difficulty_frame,
                text=text,
                value=value,
                variable=self.difficulty
            )
            rb.pack(pady=5)
            self.difficulty_buttons.append(rb)
        
        # Bouton Jouer
        self.play_button = tk.Button(
            self.main_frame,
            text="JOUER",
            command=self.start_game,
            font=('Arial', 14, 'bold'),
            width=20,
            height=2,
            bg='navy',
            fg='white',
            activebackground='darkblue',
            activeforeground='white'
        )
        self.play_button.pack(pady=20)
        
        # Bouton Quitter
        self.quit_button = tk.Button(
            self.main_frame,
            text="Quitter",
            command=self.master.quit,
            font=('Arial', 12),
            width=10
        )
        self.quit_button.pack(pady=10)
    
    def start_game(self):
        """
        Démarre une nouvelle partie avec la difficulté choisie.
        
        Ferme le menu principal et ouvre la fenêtre de jeu.
        """
        # Fermer le menu
        self.main_frame.destroy()
        
        # Créer la fenêtre de jeu avec la difficulté sélectionnée
        game_window = GameWindow(self.master, self.difficulty.get())
