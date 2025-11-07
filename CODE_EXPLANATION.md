# 📚 Guide d'explication du code - Gambling Bot

Ce document explique en détail comment fonctionne chaque partie du bot Discord de gambling.

## 📁 Structure du projet

```
gambling-bot-discord/
├── bot.py                  # 🚀 Point d'entrée - Lance le bot
├── config.py               # ⚙️ Configuration - Toutes les constantes
├── requirements.txt        # 📦 Dépendances Python
├── database/
│   └── db_manager.py      # 💾 Gestion de la base de données
├── cogs/
│   ├── economy.py         # 💰 Commandes d'économie
│   ├── games.py           # 🎮 Jeux de gambling
│   └── admin.py           # 👑 Commandes admin
└── utils/
    ├── embeds.py          # 🎨 Templates de messages Discord
    └── helpers.py         # 🛠️ Logique des jeux
```

---

## 🚀 bot.py - Le cœur du bot

### Comment ça fonctionne?

1. **Classe GamblingBot**
   - Hérite de `commands.Bot` (la classe de base de discord.py)
   - Configure les "intents" (permissions du bot)
   - Initialise le gestionnaire de base de données

2. **setup_hook()**
   - Appelée automatiquement au démarrage
   - Initialise la base de données (crée les tables)
   - Charge tous les cogs (modules de commandes)
   - Synchronise les commandes slash avec Discord

