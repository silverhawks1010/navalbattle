import random

class AIPlayer:
    """
    Représente un joueur IA dans le jeu de bataille navale.
    
    Cette classe implémente la logique de l'IA pour le placement des navires
    et la stratégie de tir. Elle peut fonctionner avec différents niveaux
    de difficulté qui affectent sa précision et sa stratégie.
    
    Attributes:
        difficulty (str): Niveau de difficulté de l'IA ('easy', 'medium', ou 'hard')
        board_size (int): Taille du plateau de jeu
        shots (list): Liste des tirs déjà effectués
        last_hit (tuple): Coordonnées du dernier tir réussi (x, y)
        hunt_mode (bool): True si l'IA est en mode "chasse" (a touché un navire)
        potential_targets (list): Liste des cibles potentielles en mode chasse
    """
    
    def __init__(self, difficulty="moyen"):
        """
        Initialise un joueur IA avec un niveau de difficulté spécifié.
        
        Args:
            difficulty (str): Niveau de difficulté ('easy', 'medium', ou 'hard')
        """
        self.difficulty = difficulty
        self.last_hit = None
        self.potential_targets = []
        self.tried_positions = set()
        self.board_size = 10
    
    def get_move(self, player_board):
        """
        Détermine la prochaine case à cibler.
        
        Utilise différentes stratégies selon le niveau de difficulté
        et si un navire a été touché précédemment.
        
        Args:
            player_board (Board): Le plateau du joueur

        Returns:
            tuple: Coordonnées du tir (x, y)
        """
        if self.difficulty == "facile":
            return self._get_random_move()
        elif self.difficulty == "moyen":
            return self._get_medium_move()
        else:  # difficile
            return self._get_hard_move(player_board)
    
    def _get_random_move(self):
        """
        Stratégie facile : tir complètement aléatoire.
        
        Returns:
            tuple: Coordonnées du tir (x, y)
        """
        while True:
            x = random.randint(0, self.board_size - 1)
            y = random.randint(0, self.board_size - 1)
            if (x, y) not in self.tried_positions:
                self.tried_positions.add((x, y))
                return x, y
    
    def _get_medium_move(self):
        """
        Stratégie moyenne : tir aléatoire mais continue autour d'un hit.
        
        Returns:
            tuple: Coordonnées du tir (x, y)
        """
        if self.last_hit and self.potential_targets:
            # Continuer à tirer autour du dernier hit
            x, y = self.potential_targets.pop()
            self.tried_positions.add((x, y))
            return x, y
        
        return self._get_random_move()
    
    def _get_hard_move(self, player_board):
        """
        Stratégie difficile : tir intelligent avec mémoire et probabilités.
        
        Args:
            player_board (Board): Le plateau du joueur

        Returns:
            tuple: Coordonnées du tir (x, y)
        """
        if self.last_hit and self.potential_targets:
            # Utiliser la connaissance des hits précédents
            best_target = max(self.potential_targets, 
                            key=lambda pos: self._calculate_probability(pos, player_board))
            self.potential_targets.remove(best_target)
            self.tried_positions.add(best_target)
            return best_target
        
        # Calculer les probabilités pour chaque case non essayée
        all_positions = [(x, y) for x in range(self.board_size) 
                        for y in range(self.board_size)
                        if (x, y) not in self.tried_positions]
        
        if not all_positions:
            return self._get_random_move()
        
        best_position = max(all_positions, 
                          key=lambda pos: self._calculate_probability(pos, player_board))
        self.tried_positions.add(best_position)
        return best_position
    
    def _calculate_probability(self, pos, player_board):
        """
        Calcule la probabilité qu'un bateau soit à une position donnée.
        
        Args:
            pos (tuple): Coordonnées de la position (x, y)
            player_board (Board): Le plateau du joueur

        Returns:
            int: La probabilité qu'un bateau soit à cette position
        """
        x, y = pos
        probability = 0
        
        # Vérifier les cases adjacentes
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.board_size and 0 <= new_y < self.board_size:
                cell_state = player_board.get_cell_state(new_x, new_y)
                if cell_state == 'hit':
                    probability += 2  # Plus probable près d'un hit
                elif cell_state == 'miss':
                    probability -= 1  # Moins probable près d'un miss
        
        # Favoriser les positions qui permettent de placer des bateaux
        for ship_size in [5, 4, 3, 3, 2, 2]:  # Tailles des bateaux selon les règles officielles
            if self._can_place_ship_at(pos, ship_size, player_board):
                probability += 1
        
        return probability
    
    def _can_place_ship_at(self, pos, ship_size, player_board):
        """
        Vérifie si un bateau de taille donnée peut être placé à la position.
        
        Args:
            pos (tuple): Coordonnées de la position (x, y)
            ship_size (int): Taille du bateau
            player_board (Board): Le plateau du joueur

        Returns:
            bool: True si le bateau peut être placé, False sinon
        """
        x, y = pos
        
        # Vérifier horizontalement
        if x + ship_size <= self.board_size:
            can_place = True
            for i in range(ship_size):
                if (x + i, y) in self.tried_positions:
                    can_place = False
                    break
            if can_place:
                return True
        
        # Vérifier verticalement
        if y + ship_size <= self.board_size:
            can_place = True
            for i in range(ship_size):
                if (x, y + i) in self.tried_positions:
                    can_place = False
                    break
            if can_place:
                return True
        
        return False
    
    def notify_hit(self, x, y, is_hit):
        """
        Notifie l'IA du résultat du tir.
        
        Met à jour la stratégie de l'IA en fonction du résultat du tir.
        
        Args:
            x (int): Coordonnée x du tir
            y (int): Coordonnée y du tir
            is_hit (bool): True si le tir a touché un navire, False sinon
        """
        if is_hit:
            self.last_hit = (x, y)
            # Ajouter les cases adjacentes comme cibles potentielles
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_x, new_y = x + dx, y + dy
                if (0 <= new_x < self.board_size and 
                    0 <= new_y < self.board_size and 
                    (new_x, new_y) not in self.tried_positions):
                    self.potential_targets.append((new_x, new_y))
        else:
            # Si c'était un miss et qu'il n'y a plus de cibles potentielles,
            # réinitialiser le dernier hit
            if not self.potential_targets:
                self.last_hit = None
