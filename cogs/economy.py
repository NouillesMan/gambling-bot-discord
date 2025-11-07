"""
Economy cog
Contains economy-related commands like balance, daily, leaderboard, etc.
"""
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta
import config
from utils.embeds import balance_embed, success_embed, error_embed, leaderboard_embed, stats_embed

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
    
    @app_commands.command(name="balance", description="Voir votre balance ou celle d'un autre utilisateur")
    @app_commands.describe(utilisateur="L'utilisateur dont vous voulez voir la balance (optionnel)")
    async def balance_command(self, interaction: discord.Interaction, utilisateur: discord.User = None):
        """Check user balance"""
        target_user = utilisateur or interaction.user
        balance = await self.db.get_balance(target_user.id)
        
        embed = balance_embed(target_user, balance)
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="daily", description="Réclamez votre récompense quotidienne")
    async def daily_command(self, interaction: discord.Interaction):
        """Claim daily reward"""
        user_id = interaction.user.id
        
        # Check if user can claim
        can_claim = await self.db.can_claim_daily(user_id)
        
        if not can_claim:
            user = await self.db.get_user(user_id)
            last_daily = datetime.fromisoformat(user['last_daily'])
            next_claim = last_daily + timedelta(hours=24)
            time_left = next_claim - datetime.now()
            
            hours = int(time_left.total_seconds() // 3600)
            minutes = int((time_left.total_seconds() % 3600) // 60)
            
            embed = error_embed(
                "⏰ Déjà réclamé",
                f"Vous avez déjà réclamé votre récompense quotidienne!\n"
                f"Revenez dans **{hours}h {minutes}m**"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Claim daily
        reward = await self.db.claim_daily(user_id)
        new_balance = await self.db.get_balance(user_id)
        
        embed = success_embed(
            f"{config.EMOJI_COIN} Récompense quotidienne",
            f"Vous avez reçu **{reward:,}** coins!\n"
            f"Nouveau solde: **{new_balance:,}** coins\n\n"
            f"Revenez dans 24 heures pour votre prochaine récompense!"
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="leaderboard", description="Voir le classement des joueurs les plus riches")
    async def leaderboard_command(self, interaction: discord.Interaction):
        """Show leaderboard"""
        leaderboard_data = await self.db.get_leaderboard(10)
        
        if not leaderboard_data:
            embed = error_embed("📊 Classement", "Aucun joueur trouvé!")
            await interaction.response.send_message(embed=embed)
            return
        
        embed = leaderboard_embed(leaderboard_data, self.bot)
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="stats", description="Voir vos statistiques ou celles d'un autre utilisateur")
    @app_commands.describe(utilisateur="L'utilisateur dont vous voulez voir les stats (optionnel)")
    async def stats_command(self, interaction: discord.Interaction, utilisateur: discord.User = None):
        """Show user statistics"""
        target_user = utilisateur or interaction.user
        stats = await self.db.get_user_stats(target_user.id)
        
        embed = stats_embed(target_user, stats)
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="give", description="Donner des coins à un autre utilisateur")
    @app_commands.describe(
        utilisateur="L'utilisateur à qui donner des coins",
        montant="Montant à donner"
    )
    async def give_command(self, interaction: discord.Interaction, utilisateur: discord.User, montant: int):
        """Give coins to another user"""
        giver_id = interaction.user.id
        receiver_id = utilisateur.id
        
        # Check if trying to give to self
        if giver_id == receiver_id:
            await interaction.response.send_message(
                embed=error_embed("❌ Erreur", "Vous ne pouvez pas vous donner des coins à vous-même!"),
                ephemeral=True
            )
            return
        
        # Check if amount is positive
        if montant <= 0:
            await interaction.response.send_message(
                embed=error_embed("❌ Erreur", "Le montant doit être positif!"),
                ephemeral=True
            )
            return
        
        # Check if giver has enough balance
        giver_balance = await self.db.get_balance(giver_id)
        if giver_balance < montant:
            await interaction.response.send_message(
                embed=error_embed("❌ Erreur", f"Vous n'avez pas assez de coins! Balance: **{giver_balance:,}** coins"),
                ephemeral=True
            )
            return
        
        # Transfer coins
        await self.db.update_balance(giver_id, -montant)
        await self.db.update_balance(receiver_id, montant)
        
        new_balance = await self.db.get_balance(giver_id)
        
        embed = success_embed(
            f"{config.EMOJI_COIN} Don effectué",
            f"Vous avez donné **{montant:,}** coins à {utilisateur.mention}!\n"
            f"Votre nouveau solde: **{new_balance:,}** coins"
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Economy(bot))
