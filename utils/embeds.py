"""
Embed templates for Discord messages
"""
import discord
from datetime import datetime
import config

def create_embed(title: str, description: str, color: int = config.COLOR_INFO) -> discord.Embed:
    """Create a basic embed"""
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=datetime.now()
    )
    return embed

def success_embed(title: str, description: str) -> discord.Embed:
    """Create a success embed"""
    return create_embed(title, description, config.COLOR_SUCCESS)

def error_embed(title: str, description: str) -> discord.Embed:
    """Create an error embed"""
    return create_embed(title, description, config.COLOR_ERROR)

def info_embed(title: str, description: str) -> discord.Embed:
    """Create an info embed"""
    return create_embed(title, description, config.COLOR_INFO)

def gambling_embed(title: str, description: str) -> discord.Embed:
    """Create a gambling-themed embed"""
    return create_embed(title, description, config.COLOR_GAMBLING)

def balance_embed(user: discord.User, balance: int) -> discord.Embed:
    """Create a balance display embed"""
    embed = discord.Embed(
        title=f"{config.EMOJI_COIN} Balance de {user.display_name}",
        description=f"**{balance:,}** coins",
        color=config.COLOR_INFO,
        timestamp=datetime.now()
    )
    embed.set_thumbnail(url=user.display_avatar.url)
    return embed

def game_result_embed(game_name: str, won: bool, bet: int, payout: int, new_balance: int, details: str = "") -> discord.Embed:
    """Create a game result embed"""
    if won:
        title = f"{config.EMOJI_WIN} Victoire au {game_name}!"
        color = config.COLOR_SUCCESS
        profit = payout - bet
        result_text = f"**+{profit:,}** coins"
    else:
        title = f"{config.EMOJI_LOSE} Défaite au {game_name}"
        color = config.COLOR_ERROR
        result_text = f"**-{bet:,}** coins"
    
    description = f"{details}\n\n"
    description += f"Mise: **{bet:,}** coins\n"
    description += f"Résultat: {result_text}\n"
    description += f"Nouveau solde: **{new_balance:,}** coins"
    
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=datetime.now()
    )
    return embed

def leaderboard_embed(leaderboard_data: list, bot) -> discord.Embed:
    """Create a leaderboard embed"""
    embed = discord.Embed(
        title=f"{config.EMOJI_CHART} Classement des joueurs",
        description="Top 10 des joueurs les plus riches",
        color=config.COLOR_GAMBLING,
        timestamp=datetime.now()
    )
    
    medals = ["🥇", "🥈", "🥉"]
    
    for idx, (user_id, balance, total_won, total_lost, games_played) in enumerate(leaderboard_data, 1):
        medal = medals[idx - 1] if idx <= 3 else f"**{idx}.**"
        user = bot.get_user(user_id)
        username = user.display_name if user else f"User {user_id}"
        
        embed.add_field(
            name=f"{medal} {username}",
            value=f"{config.EMOJI_COIN} **{balance:,}** coins\n{games_played} parties jouées",
            inline=False
        )
    
    return embed

def stats_embed(user: discord.User, stats: dict) -> discord.Embed:
    """Create a user statistics embed"""
    embed = discord.Embed(
        title=f"📊 Statistiques de {user.display_name}",
        color=config.COLOR_INFO,
        timestamp=datetime.now()
    )
    embed.set_thumbnail(url=user.display_avatar.url)
    
    # Balance info
    embed.add_field(
        name=f"{config.EMOJI_COIN} Balance",
        value=f"**{stats['balance']:,}** coins",
        inline=True
    )
    
    # Games played
    embed.add_field(
        name="🎮 Parties jouées",
        value=f"**{stats['games_played']}**",
        inline=True
    )
    
    # Net profit
    net_profit = stats['net_profit']
    profit_emoji = "📈" if net_profit >= 0 else "📉"
    embed.add_field(
        name=f"{profit_emoji} Profit net",
        value=f"**{net_profit:+,}** coins",
        inline=True
    )
    
    # Total won
    embed.add_field(
        name=f"{config.EMOJI_WIN} Total gagné",
        value=f"**{stats['total_won']:,}** coins",
        inline=True
    )
    
    # Total lost
    embed.add_field(
        name=f"{config.EMOJI_LOSE} Total perdu",
        value=f"**{stats['total_lost']:,}** coins",
        inline=True
    )
    
    # Win rate
    if stats['games_played'] > 0:
        win_rate = (stats['total_won'] / (stats['total_won'] + stats['total_lost']) * 100) if (stats['total_won'] + stats['total_lost']) > 0 else 0
        embed.add_field(
            name="📊 Taux de réussite",
            value=f"**{win_rate:.1f}%**",
            inline=True
        )
    
    # Game breakdown
    if stats['game_counts']:
        games_text = "\n".join([f"• {game}: {count} parties" for game, count in stats['game_counts'].items()])
        embed.add_field(
            name="🎲 Jeux joués",
            value=games_text,
            inline=False
        )
    
    return embed
