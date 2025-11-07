"""
Database manager for the gambling bot

Ce fichier gère toutes les interactions avec la base de données SQLite.
Il utilise aiosqlite pour des opérations asynchrones (non-bloquantes).

La base de données stocke:
- Les informations des utilisateurs (balance, statistiques)
- L'historique des parties jouées
"""

import aiosqlite
import os
from datetime import datetime, timedelta
from typing import Optional, List, Tuple
import config

class DatabaseManager:
    """
    Gestionnaire de base de données pour le bot de gambling
    
    Cette classe gère toutes les opérations de base de données:
    - Création et initialisation des tables
    - Gestion des utilisateurs (création, récupération, mise à jour)
    - Gestion de la balance (ajout, retrait, consultation)
    - Enregistrement de l'historique des jeux
    - Statistiques et classements
    """
    
    def __init__(self, db_path: str = config.DATABASE_PATH):
        """
        Initialise le gestionnaire de base de données
        
        Args:
            db_path: Chemin vers le fichier de base de données SQLite
        """
        self.db_path = db_path
        self._ensure_directory()
    
    def _ensure_directory(self):
        """
        S'assure que le dossier de la base de données existe
        
        Crée le dossier 'database/' si il n'existe pas encore.
        Cela évite une erreur si on essaie de créer le fichier .db
        dans un dossier inexistant.
        """
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    async def initialize(self):
        """
        Initialise la base de données avec les tables nécessaires
        
        Cette fonction est appelée au démarrage du bot.
        Elle crée les tables si elles n'existent pas encore.
        
        Tables créées:
        - users: Stocke les informations des utilisateurs
        - game_history: Stocke l'historique de toutes les parties jouées
        """
        async with aiosqlite.connect(self.db_path) as db:
            # Table des utilisateurs
            # Stocke toutes les informations liées à chaque utilisateur
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,           -- ID Discord de l'utilisateur (unique)
                    balance INTEGER DEFAULT 0,             -- Balance actuelle en coins
                    total_won INTEGER DEFAULT 0,           -- Total de coins gagnés (toutes parties)
                    total_lost INTEGER DEFAULT 0,          -- Total de coins perdus (toutes parties)
                    games_played INTEGER DEFAULT 0,        -- Nombre total de parties jouées
                    last_daily TEXT,                       -- Date de la dernière récompense quotidienne
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP  -- Date de création du compte
                )
            """)
            
            # Table de l'historique des jeux
            # Enregistre chaque partie jouée pour les statistiques
            await db.execute("""
                CREATE TABLE IF NOT EXISTS game_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, -- ID unique de la partie
                    user_id INTEGER,                      -- ID de l'utilisateur qui a joué
                    game_type TEXT,                       -- Type de jeu (coinflip, dice, slots, etc.)
                    bet_amount INTEGER,                   -- Montant parié
                    result INTEGER,                       -- Résultat (positif = gain, négatif = perte)
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,  -- Date et heure de la partie
                    FOREIGN KEY (user_id) REFERENCES users (user_id)  -- Lien avec la table users
                )
            """)
            
            # Sauvegarde les changements dans la base de données
            await db.commit()
    
    async def get_user(self, user_id: int) -> Optional[dict]:
        """
        Récupère les données d'un utilisateur depuis la base de données
        
        Args:
            user_id: L'ID Discord de l'utilisateur
            
        Returns:
            Un dictionnaire contenant les données de l'utilisateur, ou None si non trouvé
            Exemple: {'user_id': 123, 'balance': 1000, 'total_won': 500, ...}
        """
        async with aiosqlite.connect(self.db_path) as db:
            # row_factory permet de récupérer les résultats sous forme de dictionnaire
            db.row_factory = aiosqlite.Row
            
            async with db.execute(
                "SELECT * FROM users WHERE user_id = ?", (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                # Convertit la Row en dictionnaire, ou retourne None si pas trouvé
                return dict(row) if row else None
    
    async def create_user(self, user_id: int) -> dict:
        """
        Crée un nouvel utilisateur dans la base de données
        
        Quand quelqu'un utilise le bot pour la première fois,
        cette fonction crée son compte avec la balance de départ.
        
        Args:
            user_id: L'ID Discord de l'utilisateur
            
        Returns:
            Un dictionnaire contenant les données du nouvel utilisateur
        """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO users (user_id, balance) VALUES (?, ?)",
                (user_id, config.STARTING_BALANCE)
            )
            await db.commit()
        
        # Récupère et retourne les données du nouvel utilisateur
        return await self.get_user(user_id)
    
    async def get_or_create_user(self, user_id: int) -> dict:
        """
        Récupère un utilisateur ou le crée s'il n'existe pas
        
        Cette fonction est très utile car elle garantit qu'on a toujours
        un utilisateur valide. Si l'utilisateur existe, on le récupère.
        Sinon, on le crée automatiquement.
        
        Args:
            user_id: L'ID Discord de l'utilisateur
            
        Returns:
            Un dictionnaire contenant les données de l'utilisateur
        """
        user = await self.get_user(user_id)
        if not user:
            user = await self.create_user(user_id)
        return user
    
    async def update_balance(self, user_id: int, amount: int) -> int:
        """
        Met à jour la balance d'un utilisateur (ajoute ou retire des coins)
        
        Args:
            user_id: L'ID Discord de l'utilisateur
            amount: Montant à ajouter (positif) ou retirer (négatif)
                   Exemple: +100 pour ajouter 100 coins, -50 pour retirer 50 coins
            
        Returns:
            La nouvelle balance de l'utilisateur après modification
        """
        async with aiosqlite.connect(self.db_path) as db:
            # UPDATE users SET balance = balance + amount
            # Si amount = +100, on ajoute 100 à la balance
            # Si amount = -50, on retire 50 de la balance
            await db.execute(
                "UPDATE users SET balance = balance + ? WHERE user_id = ?",
                (amount, user_id)
            )
            await db.commit()
            
            # Récupère et retourne la nouvelle balance
            async with db.execute(
                "SELECT balance FROM users WHERE user_id = ?", (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                return row[0] if row else 0
    
    async def set_balance(self, user_id: int, amount: int):
        """
        Définit la balance d'un utilisateur à une valeur spécifique
        
        Contrairement à update_balance qui ajoute/retire,
        cette fonction définit directement la balance à une valeur exacte.
        Utilisée principalement par les commandes admin.
        
        Args:
            user_id: L'ID Discord de l'utilisateur
            amount: Le nouveau montant de la balance
        """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE users SET balance = ? WHERE user_id = ?",
                (amount, user_id)
            )
            await db.commit()
    
    async def get_balance(self, user_id: int) -> int:
        """
        Récupère la balance d'un utilisateur
        
        Args:
            user_id: L'ID Discord de l'utilisateur
            
        Returns:
            La balance actuelle de l'utilisateur en coins
        """
        user = await self.get_or_create_user(user_id)
        return user['balance']
    
    async def record_game(self, user_id: int, game_type: str, bet_amount: int, result: int):
        """
        Enregistre une partie dans l'historique et met à jour les statistiques
        
        Cette fonction est appelée après chaque partie jouée.
        Elle enregistre la partie dans l'historique et met à jour
        les statistiques de l'utilisateur (total gagné/perdu, parties jouées).
        
        Args:
            user_id: L'ID Discord de l'utilisateur
            game_type: Le type de jeu (coinflip, dice, slots, etc.)
            bet_amount: Le montant parié
            result: Le résultat (positif = gain, négatif = perte)
                   Exemple: +100 si le joueur a gagné 100 coins
                           -50 si le joueur a perdu 50 coins
        """
        async with aiosqlite.connect(self.db_path) as db:
            # Enregistre la partie dans l'historique
            await db.execute(
                "INSERT INTO game_history (user_id, game_type, bet_amount, result) VALUES (?, ?, ?, ?)",
                (user_id, game_type, bet_amount, result)
            )
            
            # Met à jour les statistiques de l'utilisateur
            if result > 0:
                # Le joueur a gagné: on ajoute au total_won
                await db.execute(
                    "UPDATE users SET total_won = total_won + ?, games_played = games_played + 1 WHERE user_id = ?",
                    (result, user_id)
                )
            else:
                # Le joueur a perdu: on ajoute au total_lost
                # abs() pour convertir le nombre négatif en positif
                await db.execute(
                    "UPDATE users SET total_lost = total_lost + ?, games_played = games_played + 1 WHERE user_id = ?",
                    (abs(result), user_id)
                )
            
            await db.commit()
    
    async def can_claim_daily(self, user_id: int) -> bool:
        """
        Vérifie si un utilisateur peut réclamer sa récompense quotidienne
        
        La récompense quotidienne peut être réclamée une fois toutes les 24 heures.
        
        Args:
            user_id: L'ID Discord de l'utilisateur
            
        Returns:
            True si l'utilisateur peut réclamer, False sinon
        """
        user = await self.get_or_create_user(user_id)
        
        # Si l'utilisateur n'a jamais réclamé, il peut réclamer
        if not user['last_daily']:
            return True
        
        # Convertit la date de la dernière réclamation en objet datetime
        last_daily = datetime.fromisoformat(user['last_daily'])
        now = datetime.now()
        
        # Vérifie si 24 heures se sont écoulées
        return (now - last_daily) >= timedelta(hours=24)
    
    async def claim_daily(self, user_id: int) -> int:
        """
        Réclame la récompense quotidienne pour un utilisateur
        
        Ajoute la récompense quotidienne à la balance et met à jour
        la date de la dernière réclamation.
        
        Args:
            user_id: L'ID Discord de l'utilisateur
            
        Returns:
            Le montant de la récompense reçue
        """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE users SET balance = balance + ?, last_daily = ? WHERE user_id = ?",
                (config.DAILY_REWARD, datetime.now().isoformat(), user_id)
            )
            await db.commit()
        
        return config.DAILY_REWARD
    
    async def get_leaderboard(self, limit: int = 10) -> List[Tuple]:
        """
        Récupère le classement des joueurs les plus riches
        
        Args:
            limit: Nombre de joueurs à récupérer (par défaut: 10)
            
        Returns:
            Une liste de tuples contenant (user_id, balance, total_won, total_lost, games_played)
            Triée par balance décroissante (du plus riche au moins riche)
        """
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT user_id, balance, total_won, total_lost, games_played FROM users ORDER BY balance DESC LIMIT ?",
                (limit,)
            ) as cursor:
                return await cursor.fetchall()
    
    def _get_connection(self):
        """
        Obtient une connexion à la base de données
        
        Cette méthode est utilisée par les commandes admin
        pour effectuer des opérations spéciales.
        
        Returns:
            Une connexion aiosqlite
        """
        return aiosqlite.connect(self.db_path)
    
    async def get_user_stats(self, user_id: int) -> dict:
        """
        Récupère les statistiques détaillées d'un utilisateur
        
        Cette fonction compile toutes les statistiques d'un utilisateur:
        - Balance actuelle
        - Total gagné et perdu
        - Nombre de parties jouées
        - Profit net (total gagné - total perdu)
        - Nombre de parties par type de jeu
        
        Args:
            user_id: L'ID Discord de l'utilisateur
            
        Returns:
            Un dictionnaire contenant toutes les statistiques
        """
        # Récupère les données de base de l'utilisateur
        user = await self.get_or_create_user(user_id)
        
        async with aiosqlite.connect(self.db_path) as db:
            # Compte le nombre de parties par type de jeu
            # Exemple de résultat: [('coinflip', 5), ('dice', 3), ('slots', 10)]
            async with db.execute(
                "SELECT game_type, COUNT(*) as count FROM game_history WHERE user_id = ? GROUP BY game_type",
                (user_id,)
            ) as cursor:
                game_counts = await cursor.fetchall()
        
        # Compile toutes les statistiques dans un dictionnaire
        return {
            'balance': user['balance'],
            'total_won': user['total_won'],
            'total_lost': user['total_lost'],
            'games_played': user['games_played'],
            'net_profit': user['total_won'] - user['total_lost'],  # Profit net (peut être négatif)
            'game_counts': dict(game_counts) if game_counts else {}  # Convertit en dictionnaire
        }
