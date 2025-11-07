"""
Gambling games cog
Contains all gambling game commands
"""
import discord
from discord import app_commands
from discord.ext import commands
import config
from utils.embeds import game_result_embed, gambling_embed, error_embed
from utils.helpers import (
    validate_bet, coinflip, roll_dice, spin_slots, 
    spin_roulette, BlackjackGame, crash_game
)

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
    
    @app_commands.command(name="coinflip", description="Pariez sur pile ou face")
    @app_commands.describe(
        choix="Choisissez pile ou face",
        mise="Montant à parier"
    )
    @app_commands.choices(choix=[
        app_commands.Choice(name="Pile", value="pile"),
        app_commands.Choice(name="Face", value="face")
    ])
    async def coinflip_command(self, interaction: discord.Interaction, choix: app_commands.Choice[str], mise: int):
        """Coinflip gambling game"""
        user_id = interaction.user.id
        balance = await self.db.get_balance(user_id)
        
        # Validate bet
        is_valid, error_msg = validate_bet(balance, mise)
        if not is_valid:
            await interaction.response.send_message(embed=error_embed("❌ Erreur", error_msg), ephemeral=True)
            return
        
        # Play game
        won, result = coinflip(choix.value)
        
        if won:
            payout = mise * 2
            await self.db.update_balance(user_id, mise)
            await self.db.record_game(user_id, "coinflip", mise, mise)
        else:
            payout = 0
            await self.db.update_balance(user_id, -mise)
            await self.db.record_game(user_id, "coinflip", mise, -mise)
        
        new_balance = await self.db.get_balance(user_id)
        
        result_emoji = "🪙" if result == "pile" else "🎴"
        details = f"Vous avez choisi: **{choix.name}**\nRésultat: {result_emoji} **{result.capitalize()}**"
        
        embed = game_result_embed("Coinflip", won, mise, payout, new_balance, details)
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="dice", description="Lancez les dés et gagnez selon le résultat")
    @app_commands.describe(mise="Montant à parier")
    async def dice_command(self, interaction: discord.Interaction, mise: int):
        """Dice gambling game"""
        user_id = interaction.user.id
        balance = await self.db.get_balance(user_id)
        
        # Validate bet
        is_valid, error_msg = validate_bet(balance, mise)
        if not is_valid:
            await interaction.response.send_message(embed=error_embed("❌ Erreur", error_msg), ephemeral=True)
            return
        
        # Roll dice
        dice = roll_dice(2)
        total = sum(dice)
        
        # Determine multiplier
        if total == 12:  # Double 6
            multiplier = 10
            won = True
        elif total == 2:  # Double 1
            multiplier = 5
            won = True
        elif total >= 10:
            multiplier = 3
            won = True
        elif total >= 7:
            multiplier = 1.5
            won = True
        else:
            multiplier = 0
            won = False
        
        if won:
            payout = int(mise * multiplier)
            profit = payout - mise
            await self.db.update_balance(user_id, profit)
            await self.db.record_game(user_id, "dice", mise, profit)
        else:
            payout = 0
            await self.db.update_balance(user_id, -mise)
            await self.db.record_game(user_id, "dice", mise, -mise)
        
        new_balance = await self.db.get_balance(user_id)
        
        details = f"{config.EMOJI_DICE} Dés: **{dice[0]}** + **{dice[1]}** = **{total}**\n"
        if won:
            details += f"Multiplicateur: **x{multiplier}**"
        
        embed = game_result_embed("Dice", won, mise, payout, new_balance, details)
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="slots", description="Jouez à la machine à sous")
    @app_commands.describe(mise="Montant à parier")
    async def slots_command(self, interaction: discord.Interaction, mise: int):
        """Slot machine gambling game"""
        user_id = interaction.user.id
        balance = await self.db.get_balance(user_id)
        
        # Validate bet
        is_valid, error_msg = validate_bet(balance, mise)
        if not is_valid:
            await interaction.response.send_message(embed=error_embed("❌ Erreur", error_msg), ephemeral=True)
            return
        
        # Spin slots
        symbols, multiplier = spin_slots()
        won = multiplier > 0
        
        if won:
            payout = int(mise * multiplier)
            profit = payout - mise
            await self.db.update_balance(user_id, profit)
            await self.db.record_game(user_id, "slots", mise, profit)
        else:
            payout = 0
            await self.db.update_balance(user_id, -mise)
            await self.db.record_game(user_id, "slots", mise, -mise)
        
        new_balance = await self.db.get_balance(user_id)
        
        details = f"{config.EMOJI_SLOTS} **{symbols[0]} | {symbols[1]} | {symbols[2]}**\n"
        if won:
            details += f"Multiplicateur: **x{multiplier}**"
            if multiplier >= 20:
                details += " 🎊 **JACKPOT!** 🎊"
        
        embed = game_result_embed("Slots", won, mise, payout, new_balance, details)
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="roulette", description="Pariez à la roulette")
    @app_commands.describe(
        type_pari="Type de pari",
        mise="Montant à parier"
    )
    @app_commands.choices(type_pari=[
        app_commands.Choice(name="Rouge (x2)", value="rouge"),
        app_commands.Choice(name="Noir (x2)", value="noir"),
        app_commands.Choice(name="Vert (x36)", value="vert"),
        app_commands.Choice(name="Pair (x2)", value="pair"),
        app_commands.Choice(name="Impair (x2)", value="impair")
    ])
    async def roulette_command(self, interaction: discord.Interaction, type_pari: app_commands.Choice[str], mise: int):
        """Roulette gambling game"""
        user_id = interaction.user.id
        balance = await self.db.get_balance(user_id)
        
        # Validate bet
        is_valid, error_msg = validate_bet(balance, mise)
        if not is_valid:
            await interaction.response.send_message(embed=error_embed("❌ Erreur", error_msg), ephemeral=True)
            return
        
        # Spin roulette
        won, multiplier, result = spin_roulette(type_pari.value)
        
        if won:
            payout = int(mise * multiplier)
            profit = payout - mise
            await self.db.update_balance(user_id, profit)
            await self.db.record_game(user_id, "roulette", mise, profit)
        else:
            payout = 0
            await self.db.update_balance(user_id, -mise)
            await self.db.record_game(user_id, "roulette", mise, -mise)
        
        new_balance = await self.db.get_balance(user_id)
        
        details = f"{config.EMOJI_ROULETTE} Vous avez parié sur: **{type_pari.name}**\n"
        details += f"Résultat: {result}"
        
        embed = game_result_embed("Roulette", won, mise, payout, new_balance, details)
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="blackjack", description="Jouez au Blackjack contre le croupier")
    @app_commands.describe(mise="Montant à parier")
    async def blackjack_command(self, interaction: discord.Interaction, mise: int):
        """Blackjack gambling game"""
        user_id = interaction.user.id
        balance = await self.db.get_balance(user_id)
        
        # Validate bet
        is_valid, error_msg = validate_bet(balance, mise)
        if not is_valid:
            await interaction.response.send_message(embed=error_embed("❌ Erreur", error_msg), ephemeral=True)
            return
        
        # Play blackjack
        game = BlackjackGame()
        won, description, multiplier = game.play()
        
        if multiplier > 0:
            payout = int(mise * multiplier)
            profit = payout - mise
            await self.db.update_balance(user_id, profit)
            await self.db.record_game(user_id, "blackjack", mise, profit)
        else:
            payout = 0
            await self.db.update_balance(user_id, -mise)
            await self.db.record_game(user_id, "blackjack", mise, -mise)
        
        new_balance = await self.db.get_balance(user_id)
        
        details = f"{config.EMOJI_CARDS}\n{description}"
        
        embed = game_result_embed("Blackjack", won, mise, payout, new_balance, details)
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="crash", description="Pariez sur un multiplicateur avant le crash")
    @app_commands.describe(
        mise="Montant à parier",
        multiplicateur="Multiplicateur de retrait (ex: 2.0 pour x2)"
    )
    async def crash_command(self, interaction: discord.Interaction, mise: int, multiplicateur: float):
        """Crash gambling game"""
        user_id = interaction.user.id
        balance = await self.db.get_balance(user_id)
        
        # Validate bet
        is_valid, error_msg = validate_bet(balance, mise)
        if not is_valid:
            await interaction.response.send_message(embed=error_embed("❌ Erreur", error_msg), ephemeral=True)
            return
        
        # Validate multiplier
        if multiplicateur < 1.01 or multiplicateur > 100:
            await interaction.response.send_message(
                embed=error_embed("❌ Erreur", "Le multiplicateur doit être entre 1.01 et 100!"),
                ephemeral=True
            )
            return
        
        # Play crash game
        won, crash_point = crash_game(multiplicateur)
        
        if won:
            payout = int(mise * multiplicateur)
            profit = payout - mise
            await self.db.update_balance(user_id, profit)
            await self.db.record_game(user_id, "crash", mise, profit)
        else:
            payout = 0
            await self.db.update_balance(user_id, -mise)
            await self.db.record_game(user_id, "crash", mise, -mise)
        
        new_balance = await self.db.get_balance(user_id)
        
        details = f"🚀 Votre multiplicateur: **x{multiplicateur}**\n"
        details += f"💥 Point de crash: **x{crash_point}**\n"
        
        if won:
            details += f"\n✅ Vous avez retiré avant le crash!"
        else:
            details += f"\n❌ Crash! Vous avez perdu votre mise."
        
        embed = game_result_embed("Crash", won, mise, payout, new_balance, details)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Games(bot))
