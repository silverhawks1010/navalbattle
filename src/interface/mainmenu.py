import tkinter as tk
from tkinter import ttk
from .game_window import GameWindow
from ..game.game_stats import GameStats

class MainMenu:
    """
    Représente le menu principal du jeu de bataille navale.
    
    Cette classe gère l'interface du menu principal, permettant au joueur
    de démarrer une nouvelle partie, voir les statistiques, et quitter le jeu.
    """
    
    def __init__(self, master):
        """Initialise le menu principal"""
        self.master = master
        self.master.title("Bataille Navale - Menu Principal")
        self.difficulty = "moyen"
        self.game_stats = GameStats()
        
        # Configuration de la fenêtre principale
        self.master.geometry("800x600")
        self.setup_ui()
    
    def setup_ui(self):
        """Configure l'interface utilisateur du menu principal"""
        # Conteneur principal avec deux colonnes
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Colonne gauche (contrôles)
        left_frame = tk.Frame(self.main_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Titre
        title = tk.Label(
            left_frame,
            text="BATAILLE NAVALE",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=20)
        
        # Frame pour la sélection de difficulté
        difficulty_frame = tk.Frame(left_frame)
        difficulty_frame.pack(pady=10)
        
        tk.Label(
            difficulty_frame,
            text="Choisissez la difficulté :",
            font=("Arial", 12)
        ).pack()
        
        # Liste déroulante pour la difficulté
        self.difficulty_var = tk.StringVar(value="moyen")
        difficulty_combo = ttk.Combobox(
            difficulty_frame,
            textvariable=self.difficulty_var,
            values=["facile", "moyen", "difficile"],
            state="readonly",
            width=15
        )
        difficulty_combo.pack(pady=5)
        difficulty_combo.bind('<<ComboboxSelected>>', lambda e: self.set_difficulty(self.difficulty_var.get()))
        
        # Bouton démarrer
        start_button = tk.Button(
            left_frame,
            text="Démarrer la partie",
            command=self.start_game,
            font=("Arial", 14),
            width=15
        )
        start_button.pack(pady=20)
        
        # Bouton quitter
        quit_button = tk.Button(
            left_frame,
            text="Quitter",
            command=self.master.quit,
            font=("Arial", 12),
            width=10
        )
        quit_button.pack(pady=10)
        
        # Colonne droite (statistiques)
        right_frame = tk.Frame(self.main_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Titre des statistiques
        tk.Label(
            right_frame,
            text="Statistiques",
            font=("Arial", 18, "bold")
        ).pack(pady=(0, 10))
        
        # Tableau des statistiques
        self.stats_tree = ttk.Treeview(
            right_frame,
            columns=("difficulty", "result", "duration", "accuracy"),
            show="headings",
            height=10
        )
        
        # Configuration des colonnes
        self.stats_tree.heading("difficulty", text="Difficulté")
        self.stats_tree.heading("result", text="Résultat")
        self.stats_tree.heading("duration", text="Durée")
        self.stats_tree.heading("accuracy", text="Précision")
        
        self.stats_tree.column("difficulty", width=100)
        self.stats_tree.column("result", width=100)
        self.stats_tree.column("duration", width=100)
        self.stats_tree.column("accuracy", width=100)
        
        # Scrollbar pour le tableau
        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.stats_tree.yview)
        self.stats_tree.configure(yscrollcommand=scrollbar.set)
        
        self.stats_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bouton pour plus de détails
        details_button = tk.Button(
            right_frame,
            text="Plus de détails",
            command=self.show_detailed_stats,
            font=("Arial", 10)
        )
        details_button.pack(pady=10)
        
        # Mettre à jour les statistiques
        self.update_stats_table()
    
    def update_stats_table(self):
        """Met à jour le tableau des statistiques"""
        # Effacer le tableau
        for item in self.stats_tree.get_children():
            self.stats_tree.delete(item)
        
        # Charger les statistiques
        stats = self.game_stats.stats_history
        
        # Ajouter les 10 dernières parties
        for game in reversed(stats[-10:]):
            duration = f"{game['duration'] // 60}:{game['duration'] % 60:02d}"
            self.stats_tree.insert("", "end", values=(
                game['difficulty'],
                "Victoire" if game['result'] == 'victory' else "Défaite",
                duration,
                f"{game['player_accuracy']}%"
            ))
    
    def show_detailed_stats(self):
        """Affiche une fenêtre avec les statistiques détaillées"""
        details_window = tk.Toplevel(self.master)
        details_window.title("Statistiques détaillées")
        details_window.geometry("600x800")
        
        # Titre
        tk.Label(
            details_window,
            text="Statistiques détaillées",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        # Statistiques globales
        stats_summary = self.game_stats.get_stats_summary()
        if stats_summary:
            # Frame pour les stats globales
            global_frame = tk.LabelFrame(details_window, text="Statistiques globales", pady=10, padx=10)
            global_frame.pack(fill="x", padx=20, pady=10)
            
            global_stats = [
                ("Parties jouées", stats_summary['total_games']),
                ("Victoires", stats_summary['victories']),
                ("Taux de victoire", f"{round(stats_summary['victories'] / stats_summary['total_games'] * 100, 2)}%")
            ]
            
            for label, value in global_stats:
                row = tk.Frame(global_frame)
                row.pack(fill="x", pady=2)
                tk.Label(row, text=label + ":", anchor="w").pack(side="left")
                tk.Label(row, text=str(value), anchor="e").pack(side="right")
            
            # Stats par difficulté
            for difficulty, diff_stats in stats_summary['stats_by_difficulty'].items():
                diff_frame = tk.LabelFrame(
                    details_window,
                    text=f"Statistiques - {difficulty.capitalize()}",
                    pady=10,
                    padx=10
                )
                diff_frame.pack(fill="x", padx=20, pady=10)
                
                diff_details = [
                    ("Parties jouées", diff_stats['total_games']),
                    ("Victoires", diff_stats['victories']),
                    ("Taux de victoire", f"{diff_stats['win_rate']}%"),
                    ("Durée moyenne", f"{int(diff_stats['avg_duration'] // 60)}:{int(diff_stats['avg_duration'] % 60):02d}")
                ]
                
                for label, value in diff_details:
                    row = tk.Frame(diff_frame)
                    row.pack(fill="x", pady=2)
                    tk.Label(row, text=label + ":", anchor="w").pack(side="left")
                    tk.Label(row, text=str(value), anchor="e").pack(side="right")
        
        # Bouton fermer
        tk.Button(
            details_window,
            text="Fermer",
            command=details_window.destroy
        ).pack(pady=20)
    
    def set_difficulty(self, difficulty):
        """Définit le niveau de difficulté"""
        self.difficulty = difficulty
    
    def start_game(self):
        """Démarre une nouvelle partie"""
        self.main_frame.destroy()
        GameWindow(self.master, self.difficulty)
