import tkinter as tk
from ..game.board import Board
from ..game.ship import Ship
from ..game.ai_player import AIPlayer
import random
import time

class GameWindow:
    def __init__(self, master, difficulty="moyen"):
        self.master = master
        self.master.title("Bataille Navale")
        self.cell_size = 40
        self.board_size = 10
        self.difficulty = difficulty
        
        # Création des plateaux
        self.player_board = Board()
        self.ai_board = Board()
        self.ai = AIPlayer(difficulty)
        
        # Liste des navires
        self.ships = [
            Ship("Porte-avions", 5),
            Ship("Croiseur", 4),
            Ship("Destroyer", 3),
            Ship("Destroyer", 3),
            Ship("Sous-marin", 2),
            Ship("Sous-marin", 2)
        ]
        
        # Variables de statistiques
        self.player_hits = 0
        self.player_misses = 0
        self.ai_hits = 0
        self.ai_misses = 0
        self.start_time = None
        self.game_time = None
        self.player_sunk_ships = []
        self.ai_sunk_ships = []
        
        # Variables d'état
        self.current_ship_index = 0
        self.placing_ships = True
        self.horizontal = True
        self.game_over = False
        self.placed_ships = {}
        
        # Création de l'interface
        self.setup_ui()
        self.update_current_ship_label()
        
    def setup_ui(self):
        # Création du conteneur principal
        self.container = tk.Frame(self.master)
        self.container.pack(expand=True, fill='both')
        
        # Frame pour les boutons du haut
        self.top_buttons_frame = tk.Frame(self.container)
        self.top_buttons_frame.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Bouton Menu Principal
        self.menu_button = tk.Button(
            self.top_buttons_frame,
            text="Menu Principal",
            command=self.return_to_main_menu,
            font=('Arial', 10),
            bg='navy',
            fg='white'
        )
        self.menu_button.pack(side=tk.LEFT, padx=10)
        
        # Message
        self.message_label = tk.Label(
            self.top_buttons_frame,
            text="Placez vos navires",
            font=('Arial', 12)
        )
        self.message_label.pack(side=tk.LEFT, padx=20)
        
        # Label du bateau actuel
        self.current_ship_label = tk.Label(
            self.top_buttons_frame,
            text="",
            font=('Arial', 12)
        )
        self.current_ship_label.pack(side=tk.LEFT, padx=20)
        
        # Timer
        self.timer_label = tk.Label(
            self.top_buttons_frame,
            text="Temps: 00:00",
            font=('Arial', 12)
        )
        self.timer_label.pack(side=tk.LEFT, padx=20)
        
        # Frame pour les statistiques (à gauche)
        self.stats_frame_left = tk.Frame(self.container)
        self.stats_frame_left.grid(row=1, column=0, padx=10, sticky='n')
        
        tk.Label(self.stats_frame_left, text="Vos statistiques:", font=('Arial', 12, 'bold')).pack(pady=5)
        self.player_stats_label = tk.Label(self.stats_frame_left, text="Tirs réussis: 0\nTirs manqués: 0", font=('Arial', 10))
        self.player_stats_label.pack(pady=5)
        
        tk.Label(self.stats_frame_left, text="Navires ennemis coulés:", font=('Arial', 12, 'bold')).pack(pady=5)
        self.ai_sunk_ships_label = tk.Label(self.stats_frame_left, text="", font=('Arial', 10))
        self.ai_sunk_ships_label.pack(pady=5)
        
        # Frame pour les statistiques (à droite)
        self.stats_frame_right = tk.Frame(self.container)
        self.stats_frame_right.grid(row=1, column=1, padx=10, sticky='n')
        
        tk.Label(self.stats_frame_right, text="Statistiques IA:", font=('Arial', 12, 'bold')).pack(pady=5)
        self.ai_stats_label = tk.Label(self.stats_frame_right, text="Tirs réussis: 0\nTirs manqués: 0", font=('Arial', 10))
        self.ai_stats_label.pack(pady=5)
        
        tk.Label(self.stats_frame_right, text="Vos navires coulés:", font=('Arial', 12, 'bold')).pack(pady=5)
        self.player_sunk_ships_label = tk.Label(self.stats_frame_right, text="", font=('Arial', 10))
        self.player_sunk_ships_label.pack(pady=5)
        
        # Frame pour les grilles
        self.grids_frame = tk.Frame(self.container)
        self.grids_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Frame pour les boutons du bas
        self.bottom_buttons_frame = tk.Frame(self.container)
        self.bottom_buttons_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Bouton de validation du placement
        self.validate_button = tk.Button(
            self.bottom_buttons_frame,
            text="VALIDER LE PLACEMENT",
            command=self.validate_placement,
            font=('Arial', 12),
            bg='green',
            fg='white'
        )
        self.validate_button.pack(pady=5)
        
        # Bouton rejouer (caché au début)
        self.replay_button = tk.Button(
            self.bottom_buttons_frame,
            text="REJOUER",
            command=self.restart_game,
            font=('Arial', 12),
            bg='blue',
            fg='white'
        )
        
        # Initialiser le plateau du joueur
        self.setup_player_board()
        
        # Bind de la touche R pour la rotation
        self.master.bind('r', lambda e: self.toggle_rotation())
        
    def update_timer(self):
        """Met à jour le timer"""
        if not self.placing_ships and not self.game_over:
            elapsed_time = int(time.time() - self.start_time)
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
            self.timer_label.config(text=f"Temps: {minutes:02d}:{seconds:02d}")
            
            # Mettre à jour toutes les secondes si la partie n'est pas terminée
            if not self.game_over:
                self.master.after(1000, self.update_timer)

    def update_stats(self):
        """Met à jour les statistiques affichées"""
        self.player_stats_label.config(
            text=f"Tirs réussis: {self.player_hits}\nTirs manqués: {self.player_misses}"
        )
        self.ai_stats_label.config(
            text=f"Tirs réussis: {self.ai_hits}\nTirs manqués: {self.ai_misses}"
        )
        
        # Mettre à jour la liste des navires coulés
        self.ai_sunk_ships_label.config(text="\n".join(self.ai_sunk_ships) or "Aucun")
        self.player_sunk_ships_label.config(text="\n".join(self.player_sunk_ships) or "Aucun")
        
    def setup_player_board(self):
        # Grille du joueur avec labels
        self.player_frame = tk.Frame(self.grids_frame)
        self.player_frame.pack(side=tk.LEFT, padx=20)
        
        # Labels des colonnes (A-J)
        for j in range(self.board_size):
            tk.Label(self.player_frame, text=chr(65 + j), width=2).grid(row=0, column=j)
        
        # Labels des lignes (1-10)
        for i in range(self.board_size):
            tk.Label(self.player_frame, text=str(i + 1), width=2).grid(row=i+1, column=self.board_size)
        
        # Création de la grille
        self.player_cells = []
        for i in range(self.board_size):
            row = []
            for j in range(self.board_size):
                cell = self.create_cell(self.player_frame, j, i)
                row.append(cell)
            self.player_cells.append(row)
    
    def setup_ai_board(self):
        # Grille de l'IA avec labels
        self.ai_frame = tk.Frame(self.grids_frame)
        self.ai_frame.pack(side=tk.LEFT, padx=20)
        
        # Labels des colonnes (A-J)
        for j in range(self.board_size):
            tk.Label(self.ai_frame, text=chr(65 + j), width=2).grid(row=0, column=j)
        
        # Labels des lignes (1-10)
        for i in range(self.board_size):
            tk.Label(self.ai_frame, text=str(i + 1), width=2).grid(row=i+1, column=self.board_size)
        
        # Création de la grille
        self.ai_cells = []
        for i in range(self.board_size):
            row = []
            for j in range(self.board_size):
                cell = self.create_cell(self.ai_frame, j, i, True)
                row.append(cell)
            self.ai_cells.append(row)
    
    def create_cell(self, parent, x, y, is_ai_board=False):
        """Crée une cellule de la grille"""
        cell = tk.Frame(
            parent,
            width=self.cell_size,
            height=self.cell_size,
            bg='white',
            highlightbackground='black',
            highlightthickness=1
        )
        cell.grid(row=y+1, column=x, padx=0, pady=0)
        cell.grid_propagate(False)  # Empêche le redimensionnement
        
        # Canvas pour les marqueurs
        canvas = tk.Canvas(
            cell,
            width=self.cell_size,
            height=self.cell_size,
            bg='white',
            highlightthickness=0
        )
        canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        cell.canvas = canvas  # Stocker le canvas dans la cellule
        
        if is_ai_board:
            canvas.bind('<Button-1>', lambda e, x=x, y=y: self.cell_clicked(x, y))
            cell.bind('<Button-1>', lambda e, x=x, y=y: self.cell_clicked(x, y))
        else:
            # Événements pour le placement des bateaux
            canvas.bind('<Enter>', lambda e, x=x, y=y: self.preview_ship_placement(x, y, True))
            canvas.bind('<Leave>', lambda e, x=x, y=y: self.preview_ship_placement(x, y, False))
            canvas.bind('<Button-1>', lambda e, x=x, y=y: self.place_ship_at(x, y))
            cell.bind('<Enter>', lambda e, x=x, y=y: self.preview_ship_placement(x, y, True))
            cell.bind('<Leave>', lambda e, x=x, y=y: self.preview_ship_placement(x, y, False))
            cell.bind('<Button-1>', lambda e, x=x, y=y: self.place_ship_at(x, y))
        
        return cell

    def draw_hit_marker(self, cell):
        """Dessine une croix rouge pour un tir réussi"""
        canvas = cell.canvas
        canvas.delete('all')  # Effacer les marqueurs précédents
        
        # Calculer les coordonnées pour la croix
        padding = 5
        x1, y1 = padding, padding
        x2, y2 = self.cell_size - padding, self.cell_size - padding
        
        # Dessiner la croix
        canvas.create_line(x1, y1, x2, y2, fill='red', width=2)
        canvas.create_line(x1, y2, x2, y1, fill='red', width=2)
    
    def draw_miss_marker(self, cell):
        """Dessine un cercle bleu pour un tir manqué"""
        canvas = cell.canvas
        canvas.delete('all')  # Effacer les marqueurs précédents
        
        # Calculer les coordonnées pour le cercle
        padding = 5
        x1, y1 = padding, padding
        x2, y2 = self.cell_size - padding, self.cell_size - padding
        
        # Dessiner le cercle
        canvas.create_oval(x1, y1, x2, y2, outline='blue', width=2)
    
    def reveal_sunk_ship(self, ship, cells):
        """Affiche visuellement un navire coulé sur le plateau"""
        x, y, horizontal = ship.position
        for i in range(ship.size):
            if horizontal:
                cell = cells[y][x + i]
            else:
                cell = cells[y + i][x]
            cell.configure(bg='darkred')
            cell.canvas.configure(bg='darkred')
            # Redessiner la croix sur le fond rouge
            self.draw_hit_marker(cell)
    
    def preview_ship_placement(self, x, y, show):
        """Affiche ou cache l'aperçu du placement d'un bateau"""
        if self.placing_ships and self.current_ship_index < len(self.ships):
            ship = self.ships[self.current_ship_index]
            cells_to_update = []
            
            # Vérifier si le placement est possible
            if self.horizontal:
                if x + ship.size <= self.board_size:
                    cells_to_update = [(x + i, y) for i in range(ship.size)]
            else:
                if y + ship.size <= self.board_size:
                    cells_to_update = [(x, y + i) for i in range(ship.size)]
            
            # Vérifier les collisions avec d'autres bateaux
            valid_placement = True
            if cells_to_update:
                for cell_x, cell_y in cells_to_update:
                    if self.player_board.grid[cell_y][cell_x] != 0:
                        valid_placement = False
                        break
            else:
                valid_placement = False
            
            # Mettre à jour les couleurs
            if cells_to_update:
                for cell_x, cell_y in cells_to_update:
                    cell = self.player_cells[cell_y][cell_x]
                    if show:
                        cell.configure(bg='lightgreen' if valid_placement else 'pink')
                        cell.canvas.configure(bg='lightgreen' if valid_placement else 'pink')
                    else:
                        current_state = self.player_board.grid[cell_y][cell_x]
                        color = 'gray' if current_state == 1 else 'white'
                        cell.configure(bg=color)
                        cell.canvas.configure(bg=color)
    
    def is_cell_in_ship(self, x, y, ship_position):
        ship_x, ship_y, ship_horizontal, ship_size = ship_position
        if ship_horizontal:
            return ship_y == y and ship_x <= x < ship_x + ship_size
        else:
            return ship_x == x and ship_y <= y < ship_y + ship_size

    def place_ship_at(self, x, y):
        if self.placing_ships and self.current_ship_index < len(self.ships):
            ship = self.ships[self.current_ship_index]
            
            # Vérifier si le placement est possible
            if self.horizontal:
                if x + ship.size <= self.board_size:
                    cells_to_place = [(x + i, y) for i in range(ship.size)]
            else:
                if y + ship.size <= self.board_size:
                    cells_to_place = [(x, y + i) for i in range(ship.size)]
            
            # Vérifier si les cellules sont libres
            valid_placement = True
            if cells_to_place:
                for cell_x, cell_y in cells_to_place:
                    if self.player_board.grid[cell_y][cell_x] != 0:
                        valid_placement = False
                        break
            else:
                valid_placement = False
            
            # Si le placement est valide, placer le bateau
            if valid_placement and cells_to_place:
                # Effacer l'ancien placement si existant
                if self.current_ship_index in self.placed_ships:
                    old_x, old_y, old_horizontal, old_size = self.placed_ships[self.current_ship_index]
                    if old_horizontal:
                        old_cells = [(old_x + i, old_y) for i in range(old_size)]
                    else:
                        old_cells = [(old_x, old_y + i) for i in range(old_size)]
                    for old_x, old_y in old_cells:
                        if 0 <= old_x < self.board_size and 0 <= old_y < self.board_size:
                            self.player_board.grid[old_y][old_x] = 0
                            self.player_cells[old_y][old_x].configure(bg='white')
                            self.player_cells[old_y][old_x].canvas.configure(bg='white')
                
                # Placer le nouveau bateau
                for cell_x, cell_y in cells_to_place:
                    self.player_board.grid[cell_y][cell_x] = 1
                    self.player_cells[cell_y][cell_x].configure(bg='gray')
                    self.player_cells[cell_y][cell_x].canvas.configure(bg='gray')
                
                # Sauvegarder la position du bateau
                ship.position = (x, y, self.horizontal)
                self.placed_ships[self.current_ship_index] = (x, y, self.horizontal, ship.size)
                self.player_board.ships.append(ship)
                
                # Passer au bateau suivant
                self.current_ship_index += 1
                self.update_current_ship_label()
                
                # Si c'était le dernier bateau, activer le bouton de validation
                if self.current_ship_index >= len(self.ships):
                    self.current_ship_index = 0  # Revenir au premier bateau pour permettre les ajustements
                    self.message_label.config(text="Ajustez la position des bateaux si nécessaire\npuis cliquez sur VALIDER")

    def validate_placement(self):
        """Valide le placement des bateaux et commence la partie"""
        # Vérifier si tous les bateaux ont une position
        if len(self.placed_ships) == len(self.ships):
            # Mettre à jour le plateau avec les positions finales
            self.player_board = Board()  # Réinitialiser le plateau
            for i, ship in enumerate(self.ships):
                x, y, horizontal, _ = self.placed_ships[i]
                self.player_board.place_ship(ship, x, y, horizontal)
            
            # Placer les bateaux de l'IA
            self.place_ai_ships()
            
            # Passer à la phase de jeu
            self.placing_ships = False
            self.validate_button.pack_forget()  # Cacher le bouton de validation
            self.message_label.config(text="À votre tour !")
            self.current_ship_label.config(text="")
            
            # Démarrer le timer
            self.start_time = time.time()
            self.update_timer()
            
            # Configurer le plateau de l'IA
            self.setup_ai_board()
        else:
            self.message_label.config(text="Placez tous les bateaux avant de valider")

    def place_ai_ships(self):
        """Place les bateaux de l'IA de manière aléatoire"""
        self.ai_board = Board()  # Réinitialiser le plateau de l'IA
        ai_ships = [
            Ship("Porte-avions", 5),
            Ship("Croiseur", 4),
            Ship("Destroyer", 3),
            Ship("Destroyer", 3),
            Ship("Sous-marin", 2),
            Ship("Sous-marin", 2)
        ]
        
        for ship in ai_ships:
            placed = False
            while not placed:
                x = random.randint(0, self.board_size - 1)
                y = random.randint(0, self.board_size - 1)
                horizontal = random.choice([True, False])
                if self.ai_board.place_ship(ship, x, y, horizontal):
                    placed = True

    def toggle_rotation(self):
        if self.placing_ships:
            self.horizontal = not self.horizontal
            # Réappliquer le placement du bateau actuel avec la nouvelle rotation
            if self.current_ship_index < len(self.ships) and self.current_ship_index in self.placed_ships:
                x, y, _ = self.placed_ships[self.current_ship_index][:3]
                self.preview_ship_placement(x, y, True)

    def cell_clicked(self, x, y):
        """Gestion des clics sur la grille de l'IA"""
        if not self.placing_ships and not self.game_over:
            # Vérifier si la cellule n'a pas déjà été ciblée
            result = self.ai_board.receive_shot(x, y)
            if result is not None:  # Si le tir est valide
                cell = self.ai_cells[y][x]
                cell.configure(bg='white')
                cell.canvas.configure(bg='white')
                
                if result:  # Touché
                    self.draw_hit_marker(cell)
                    self.message_label.config(text="Touché !")
                    self.player_hits += 1
                    
                    # Vérifier si un navire a été coulé
                    sunk_ship = self.ai_board.check_sunk_ship(x, y)
                    if sunk_ship:
                        self.ai_sunk_ships.append(sunk_ship.name)
                        self.message_label.config(text=f"Coulé ! {sunk_ship.name} détruit !")
                        # Révéler et marquer le navire coulé
                        self.reveal_sunk_ship(sunk_ship, self.ai_cells)
                    
                    self.update_stats()
                    # Vérifier si tous les navires sont coulés
                    if self.ai_board.all_ships_sunk():
                        self.message_label.config(text="Victoire ! Vous avez gagné !")
                        self.game_over = True
                        self.show_replay_button()
                        return
                else:  # Manqué
                    self.draw_miss_marker(cell)
                    self.message_label.config(text="Manqué !")
                    self.player_misses += 1
                    self.update_stats()
                
                if not self.game_over:
                    # Tour de l'IA
                    self.play_ai_turn()

    def play_ai_turn(self):
        """Fait jouer l'IA"""
        if not self.game_over:
            # Obtenir le coup de l'IA
            x, y = self.ai.get_move(self.player_board)
            
            # Effectuer le tir
            result = self.player_board.receive_shot(x, y)
            if result is not None:  # Si le tir est valide
                cell = self.player_cells[y][x]
                cell.configure(bg='white')
                cell.canvas.configure(bg='white')
                
                # Notifier l'IA du résultat
                self.ai.notify_hit(x, y, result)
                
                if result:  # Touché
                    self.draw_hit_marker(cell)
                    self.message_label.config(text="L'IA vous a touché !")
                    self.ai_hits += 1
                    
                    # Vérifier si un navire a été coulé
                    sunk_ship = self.player_board.check_sunk_ship(x, y)
                    if sunk_ship:
                        self.player_sunk_ships.append(sunk_ship.name)
                        self.message_label.config(text=f"L'IA a coulé votre {sunk_ship.name} !")
                        # Marquer le navire coulé
                        self.reveal_sunk_ship(sunk_ship, self.player_cells)
                    
                    self.update_stats()
                    # Vérifier si tous les navires sont coulés
                    if self.player_board.all_ships_sunk():
                        self.message_label.config(text="Game Over ! L'IA a gagné !")
                        self.game_over = True
                        self.show_replay_button()
                else:  # Manqué
                    self.draw_miss_marker(cell)
                    self.message_label.config(text="L'IA vous a manqué ! À vous de jouer !")
                    self.ai_misses += 1
                    self.update_stats()

    def update_current_ship_label(self):
        if self.placing_ships and self.current_ship_index < len(self.ships):
            ship = self.ships[self.current_ship_index]
            self.current_ship_label.config(
                text=f"Placement du {ship.name} (Taille: {ship.size})"
            )
        else:
            self.current_ship_label.config(text="")

    def update_player_board(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.player_board.grid[i][j] == 1:
                    self.player_cells[i][j].configure(bg='gray')
                elif self.player_board.grid[i][j] == 2:
                    self.player_cells[i][j].configure(bg='blue')
                elif self.player_board.grid[i][j] == 3:
                    self.player_cells[i][j].configure(bg='red')
                    
    def update_ai_board(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.ai_board.grid[i][j] == 2:
                    self.ai_cells[i][j].configure(bg='blue')
                elif self.ai_board.grid[i][j] == 3:
                    self.ai_cells[i][j].configure(bg='red')
                    
    def return_to_main_menu(self):
        # Détruire la fenêtre de jeu actuelle
        self.container.destroy()
        
        # Réinitialiser le titre
        self.master.title("Bataille Navale - Menu Principal")
        
        # Recréer le menu principal
        from .mainmenu import MainMenu
        MainMenu(self.master)

    def show_replay_button(self):
        """Affiche le bouton rejouer et arrête le timer"""
        self.validate_button.pack_forget()  # Cacher le bouton valider s'il est encore visible
        self.replay_button.pack(pady=5)  # Afficher le bouton rejouer
        
        # Sauvegarder le temps final
        if self.start_time is not None:
            self.game_time = int(time.time() - self.start_time)
            minutes = self.game_time // 60
            seconds = self.game_time % 60
            self.timer_label.config(text=f"Temps final: {minutes:02d}:{seconds:02d}")

    def restart_game(self):
        """Redémarre une nouvelle partie"""
        # Détruire le conteneur principal
        self.container.destroy()
        
        # Réinitialiser les variables
        self.player_board = Board()
        self.ai_board = Board()
        self.ai = AIPlayer(self.difficulty)
        self.current_ship_index = 0
        self.placing_ships = True
        self.horizontal = True
        self.game_over = False
        self.placed_ships = {}
        
        # Réinitialiser les statistiques
        self.player_hits = 0
        self.player_misses = 0
        self.ai_hits = 0
        self.ai_misses = 0
        self.start_time = None
        self.game_time = None
        self.player_sunk_ships = []
        self.ai_sunk_ships = []
        
        # Recréer l'interface
        self.setup_ui()
        self.update_current_ship_label()
