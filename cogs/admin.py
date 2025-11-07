"""
Admin cog
Contains administrative commands for bot management
"""
import discord
from discord import app_commands
from discord.ext import commands
import config
from utils.embeds import success_embed, error_embed, info_embed

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
    
    @app_commands.command(name="addcoins", description="[ADMIN] Ajouter des coins à un utilisateur")
    @app_commands.describe(
        utilisateur="L'utilisateur à qui ajouter des coins",
        montant="Montant à ajouter"
    )
    @app_commands.default_permissions(administrator=True)
    async def addcoins_command(self, interaction: discord.Interaction, utilisateur: discord.User, montant: int):
        """Add coins to a user (admin only)"""
        if montant <= 0:
            await interaction.response.send_message(
                embed=error_embed("❌ Erreur", "Le montant doit être positif!"),
                ephemeral=True
            )
            return
        
        await self.db.update_balance(utilisateur.id, montant)
        new_balance = await self.db.get_balance(utilisateur.id)
        
        embed = success_embed(
            f"{config.EMOJI_COIN} Coins ajoutés",
            f"**{montant:,}** coins ont été ajoutés à {utilisateur.mention}\n"
            f"Nouveau solde: **{new_balance:,}** coins"
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="removecoins", description="[ADMIN] Retirer des coins à un utilisateur")
    @app_commands.describe(
        utilisateur="L'utilisateur à qui retirer des coins",
        montant="Montant à retirer"
    )
    @app_commands.default_permissions(administrator=True)
    async def removecoins_command(self, interaction: discord.Interaction, utilisateur: discord.User, montant: int):
        """Remove coins from a user (admin only)"""
        if montant <= 0:
            await interaction.response.send_message(
                embed=error_embed("❌ Erreur", "Le montant doit être positif!"),
                ephemeral=True
            )
            return
        
        await self.db.update_balance(utilisateur.id, -montant)
        new_balance = await self.db.get_balance(utilisateur.id)
        
        embed = success_embed(
            f"{config.EMOJI_COIN} Coins retirés",
            f"**{montant:,}** coins ont été retirés à {utilisateur.mention}\n"
            f"Nouveau solde: **{new_balance:,}** coins"
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="setbalance", description="[ADMIN] Définir la balance d'un utilisateur")
    @app_commands.describe(
        utilisateur="L'utilisateur dont modifier la balance",
        montant="Nouveau montant de la balance"
    )
    @app_commands.default_permissions(administrator=True)
    async def setbalance_command(self, interaction: discord.Interaction, utilisateur: discord.User, montant: int):
        """Set user balance to a specific amount (admin only)"""
        if montant < 0:
            await interaction.response.send_message(
                embed=error_embed("❌ Erreur", "Le montant ne peut pas être négatif!"),
                ephemeral=True
            )
            return
        
        await self.db.set_balance(utilisateur.id, montant)
        
        embed = success_embed(
            f"{config.EMOJI_COIN} Balance modifiée",
            f"La balance de {utilisateur.mention} a été définie à **{montant:,}** coins"
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="resetuser", description="[ADMIN] Réinitialiser complètement un utilisateur")
    @app_commands.describe(utilisateur="L'utilisateur à réinitialiser")
    @app_commands.default_permissions(administrator=True)
    async def resetuser_command(self, interaction: discord.Interaction, utilisateur: discord.User):
        """Reset a user's data (admin only)"""
        await self.db.set_balance(utilisateur.id, config.STARTING_BALANCE)
        
        # Reset stats
        async with self.db._get_connection() as db:
            await db.execute(
                "UPDATE users SET total_won = 0, total_lost = 0, games_played = 0, last_daily = NULL WHERE user_id = ?",
                (utilisateur.id,)
            )
            await db.execute(
                "DELETE FROM game_history WHERE user_id = ?",
                (utilisateur.id,)
            )
            await db.commit()
        
        embed = success_embed(
            "🔄 Utilisateur réinitialisé",
            f"{utilisateur.mention} a été réinitialisé avec succès!\n"
            f"Balance: **{config.STARTING_BALANCE:,}** coins"
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="botstats", description="[ADMIN] Voir les statistiques globales du bot")
    @app_commands.default_permissions(administrator=True)
    async def botstats_command(self, interaction: discord.Interaction):
        """Show global bot statistics (admin only)"""
        async with self.db._get_connection() as db:
            # Total users
            async with db.execute("SELECT COUNT(*) FROM users") as cursor:
                total_users = (await cursor.fetchone())[0]
            
            # Total coins in circulation
            async with db.execute("SELECT SUM(balance) FROM users") as cursor:
                total_coins = (await cursor.fetchone())[0] or 0
            
            # Total games played
            async with db.execute("SELECT COUNT(*) FROM game_history") as cursor:
                total_games = (await cursor.fetchone())[0]
            
            # Total won/lost
            async with db.execute("SELECT SUM(total_won), SUM(total_lost) FROM users") as cursor:
                row = await cursor.fetchone()
                total_won = row[0] or 0
                total_lost = row[1] or 0
            
            # Most popular game
            async with db.execute(
                "SELECT game_type, COUNT(*) as count FROM game_history GROUP BY game_type ORDER BY count DESC LIMIT 1"
            ) as cursor:
                popular_game = await cursor.fetchone()
                most_popular = f"{popular_game[0]} ({popular_game[1]} parties)" if popular_game else "Aucun"
        
        embed = info_embed(
            "📊 Statistiques globales du bot",
            f"**Utilisateurs totaux:** {total_users:,}\n"
            f"**Coins en circulation:** {total_coins:,}\n"
            f"**Parties jouées:** {total_games:,}\n"
            f"**Total gagné:** {total_won:,} coins\n"
            f"**Total perdu:** {total_lost:,} coins\n"
            f"**Jeu le plus populaire:** {most_popular}\n\n"
            f"**Serveurs:** {len(self.bot.guilds)}\n"
            f"**Latence:** {round(self.bot.latency * 1000)}ms"
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Admin(bot))
