class Board:
    def __init__(self):
        self.size = 10
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.ships = []
        # 0: empty, 1: ship, 2: hit, 3: miss
    
    def place_ship(self, ship, x, y, horizontal):
        """Place un bateau sur le plateau"""
        # Vérifier si le placement est possible
        if horizontal:
            if x + ship.size > self.size:
                return False
            # Vérifier si l'espace est libre
            for i in range(ship.size):
                if self.grid[y][x + i] != 0:
                    return False
            # Placer le bateau
            for i in range(ship.size):
                self.grid[y][x + i] = 1
        else:
            if y + ship.size > self.size:
                return False
            # Vérifier si l'espace est libre
            for i in range(ship.size):
                if self.grid[y + i][x] != 0:
                    return False
            # Placer le bateau
            for i in range(ship.size):
                self.grid[y + i][x] = 1
        
        # Ajouter le bateau à la liste avec sa position
        ship.position = (x, y, horizontal)
        self.ships.append(ship)
        return True
    
    def receive_shot(self, x, y):
        """Reçoit un tir aux coordonnées (x, y)"""
        # Si la cellule a déjà été touchée ou manquée
        if self.grid[y][x] in [2, 3]:
            return None
        
        if self.grid[y][x] == 1:  # Touché
            self.grid[y][x] = 2  # Marquer comme touché
            return True
        else:  # Manqué
            self.grid[y][x] = 3  # Marquer comme manqué
            return False
    
    def get_cell_state(self, x, y):
        """Retourne l'état d'une cellule"""
        state = self.grid[y][x]
        if state == 0:
            return 'empty'
        elif state == 1:
            return 'ship'
        elif state == 2:
            return 'hit'
        else:
            return 'miss'
    
    def all_ships_sunk(self):
        """Vérifie si tous les bateaux sont coulés"""
        for ship in self.ships:
            x, y, horizontal = ship.position
            # Vérifier chaque case du bateau
            if horizontal:
                for i in range(ship.size):
                    if self.grid[y][x + i] == 1:  # Si une case n'est pas touchée
                        return False
            else:
                for i in range(ship.size):
                    if self.grid[y + i][x] == 1:  # Si une case n'est pas touchée
                        return False
        return True

    def check_sunk_ship(self, x, y):
        """Vérifie si un navire a été coulé après un tir en (x, y)"""
        # Trouver le navire touché
        hit_ship = None
        for ship in self.ships:
            ship_x, ship_y, horizontal = ship.position
            if horizontal:
                if ship_y == y and ship_x <= x < ship_x + ship.size:
                    hit_ship = ship
                    break
            else:
                if ship_x == x and ship_y <= y < ship_y + ship.size:
                    hit_ship = ship
                    break
        
        if hit_ship:
            # Vérifier si toutes les cases du navire sont touchées
            ship_x, ship_y, horizontal = hit_ship.position
            if horizontal:
                for i in range(hit_ship.size):
                    if self.grid[ship_y][ship_x + i] != 2:  # 2 = touché
                        return None
            else:
                for i in range(hit_ship.size):
                    if self.grid[ship_y + i][ship_x] != 2:  # 2 = touché
                        return None
            return hit_ship
        return None
