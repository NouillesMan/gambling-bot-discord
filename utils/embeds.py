"""
Embed templates for Discord messages

Ce fichier contient toutes les fonctions pour créer des embeds Discord.
Les embeds sont des messages formatés et colorés qui rendent le bot plus professionnel.

Un embed peut contenir:
- Un titre
- Une description
- Des champs (fields)
- Une couleur
- Une image/thumbnail
- Un footer
- Un timestamp
"""

import discord
from datetime import datetime
import config

def create_embed(title: str, description: str, color: int = config.COLOR_INFO) -> discord.Embed:
    """
    Crée un embed Discord de base
    
    Cette fonction est la base pour tous les autres embeds.
    Elle crée un embed avec un titre, une description, une couleur et un timestamp.
    
    Args:
        title: Le titre de l'embed (texte en gras en haut)
        description: La description de l'embed (texte principal)
        color: La couleur de la barre latérale (en hexadécimal)
        
    Returns:
        Un objet discord.Embed prêt à être envoyé
    """
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=datetime.now()  # Ajoute l'heure actuelle en bas de l'embed
    )
    return embed

def success_embed(title: str, description: str) -> discord.Embed:
    """
    Crée un embed de succès (vert)
    
    Utilisé pour afficher les victoires, les succès, les confirmations.
    
    Args:
        title: Le titre de l'embed
        description: La description de l'embed
        
    Returns:
        Un embed vert
    """
    return create_embed(title, description, config.COLOR_SUCCESS)

def error_embed(title: str, description: str) -> discord.Embed:
    """
    Crée un embed d'erreur (rouge)
    
    Utilisé pour afficher les erreurs, les défaites, les problèmes.
    
    Args:
        title: Le titre de l'embed
        description: La description de l'embed
        
    Returns:
        Un embed rouge
    """
    return create_embed(title, description, config.COLOR_ERROR)

def info_embed(title: str, description: str) -> discord.Embed:
    """
    Crée un embed d'information (bleu)
    
    Utilisé pour afficher des informations générales, des statistiques.
    
    Args:
        title: Le titre de l'embed
        description: La description de l'embed
        
    Returns:
        Un embed bleu
    """
    return create_embed(title, description, config.COLOR_INFO)

def gambling_embed(title: str, description: str) -> discord.Embed:
    """
    Crée un embed sur le thème du gambling (or)
    
    Utilisé pour les messages liés aux jeux de gambling.
    
    Args:
        title: Le titre de l'embed
        description: La description de l'embed
        
    Returns:
        Un embed doré
    """
    return create_embed(title, description, config.COLOR_GAMBLING)

def balance_embed(user: discord.User, balance: int) -> discord.Embed:
    """
    Crée un embed pour afficher la balance d'un utilisateur
    
    Affiche la balance avec l'avatar de l'utilisateur comme thumbnail.
    
    Args:
        user: L'objet utilisateur Discord
        balance: La balance de l'utilisateur en coins
        
    Returns:
        Un embed affichant la balance
    """
    embed = discord.Embed(
        title=f"{config.EMOJI_COIN} Balance de {user.display_name}",
        description=f"**{balance:,}** coins",  # :, ajoute des séparateurs de milliers (1,000 au lieu de 1000)
        color=config.COLOR_INFO,
        timestamp=datetime.now()
    )
    # Ajoute l'avatar de l'utilisateur comme petite image dans le coin
    embed.set_thumbnail(url=user.display_avatar.url)
    return embed

