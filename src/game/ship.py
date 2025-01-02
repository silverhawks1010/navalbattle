class Ship:
    """
    Représente un navire dans le jeu de bataille navale.
    
    Cette classe gère les propriétés d'un navire, notamment sa taille,
    son nom et sa position sur le plateau de jeu.
    
    Attributes:
        name (str): Le nom du navire (ex: "Porte-avions", "Croiseur", etc.)
        size (int): La taille du navire en nombre de cases
        position (tuple): Un tuple (x, y, horizontal) indiquant la position et l'orientation du navire
            - x (int): Coordonnée x de la première case du navire
            - y (int): Coordonnée y de la première case du navire
            - horizontal (bool): True si le navire est horizontal, False si vertical
    """
    
    def __init__(self, name, size):
        """
        Initialise un nouveau navire.
        
        Args:
            name (str): Le nom du navire
            size (int): La taille du navire en nombre de cases
        """
        self.name = name
        self.size = size
        self.position = None  # Sera défini lors du placement (x, y, horizontal)
