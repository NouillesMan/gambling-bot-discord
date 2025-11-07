# 🚀 Guide de Démarrage Rapide

## Étape 1: Réinitialiser ton token (URGENT!)

⚠️ **Ton token a été exposé, tu DOIS le réinitialiser d'abord!**

1. Va sur https://discord.com/developers/applications
2. Sélectionne ton application
3. Va dans "Bot" → Clique sur "Reset Token"
4. Copie le nouveau token

## Étape 2: Créer le fichier .env

Dans le dossier `gambling-bot-discord`, crée un fichier nommé `.env`:

```env
DISCORD_TOKEN=ton_nouveau_token_ici
PREFIX=/
STARTING_BALANCE=1000
DAILY_REWARD=500
```

**Remplace `ton_nouveau_token_ici` par ton vrai token!**

## Étape 3: Activer les Intents

Sur le Discord Developer Portal:
1. Va dans "Bot"
2. Descends jusqu'à "Privileged Gateway Intents"
3. Active:
   - ✅ Presence Intent
   - ✅ Server Members Intent
   - ✅ Message Content Intent
4. Clique sur "Save Changes"

## Étape 4: Inviter le bot sur ton serveur

1. Va dans "OAuth2" → "URL Generator"
2. Sélectionne:
   - Scopes: `bot` et `applications.commands`
   - Permissions: `Administrator` (ou personnalise)
3. Copie l'URL en bas de la page
4. Ouvre l'URL dans ton navigateur
5. Sélectionne ton serveur et autorise

## Étape 5: Installer les dépendances

```bash
cd gambling-bot-discord
pip install -r requirements.txt
```

## Étape 6: Lancer le bot

```bash
python bot.py
```

Si tout est correct, tu devrais voir:
```
✅ Database initialized
✅ Loaded cog: cogs.economy
✅ Loaded cog: cogs.games
✅ Loaded cog: cogs.admin
✅ Synced X command(s)

==================================================
🎰 Gambling Bot is ready!
==================================================
```

## Étape 7: Tester le bot

Sur Discord, tape:
- `/help` - Voir toutes les commandes
- `/balance` - Voir ta balance (tu commences avec 1000 coins)
- `/coinflip pile 100` - Jouer au coinflip

## 🎮 Commandes principales

### Économie
- `/balance` - Voir ta balance
- `/daily` - Récompense quotidienne (500 coins)
- `/stats` - Tes statistiques
- `/leaderboard` - Top 10 des joueurs

### Jeux
- `/coinflip <choix> <mise>` - Pile ou face
- `/dice <mise>` - Lancer de dés
- `/slots <mise>` - Machine à sous
- `/roulette <type> <mise>` - Roulette
- `/blackjack <mise>` - Blackjack
- `/crash <mise> <multiplicateur>` - Crash game

### Admin (nécessite permissions administrateur)
- `/addcoins <user> <montant>` - Ajouter des coins
- `/setbalance <user> <montant>` - Définir la balance
- `/botstats` - Stats globales du bot

## ❓ Problèmes courants

### "Invalid token"
→ Vérifie que tu as bien copié le token complet dans le fichier `.env`

### "Intents error"
→ Active les Privileged Gateway Intents dans le Developer Portal

### "Commands not showing"
→ Attends quelques minutes, Discord peut prendre du temps pour synchroniser les commandes

### Le bot ne répond pas
→ Vérifie que le bot est bien en ligne sur Discord (statut vert)

## 📚 Documentation complète

Consulte le fichier `README.md` pour la documentation complète!

Bon jeu! 🎰🍀
