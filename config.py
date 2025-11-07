"""
Configuration file for the gambling bot
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Discord Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('PREFIX', '/')

# Economy Configuration
STARTING_BALANCE = int(os.getenv('STARTING_BALANCE', 1000))
DAILY_REWARD = int(os.getenv('DAILY_REWARD', 500))

# Game Configuration
MIN_BET = 10
MAX_BET = 10000

# Database Configuration
DATABASE_PATH = 'database/gambling.db'

# Colors for embeds
COLOR_SUCCESS = 0x00ff00
COLOR_ERROR = 0xff0000
COLOR_INFO = 0x3498db
COLOR_WARNING = 0xffa500
COLOR_GAMBLING = 0xffd700

# Emojis
EMOJI_COIN = "🪙"
EMOJI_WIN = "🎉"
EMOJI_LOSE = "😢"
EMOJI_DICE = "🎲"
EMOJI_SLOTS = "🎰"
EMOJI_CARDS = "🃏"
EMOJI_ROULETTE = "🎡"
EMOJI_CHART = "📊"