3. **on_ready()**
   - Appelée quand le bot est connecté et prêt
   - Affiche des informations dans la console
   - Définit le statut du bot (ce qui s'affiche sous son nom)

4. **Commande /help**
   - Définie directement dans bot.py
   - Affiche toutes les commandes disponibles
   - Utilise des embeds pour un affichage professionnel

### Flux de démarrage

```
1. main() est appelée
2. GamblingBot() est créé
3. setup_hook() s'exécute:
   - Base de données initialisée ✅
   - Cogs chargés ✅
   - Commandes synchronisées ✅
4. bot.start() se connecte à Discord
5. on_ready() confirme que tout est prêt
6. Le bot attend les commandes des utilisateurs
```

---

## ⚙️ config.py - Configuration centralisée

### Pourquoi ce fichier existe?

Au lieu de mettre des valeurs en dur partout dans le code, on centralise tout ici.
Cela permet de modifier facilement les paramètres sans toucher au code principal.

### Variables d'environnement (.env)

```env
DISCORD_TOKEN=ton_token_ici
STARTING_BALANCE=1000
DAILY_REWARD=500
```

Ces valeurs sont **secrètes** et ne doivent JAMAIS être dans le code source.
Le fichier `.env` reste sur ton ordinateur et n'est jamais envoyé sur GitHub.

### Constantes importantes

- **MIN_BET / MAX_BET**: Limites des paris
- **COLOR_*****: Couleurs pour les embeds Discord (en hexadécimal)
- **EMOJI_*****: Emojis utilisés dans les messages

---

## 💾 database/db_manager.py - Gestion des données

### Structure de la base de données

#### Table `users`
```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,      -- ID Discord (unique)
    balance INTEGER,                  -- Argent actuel
    total_won INTEGER,                -- Total gagné (statistiques)
    total_lost INTEGER,               -- Total perdu (statistiques)
    games_played INTEGER,             -- Nombre de parties
    last_daily TEXT,                  -- Date du dernier /daily
    created_at TEXT                   -- Date de création du compte
)
```

#### Table `game_history`
```sql
CREATE TABLE game_history (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,                  -- Qui a joué?
    game_type TEXT,                   -- Quel jeu? (coinflip, dice, etc.)
    bet_amount INTEGER,               -- Combien parié?
    result INTEGER,                   -- Gain (+) ou perte (-)
    timestamp TEXT                    -- Quand?
)
```

### Fonctions principales

#### `get_or_create_user(user_id)`
```python
# Vérifie si l'utilisateur existe
user = await db.get_user(user_id)

# Si non, le crée avec la balance de départ
if not user:
    user = await db.create_user(user_id)

return user
```

**Pourquoi?** On ne sait jamais si c'est la première fois qu'un utilisateur utilise le bot.
Cette fonction garantit qu'on a toujours un utilisateur valide.

#### `update_balance(user_id, amount)`
```python
# Ajoute ou retire de l'argent
UPDATE users SET balance = balance + amount WHERE user_id = ?

# Si amount = +100 → ajoute 100 coins
# Si amount = -50 → retire 50 coins
```

#### `record_game(user_id, game_type, bet, result)`
```python
# 1. Enregistre la partie dans l'historique
INSERT INTO game_history (user_id, game_type, bet_amount, result) VALUES (...)

# 2. Met à jour les statistiques
if result > 0:  # Victoire
    UPDATE users SET total_won = total_won + result
else:  # Défaite
    UPDATE users SET total_lost = total_lost + abs(result)
```

**Pourquoi enregistrer?** Pour les statistiques et le classement!

---

## 🎨 utils/embeds.py - Messages Discord stylisés

### Qu'est-ce qu'un embed?

Un embed est un message Discord formaté avec:
- Un titre
- Une description
- Des champs (colonnes)
- Une couleur
- Des images
- Un footer

### Exemple de création d'embed

```python
def balance_embed(user, balance):
    embed = discord.Embed(
        title=f"🪙 Balance de {user.display_name}",
        description=f"**{balance:,}** coins",  # :, ajoute des virgules (1,000)
        color=0x3498db,  # Bleu
        timestamp=datetime.now()
    )
    embed.set_thumbnail(url=user.display_avatar.url)  # Avatar de l'utilisateur
    return embed
```

### Embeds principaux

1. **balance_embed**: Affiche la balance
2. **game_result_embed**: Résultat d'une partie (victoire/défaite)
3. **leaderboard_embed**: Classement des joueurs
4. **stats_embed**: Statistiques détaillées

---

## 🛠️ utils/helpers.py - Logique des jeux

### validate_bet(balance, bet)

Vérifie qu'un pari est valide:

```python
if bet < MIN_BET:
    return False, "Mise trop petite!"

if bet > MAX_BET:
    return False, "Mise trop grande!"

if bet > balance:
    return False, "Pas assez d'argent!"

return True, ""  # ✅ Tout est bon
```

### coinflip(choice)

Le jeu le plus simple:

```python
# Lance la pièce
result = random.choice(['pile', 'face'])

# Compare avec le choix du joueur
won = (result == choice)

return won, result
```

**Probabilité**: 50% de gagner, multiplicateur x2

### spin_slots()

Machine à sous avec probabilités:

```python
symbols = ['🍒', '🍋', '🍊', '🍇', '💎', '7️⃣']
weights = [30, 25, 20, 15, 8, 2]  # Probabilités

# Tire 3 symboles
result = random.choices(symbols, weights=weights, k=3)

# Calcule le multiplicateur
if result[0] == result[1] == result[2]:  # 3 identiques
    if result[0] == '7️⃣':
        multiplier = 50  # JACKPOT!
    # ... autres symboles
else:
    multiplier = 0  # Perte
```

**Probabilités**:
- 🍒 : 30% (le plus commun)
- 7️⃣ : 2% (le plus rare, x50!)

### BlackjackGame

Jeu de cartes complet:

```python
class BlackjackGame:
    def __init__(self):
        self.deck = self._create_deck()  # 52 cartes mélangées
        self.player_hand = []
        self.dealer_hand = []
    
    def play(self):
        # 1. Distribution initiale (2 cartes chacun)
        self.player_hand = [self.deal_card(), self.deal_card()]
        self.dealer_hand = [self.deal_card(), self.deal_card()]
        
        # 2. Vérification Blackjack (21 avec 2 cartes)
        if player_value == 21:
            return True, description, 2.5  # x2.5 pour Blackjack!
        
        # 3. Joueur tire jusqu'à 17 minimum
        while player_value < 17:
            self.player_hand.append(self.deal_card())
        
        # 4. Croupier tire jusqu'à 17 minimum
        while dealer_value < 17:
            self.dealer_hand.append(self.deal_card())
        
        # 5. Comparaison des mains
        if player_value > dealer_value:
            return True, description, 2  # Victoire x2
```

**Gestion des As**:
```python
def calculate_hand_value(self, hand):
    value = sum(card[1] for card in hand)
    aces = sum(1 for card in hand if card[0].startswith('A'))
    
    # Ajuste les As si on dépasse 21
    while value > 21 and aces > 0:
        value -= 10  # As passe de 11 à 1
        aces -= 1
    
    return value
```

### crash_game(cashout_multiplier)

Jeu de risque:

```python
# Génère un point de crash aléatoire
rand = random.random()

if rand < 0.33:
    crash_point = random.uniform(1.0, 2.0)  # 33% de chances
elif rand < 0.66:
    crash_point = random.uniform(2.0, 5.0)  # 33% de chances
elif rand < 0.90:
    crash_point = random.uniform(5.0, 10.0)  # 24% de chances
else:
    crash_point = random.uniform(10.0, 50.0)  # 10% de chances

# Le joueur gagne si son multiplicateur est <= crash_point
won = cashout_multiplier <= crash_point
```

---

## 🎮 cogs/games.py - Commandes de jeux

### Structure d'une commande

```python
@app_commands.command(name="coinflip", description="Pariez sur pile ou face")
@app_commands.describe(
    choix="Choisissez pile ou face",
    mise="Montant à parier"
)
async def coinflip_command(self, interaction, choix, mise):
    # 1. Récupère la balance du joueur
    balance = await self.db.get_balance(interaction.user.id)
    
    # 2. Valide le pari
    is_valid, error_msg = validate_bet(balance, mise)
    if not is_valid:
        await interaction.response.send_message(error_embed("Erreur", error_msg))
        return
    
    # 3. Joue la partie
    won, result = coinflip(choix.value)
    
    # 4. Met à jour la balance
    if won:
        await self.db.update_balance(user_id, +mise)  # Ajoute le gain
    else:
        await self.db.update_balance(user_id, -mise)  # Retire la perte
    
    # 5. Enregistre dans l'historique
    await self.db.record_game(user_id, "coinflip", mise, +mise if won else -mise)
    
    # 6. Affiche le résultat
    embed = game_result_embed("Coinflip", won, mise, payout, new_balance, details)
    await interaction.response.send_message(embed=embed)
```

### Flux d'une partie

```
Utilisateur tape: /coinflip pile 100

1. Discord envoie l'interaction au bot
2. coinflip_command() est appelée
3. Vérification de la balance ✅
4. Validation du pari ✅
5. Simulation du jeu (random.choice)
6. Mise à jour de la base de données
7. Création de l'embed de résultat
8. Envoi du message à l'utilisateur
```

---

## 💰 cogs/economy.py - Système d'économie

### /balance

```python
async def balance_command(self, interaction, utilisateur=None):
    # Si aucun utilisateur spécifié, utilise celui qui tape la commande
    target_user = utilisateur or interaction.user
    
    # Récupère la balance
    balance = await self.db.get_balance(target_user.id)
    
    # Affiche avec un embed
    embed = balance_embed(target_user, balance)
    await interaction.response.send_message(embed=embed)
```

### /daily

```python
async def daily_command(self, interaction):
    user_id = interaction.user.id
    
    # Vérifie si l'utilisateur peut réclamer
    can_claim = await self.db.can_claim_daily(user_id)
    
    if not can_claim:
        # Calcule le temps restant
        time_left = next_claim - datetime.now()
        hours = int(time_left.total_seconds() // 3600)
        minutes = int((time_left.total_seconds() % 3600) // 60)
        
        await interaction.response.send_message(
            f"Revenez dans {hours}h {minutes}m"
        )
        return
    
    # Donne la récompense
    reward = await self.db.claim_daily(user_id)
    await interaction.response.send_message(f"Vous avez reçu {reward} coins!")
```

### /leaderboard

```python
async def leaderboard_command(self, interaction):
    # Récupère les 10 meilleurs joueurs
    leaderboard_data = await self.db.get_leaderboard(10)
    
    # Crée l'embed avec médailles pour le top 3
    embed = leaderboard_embed(leaderboard_data, self.bot)
    
    await interaction.response.send_message(embed=embed)
```

---

## 👑 cogs/admin.py - Commandes administratives

### Permissions

```python
@app_commands.default_permissions(administrator=True)
```

Cette ligne fait que **seuls les administrateurs** peuvent utiliser la commande.

### /addcoins

```python
async def addcoins_command(self, interaction, utilisateur, montant):
    # Ajoute des coins à un utilisateur
    await self.db.update_balance(utilisateur.id, montant)
    
    # Récupère la nouvelle balance
    new_balance = await self.db.get_balance(utilisateur.id)
    
    await interaction.response.send_message(
        f"{montant} coins ajoutés à {utilisateur.mention}!"
    )
```

### /botstats

```python
async def botstats_command(self, interaction):
    # Récupère les statistiques globales
    total_users = COUNT(*) FROM users
    total_coins = SUM(balance) FROM users
    total_games = COUNT(*) FROM game_history
    
    # Affiche dans un embed
    embed = info_embed("Statistiques", f"Utilisateurs: {total_users}...")
    await interaction.response.send_message(embed=embed)
```

---

## 🔄 Cycle de vie d'une commande

```
1. Utilisateur tape /coinflip pile 100
   ↓
2. Discord envoie l'interaction au bot
   ↓
3. Le bot appelle coinflip_command()
   ↓
4. Récupération de la balance depuis la DB
   ↓
5. Validation du pari (assez d'argent?)
   ↓
6. Simulation du jeu (random.choice)
   ↓
7. Mise à jour de la balance dans la DB
   ↓
8. Enregistrement dans game_history
   ↓
9. Création de l'embed de résultat
   ↓
10. Envoi du message à Discord
   ↓
11. L'utilisateur voit le résultat!
```

---

## 🔐 Sécurité et bonnes pratiques

### 1. Variables d'environnement

```python
# ❌ MAUVAIS
DISCORD_TOKEN = "MTQzNjMwMDgxNjYzMzA0MDk1Ng.GpowQw..."

# ✅ BON
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
```

### 2. Validation des entrées

```python
# Toujours valider avant d'utiliser
is_valid, error = validate_bet(balance, bet)
if not is_valid:
    return error
```

### 3. Gestion des erreurs

```python
try:
    await self.db.update_balance(user_id, amount)
except Exception as e:
    print(f"Erreur: {e}")
    await interaction.response.send_message("Une erreur s'est produite")
```

### 4. Base de données asynchrone

```python
# ✅ BON - Non-bloquant
async with aiosqlite.connect(self.db_path) as db:
    await db.execute("SELECT ...")

# ❌ MAUVAIS - Bloquerait le bot
import sqlite3
db = sqlite3.connect("database.db")
db.execute("SELECT ...")
```

---

## 🎯 Points clés à retenir

1. **bot.py** = Point d'entrée, charge tout
2. **config.py** = Toutes les constantes centralisées
3. **db_manager.py** = Toutes les opérations de base de données
4. **embeds.py** = Création de messages Discord stylisés
5. **helpers.py** = Logique des jeux (random, calculs)
6. **Cogs** = Modules de commandes (economy, games, admin)

### Flux général

```
Utilisateur → Discord → Bot → Cog → Helper/DB → Embed → Discord → Utilisateur
```

### Asynchrone (async/await)

```python
# async = fonction asynchrone (non-bloquante)
async def ma_fonction():
    # await = attend le résultat sans bloquer
    result = await autre_fonction()
    return result
```

**Pourquoi?** Un bot Discord doit gérer plusieurs utilisateurs en même temps.
L'asynchrone permet de ne pas bloquer le bot pendant qu'il attend une réponse de la base de données.

---

## 📝 Exercices pour comprendre

### Exercice 1: Ajouter un nouveau jeu

Pour ajouter un jeu "Double or Nothing":

1. Créer la fonction dans `helpers.py`:
```python
def double_or_nothing() -> bool:
    return random.random() < 0.5  # 50% de chances
```

2. Ajouter la commande dans `cogs/games.py`:
```python
@app_commands.command(name="double", description="Double ou rien!")
async def double_command(self, interaction, mise: int):
    # ... même structure que coinflip
```

### Exercice 2: Modifier les probabilités

Pour rendre les slots plus généreux:

```python
# Dans helpers.py, fonction spin_slots()
weights = [30, 25, 20, 15, 8, 2]  # Avant

weights = [25, 20, 20, 15, 12, 8]  # Après (7️⃣ plus fréquent)
```

### Exercice 3: Ajouter une statistique

Pour tracker les Blackjacks:

1. Ajouter une colonne dans la DB:
```sql
ALTER TABLE users ADD COLUMN blackjacks_won INTEGER DEFAULT 0
```

2. Incrémenter dans `helpers.py`:
```python
if player_value == 21:
    # ... code existant
    # Ajouter:
    await self.db.execute(
        "UPDATE users SET blackjacks_won = blackjacks_won + 1 WHERE user_id = ?",
        (user_id,)
    )
```

---

## ❓ Questions fréquentes

**Q: Pourquoi utiliser SQLite?**
R: Simple, portable, pas besoin de serveur. Parfait pour un bot Discord.

**Q: Pourquoi les cogs?**
R: Pour organiser le code. Au lieu d'un fichier de 3000 lignes, on a des modules séparés.

**Q: C'est quoi un "interaction"?**
R: C'est l'objet que Discord envoie quand un utilisateur tape une commande slash.

**Q: Pourquoi async/await partout?**
R: Pour que le bot puisse gérer plusieurs utilisateurs en même temps sans bloquer.

**Q: Comment ajouter plus de coins de départ?**
R: Modifie `STARTING_BALANCE` dans le fichier `.env`.

---

**Bon code! 🚀**
