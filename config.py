"""
Configuration file for the gambling bot

Ce fichier contient toutes les configurations du bot.
Il charge les variables d'environnement depuis le fichier .env
et définit les constantes utilisées dans tout le projet.
"""

import os
from dotenv import load_dotenv

# Charge les variables d'environnement depuis le fichier .env
# Le fichier .env contient des informations sensibles comme le token Discord
load_dotenv()

# ============================================================================
# CONFIGURATION DISCORD
# ============================================================================

# Token du bot Discord (récupéré depuis la variable d'environnement)
# Ce token permet au bot de se connecter à Discord
# ⚠️ NE JAMAIS partager ce token publiquement!
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Préfixe des commandes (par défaut: /)
# Avec discord.py 2.0+, on utilise les slash commands donc ce préfixe est moins important
PREFIX = os.getenv('PREFIX', '/')

# ============================================================================
# CONFIGURATION DE L'ÉCONOMIE
# ============================================================================

# Balance de départ pour les nouveaux utilisateurs
# Quand un utilisateur utilise le bot pour la première fois, il reçoit ce montant
STARTING_BALANCE = int(os.getenv('STARTING_BALANCE', 1000))

# Récompense quotidienne (commande /daily)
# Les utilisateurs peuvent réclamer cette récompense une fois toutes les 24 heures
DAILY_REWARD = int(os.getenv('DAILY_REWARD', 500))

# ============================================================================
# CONFIGURATION DES JEUX
# ============================================================================

# Mise minimum pour tous les jeux
# Les joueurs ne peuvent pas parier moins que cette valeur
MIN_BET = 10

# Mise maximum pour tous les jeux
# Limite les paris pour éviter que les joueurs perdent trop d'un coup
MAX_BET = 10000

# ============================================================================
# CONFIGURATION DE LA BASE DE DONNÉES
# ============================================================================

# Chemin vers le fichier de base de données SQLite
# La base de données stocke toutes les informations des utilisateurs
DATABASE_PATH = 'database/gambling.db'

# ============================================================================
# COULEURS POUR LES EMBEDS DISCORD
# ============================================================================
# Les embeds sont les messages colorés et formatés que le bot envoie
# Les couleurs sont en format hexadécimal (0xRRGGBB)

COLOR_SUCCESS = 0x00ff00    # Vert - Pour les victoires et succès
COLOR_ERROR = 0xff0000      # Rouge - Pour les erreurs et défaites
COLOR_INFO = 0x3498db       # Bleu - Pour les informations générales
COLOR_WARNING = 0xffa500    # Orange - Pour les avertissements
COLOR_GAMBLING = 0xffd700   # Or - Pour les messages liés aux jeux

# ============================================================================
# EMOJIS
# ============================================================================
# Emojis utilisés dans les messages du bot pour rendre l'interface plus visuelle

EMOJI_COIN = "🪙"       # Représente la monnaie virtuelle
EMOJI_WIN = "🎉"        # Affiché quand le joueur gagne
EMOJI_LOSE = "😢"       # Affiché quand le joueur perd
EMOJI_DICE = "🎲"       # Pour le jeu de dés
EMOJI_SLOTS = "🎰"      # Pour la machine à sous
EMOJI_CARDS = "🃏"      # Pour le blackjack
EMOJI_ROULETTE = "🎡"   # Pour la roulette
EMOJI_CHART = "📊"      # Pour les statistiques et classements
