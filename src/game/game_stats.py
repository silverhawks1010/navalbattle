import json
import os
from datetime import datetime

class GameStats:
    """
    Gère les statistiques et la sauvegarde des résultats des parties.
    
    Cette classe s'occupe de sauvegarder et charger les résultats des parties
    dans un fichier JSON, permettant de conserver un historique des performances.
    
    Attributes:
        save_file (str): Chemin vers le fichier de sauvegarde
        stats_history (list): Liste des statistiques des parties précédentes
    """
    
    def __init__(self):
        """Initialise le gestionnaire de statistiques."""
        self.save_file = "game_stats.json"
        self.stats_history = self._load_stats()
    
    def _load_stats(self):
        """
        Charge les statistiques depuis le fichier JSON.
        
        Returns:
            list: Liste des statistiques des parties précédentes
        """
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []
    
    def save_game_stats(self, stats):
        """
        Sauvegarde les statistiques d'une partie.
        
        Args:
            stats (dict): Dictionnaire contenant les statistiques de la partie
                - difficulty (str): Niveau de difficulté
                - duration (int): Durée de la partie en secondes
                - result (str): Résultat de la partie ("victory" ou "defeat")
                - player_shots (int): Nombre de tirs du joueur
                - ai_shots (int): Nombre de tirs de l'IA
                - player_hits (int): Nombre de tirs réussis du joueur
                - ai_hits (int): Nombre de tirs réussis de l'IA
                - date (str): Date et heure de la partie
        """
        # Ajouter la date actuelle
        stats['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Ajouter les nouvelles stats à l'historique
        self.stats_history.append(stats)
        
        # Sauvegarder dans le fichier
        try:
            with open(self.save_file, 'w') as f:
                json.dump(self.stats_history, f, indent=2)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des statistiques : {e}")
    
    def get_stats_summary(self):
        """
        Génère un résumé des statistiques de toutes les parties.
        
        Returns:
            dict: Résumé des statistiques
                - total_games (int): Nombre total de parties
                - victories (int): Nombre de victoires
                - avg_duration (float): Durée moyenne des parties
                - best_time (int): Meilleur temps pour une victoire
                - stats_by_difficulty (dict): Statistiques par niveau de difficulté
        """
        if not self.stats_history:
            return None
        
        summary = {
            'total_games': len(self.stats_history),
            'victories': sum(1 for game in self.stats_history if game['result'] == 'victory'),
            'stats_by_difficulty': {}
        }
        
        # Calculer les statistiques par difficulté
        for difficulty in ['facile', 'moyen', 'difficile']:
            diff_games = [game for game in self.stats_history if game['difficulty'] == difficulty]
            if diff_games:
                wins = sum(1 for game in diff_games if game['result'] == 'victory')
                summary['stats_by_difficulty'][difficulty] = {
                    'total_games': len(diff_games),
                    'victories': wins,
                    'win_rate': round(wins / len(diff_games) * 100, 2),
                    'avg_duration': sum(game['duration'] for game in diff_games) / len(diff_games)
                }
        
        # Calculer le meilleur temps (victoires uniquement)
        victory_games = [game for game in self.stats_history if game['result'] == 'victory']
        if victory_games:
            summary['best_time'] = min(game['duration'] for game in victory_games)
        
        return summary