def game_result_embed(game_name: str, won: bool, bet: int, payout: int, new_balance: int, details: str = "") -> discord.Embed:
    """
    Crée un embed pour afficher le résultat d'une partie
    
    Cet embed est utilisé après chaque jeu pour montrer:
    - Si le joueur a gagné ou perdu
    - Le montant parié
    - Le gain ou la perte
    - La nouvelle balance
    - Des détails spécifiques au jeu
    
    Args:
        game_name: Le nom du jeu (Coinflip, Dice, Slots, etc.)
        won: True si le joueur a gagné, False sinon
        bet: Le montant parié
        payout: Le montant gagné (0 si perte)
        new_balance: La nouvelle balance après la partie
        details: Détails spécifiques au jeu (résultat des dés, symboles des slots, etc.)
        
    Returns:
        Un embed vert (victoire) ou rouge (défaite)
    """
    if won:
        # Le joueur a gagné
        title = f"{config.EMOJI_WIN} Victoire au {game_name}!"
        color = config.COLOR_SUCCESS
        profit = payout - bet  # Calcule le profit net (gain - mise)
        result_text = f"**+{profit:,}** coins"
    else:
        # Le joueur a perdu
        title = f"{config.EMOJI_LOSE} Défaite au {game_name}"
        color = config.COLOR_ERROR
        result_text = f"**-{bet:,}** coins"
    
    # Construit la description avec toutes les informations
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
    """
    Crée un embed pour afficher le classement des joueurs
    
    Affiche les 10 joueurs les plus riches avec leurs statistiques.
    Les 3 premiers ont des médailles (🥇🥈🥉).
    
    Args:
        leaderboard_data: Liste de tuples (user_id, balance, total_won, total_lost, games_played)
        bot: L'instance du bot (pour récupérer les noms des utilisateurs)
        
    Returns:
        Un embed avec le classement
    """
    embed = discord.Embed(
        title=f"{config.EMOJI_CHART} Classement des joueurs",
        description="Top 10 des joueurs les plus riches",
        color=config.COLOR_GAMBLING,
        timestamp=datetime.now()
    )
    
    # Médailles pour les 3 premiers
    medals = ["🥇", "🥈", "🥉"]
    
    # Parcourt chaque joueur dans le classement
    for idx, (user_id, balance, total_won, total_lost, games_played) in enumerate(leaderboard_data, 1):
        # Détermine la médaille ou le numéro
        medal = medals[idx - 1] if idx <= 3 else f"**{idx}.**"
        
        # Récupère l'utilisateur Discord
        user = bot.get_user(user_id)
        username = user.display_name if user else f"User {user_id}"
        
        # Ajoute un champ pour ce joueur
        embed.add_field(
            name=f"{medal} {username}",
            value=f"{config.EMOJI_COIN} **{balance:,}** coins\n{games_played} parties jouées",
            inline=False  # Chaque joueur sur une ligne séparée
        )
    
    return embed

def stats_embed(user: discord.User, stats: dict) -> discord.Embed:
    """
    Crée un embed pour afficher les statistiques détaillées d'un utilisateur
    
    Affiche toutes les statistiques:
    - Balance actuelle
    - Nombre de parties jouées
    - Profit net
    - Total gagné et perdu
    - Taux de réussite
    - Répartition des jeux joués
    
    Args:
        user: L'objet utilisateur Discord
        stats: Dictionnaire contenant toutes les statistiques
        
    Returns:
        Un embed avec toutes les statistiques
    """
    embed = discord.Embed(
        title=f"📊 Statistiques de {user.display_name}",
        color=config.COLOR_INFO,
        timestamp=datetime.now()
    )
    embed.set_thumbnail(url=user.display_avatar.url)
    
    # Balance actuelle
    embed.add_field(
        name=f"{config.EMOJI_COIN} Balance",
        value=f"**{stats['balance']:,}** coins",
        inline=True  # Affiche sur la même ligne que le champ suivant
    )
    
    # Nombre de parties jouées
    embed.add_field(
        name="🎮 Parties jouées",
        value=f"**{stats['games_played']}**",
        inline=True
    )
    
    # Profit net (peut être positif ou négatif)
    net_profit = stats['net_profit']
    profit_emoji = "📈" if net_profit >= 0 else "📉"  # Flèche montante ou descendante
    embed.add_field(
        name=f"{profit_emoji} Profit net",
        value=f"**{net_profit:+,}** coins",  # :+ affiche le signe + pour les nombres positifs
        inline=True
    )
    
    # Total gagné
    embed.add_field(
        name=f"{config.EMOJI_WIN} Total gagné",
        value=f"**{stats['total_won']:,}** coins",
        inline=True
    )
    
    # Total perdu
    embed.add_field(
        name=f"{config.EMOJI_LOSE} Total perdu",
        value=f"**{stats['total_lost']:,}** coins",
        inline=True
    )
    
    # Taux de réussite (pourcentage de gains par rapport aux pertes)
    if stats['games_played'] > 0:
        # Calcule le taux de réussite basé sur l'argent gagné vs perdu
        if (stats['total_won'] + stats['total_lost']) > 0:
            win_rate = (stats['total_won'] / (stats['total_won'] + stats['total_lost']) * 100)
        else:
            win_rate = 0
        
        embed.add_field(
            name="📊 Taux de réussite",
            value=f"**{win_rate:.1f}%**",  # :.1f affiche un chiffre après la virgule
            inline=True
        )
    
    # Répartition des jeux joués
    if stats['game_counts']:
        # Crée une liste formatée des jeux joués
        games_text = "\n".join([f"• {game}: {count} parties" for game, count in stats['game_counts'].items()])
        embed.add_field(
            name="🎲 Jeux joués",
            value=games_text,
            inline=False  # Prend toute la largeur
        )
    
    return embed
