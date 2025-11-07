"""
Database manager for the gambling bot
Handles all database operations using aiosqlite
"""
import aiosqlite
import os
from datetime import datetime, timedelta
from typing import Optional, List, Tuple
import config

class DatabaseManager:
    def __init__(self, db_path: str = config.DATABASE_PATH):
        self.db_path = db_path
        self._ensure_directory()
    
    def _ensure_directory(self):
        """Ensure the database directory exists"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    async def initialize(self):
        """Initialize the database with required tables"""
        async with aiosqlite.connect(self.db_path) as db:
            # Users table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    balance INTEGER DEFAULT 0,
                    total_won INTEGER DEFAULT 0,
                    total_lost INTEGER DEFAULT 0,
                    games_played INTEGER DEFAULT 0,
                    last_daily TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Game history table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS game_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    game_type TEXT,
                    bet_amount INTEGER,
                    result INTEGER,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)
            
            await db.commit()
    
    async def get_user(self, user_id: int) -> Optional[dict]:
        """Get user data from database"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM users WHERE user_id = ?", (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                return dict(row) if row else None
    
    async def create_user(self, user_id: int) -> dict:
        """Create a new user with starting balance"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO users (user_id, balance) VALUES (?, ?)",
                (user_id, config.STARTING_BALANCE)
            )
            await db.commit()
        return await self.get_user(user_id)
    
    async def get_or_create_user(self, user_id: int) -> dict:
        """Get user or create if doesn't exist"""
        user = await self.get_user(user_id)
        if not user:
            user = await self.create_user(user_id)
        return user
    
    async def update_balance(self, user_id: int, amount: int) -> int:
        """Update user balance (can be positive or negative)"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE users SET balance = balance + ? WHERE user_id = ?",
                (amount, user_id)
            )
            await db.commit()
            
            # Get new balance
            async with db.execute(
                "SELECT balance FROM users WHERE user_id = ?", (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                return row[0] if row else 0
    
    async def set_balance(self, user_id: int, amount: int):
        """Set user balance to a specific amount"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE users SET balance = ? WHERE user_id = ?",
                (amount, user_id)
            )
            await db.commit()
    
    async def get_balance(self, user_id: int) -> int:
        """Get user balance"""
        user = await self.get_or_create_user(user_id)
        return user['balance']
    
    async def record_game(self, user_id: int, game_type: str, bet_amount: int, result: int):
        """Record a game in history and update user stats"""
        async with aiosqlite.connect(self.db_path) as db:
            # Record game
            await db.execute(
                "INSERT INTO game_history (user_id, game_type, bet_amount, result) VALUES (?, ?, ?, ?)",
                (user_id, game_type, bet_amount, result)
            )
            
            # Update user stats
            if result > 0:
                await db.execute(
                    "UPDATE users SET total_won = total_won + ?, games_played = games_played + 1 WHERE user_id = ?",
                    (result, user_id)
                )
            else:
                await db.execute(
                    "UPDATE users SET total_lost = total_lost + ?, games_played = games_played + 1 WHERE user_id = ?",
                    (abs(result), user_id)
                )
            
            await db.commit()
    
    async def can_claim_daily(self, user_id: int) -> bool:
        """Check if user can claim daily reward"""
        user = await self.get_or_create_user(user_id)
        if not user['last_daily']:
            return True
        
        last_daily = datetime.fromisoformat(user['last_daily'])
        now = datetime.now()
        return (now - last_daily) >= timedelta(hours=24)
    
    async def claim_daily(self, user_id: int) -> int:
        """Claim daily reward"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE users SET balance = balance + ?, last_daily = ? WHERE user_id = ?",
                (config.DAILY_REWARD, datetime.now().isoformat(), user_id)
            )
            await db.commit()
        return config.DAILY_REWARD
    
    async def get_leaderboard(self, limit: int = 10) -> List[Tuple]:
        """Get top users by balance"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT user_id, balance, total_won, total_lost, games_played FROM users ORDER BY balance DESC LIMIT ?",
                (limit,)
            ) as cursor:
                return await cursor.fetchall()
    
    def _get_connection(self):
        """Get database connection (for admin operations)"""
        return aiosqlite.connect(self.db_path)
    
    async def get_user_stats(self, user_id: int) -> dict:
        """Get detailed user statistics"""
        user = await self.get_or_create_user(user_id)
        
        async with aiosqlite.connect(self.db_path) as db:
            # Get game counts by type
            async with db.execute(
                "SELECT game_type, COUNT(*) as count FROM game_history WHERE user_id = ? GROUP BY game_type",
                (user_id,)
            ) as cursor:
                game_counts = await cursor.fetchall()
        
        return {
            'balance': user['balance'],
            'total_won': user['total_won'],
            'total_lost': user['total_lost'],
            'games_played': user['games_played'],
            'net_profit': user['total_won'] - user['total_lost'],
            'game_counts': dict(game_counts) if game_counts else {}
        }
