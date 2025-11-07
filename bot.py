"""
Gambling Bot Discord
A complete Discord bot for gambling games with virtual currency
"""
import discord
from discord.ext import commands
import asyncio
import os
import config
from database.db_manager import DatabaseManager

class GamblingBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        super().__init__(
            command_prefix=config.PREFIX,
            intents=intents,
            help_command=None
        )
        
        self.db = DatabaseManager()
    
    async def setup_hook(self):
        """Setup hook called when bot is starting"""
        # Initialize database
        await self.db.initialize()
        print("✅ Database initialized")
        
        # Load cogs
        cogs = ['cogs.economy', 'cogs.games', 'cogs.admin']
        for cog in cogs:
            try:
                await self.load_extension(cog)
                print(f"✅ Loaded cog: {cog}")
            except Exception as e:
                print(f"❌ Failed to load cog {cog}: {e}")
        
        # Sync commands
        try:
            synced = await self.tree.sync()
            print(f"✅ Synced {len(synced)} command(s)")
        except Exception as e:
            print(f"❌ Failed to sync commands: {e}")
    
    async def on_ready(self):
        """Called when bot is ready"""
        print(f"\n{'='*50}")
        print(f"🎰 Gambling Bot is ready!")
        print(f"{'='*50}")
        print(f"Bot: {self.user.name} (ID: {self.user.id})")
        print(f"Servers: {len(self.guilds)}")
        print(f"Users: {len(self.users)}")
        print(f"{'='*50}\n")
        
        # Set bot status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.playing,
                name="🎰 /help | Gambling Bot"
            )
        )
    
    async def on_command_error(self, ctx, error):
        """Global error handler"""
        if isinstance(error, commands.CommandNotFound):
            return
        
        print(f"Error: {error}")

# Help command
@discord.app_commands.command(name="help", description="Afficher l'aide et la liste des commandes")
async def help_command(interaction: discord.Interaction):
    """Show help message"""
    embed = discord.Embed(
        title="🎰 Gambling Bot - Aide",
        description="Bienvenue sur le bot de gambling! Voici toutes les commandes disponibles:",
        color=config.COLOR_INFO
    )
    
    # Economy commands
    embed.add_field(
        name=f"{config.EMOJI_COIN} Économie",
        value=(
            "`/balance` - Voir votre balance\n"
            "`/daily` - Récompense quotidienne\n"
            "`/give` - Donner des coins\n"
            "`/stats` - Voir vos statistiques\n"
            "`/leaderboard` - Classement des joueurs"
        ),
        inline=False
    )
    
    # Games commands
    embed.add_field(
        name="🎮 Jeux",
        value=(
            "`/coinflip` - Pile ou face (x2)\n"
            "`/dice` - Lancer de dés (jusqu'à x10)\n"
            "`/slots` - Machine à sous (jusqu'à x50)\n"
            "`/roulette` - Roulette (x2 ou x36)\n"
            "`/blackjack` - Blackjack (x2 ou x2.5)\n"
            "`/crash` - Crash game (multiplicateur variable)"
        ),
        inline=False
    )
    
    # Admin commands
    embed.add_field(
        name="⚙️ Administration",
        value=(
            "`/addcoins` - Ajouter des coins\n"
            "`/removecoins` - Retirer des coins\n"
            "`/setbalance` - Définir une balance\n"
            "`/resetuser` - Réinitialiser un utilisateur\n"
            "`/botstats` - Statistiques du bot"
        ),
        inline=False
    )
    
    embed.add_field(
        name="ℹ️ Informations",
        value=(
            f"• Balance de départ: **{config.STARTING_BALANCE:,}** coins\n"
            f"• Récompense quotidienne: **{config.DAILY_REWARD:,}** coins\n"
            f"• Mise minimum: **{config.MIN_BET:,}** coins\n"
            f"• Mise maximum: **{config.MAX_BET:,}** coins"
        ),
        inline=False
    )
    
    embed.set_footer(text="Bonne chance! 🍀")
    
    await interaction.response.send_message(embed=embed)

async def main():
    """Main function to run the bot"""
    # Check if token is set
    if not config.DISCORD_TOKEN:
        print("❌ Error: DISCORD_TOKEN not found in environment variables!")
        print("Please create a .env file with your bot token.")
        return
    
    # Create and run bot
    bot = GamblingBot()
    
    # Add help command
    bot.tree.add_command(help_command)
    
    try:
        await bot.start(config.DISCORD_TOKEN)
    except KeyboardInterrupt:
        print("\n⚠️ Bot stopped by user")
    except Exception as e:
        print(f"❌ Error running bot: {e}")
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
