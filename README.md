# 🎰 Gambling Bot Discord

Un bot Discord complet de gambling avec système de monnaie virtuelle, plusieurs jeux de casino et un système d'économie.

## ✨ Fonctionnalités

### 🎮 Jeux disponibles

- **Coinflip** - Pariez sur pile ou face (multiplicateur x2)
- **Dice** - Lancez les dés et gagnez selon le résultat (jusqu'à x10)
- **Slots** - Machine à sous avec différents symboles (jusqu'à x50 pour le jackpot!)
- **Roulette** - Pariez sur rouge, noir, vert, pair ou impair (x2 ou x36)
- **Blackjack** - Jouez contre le croupier (x2 ou x2.5 pour un blackjack)
- **Crash** - Définissez votre multiplicateur avant le crash (multiplicateur variable)

### 💰 Système d'économie

- Balance personnelle pour chaque utilisateur
- Récompense quotidienne de 500 coins
- Système de transfert entre joueurs
- Statistiques détaillées (gains, pertes, parties jouées)
- Classement des joueurs les plus riches

### ⚙️ Commandes administratives

- Ajouter/retirer des coins
- Définir la balance d'un utilisateur
- Réinitialiser un utilisateur
- Voir les statistiques globales du bot

## 🚀 Installation

### Prérequis

- Python 3.11 ou supérieur
- Un bot Discord (token)
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner le repository**
```bash
git clone https://github.com/NouillesMan/gambling-bot-discord.git
cd gambling-bot-discord
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configurer le bot**

Créez un fichier `.env` à la racine du projet :
```bash
cp .env.example .env
```

Éditez le fichier `.env` et ajoutez votre token Discord :
```env
DISCORD_TOKEN=votre_token_ici
PREFIX=/
STARTING_BALANCE=1000
DAILY_REWARD=500
```

4. **Lancer le bot**
```bash
python bot.py
```

## 🤖 Créer un bot Discord

Si vous n'avez pas encore de bot Discord :

1. Allez sur le [Discord Developer Portal](https://discord.com/developers/applications)
2. Cliquez sur "New Application"
3. Donnez un nom à votre application
4. Allez dans l'onglet "Bot"
5. Cliquez sur "Add Bot"
6. Copiez le token (⚠️ Ne le partagez jamais!)
7. Activez les "Privileged Gateway Intents" :
   - Presence Intent
   - Server Members Intent
   - Message Content Intent
8. Allez dans l'onglet "OAuth2" > "URL Generator"
9. Sélectionnez les scopes : `bot` et `applications.commands`
10. Sélectionnez les permissions : `Administrator` (ou personnalisez)
11. Copiez l'URL générée et ouvrez-la dans votre navigateur pour inviter le bot

## 📋 Commandes

### Économie

| Commande | Description |
|----------|-------------|
| `/balance [utilisateur]` | Voir votre balance ou celle d'un autre utilisateur |
| `/daily` | Réclamez votre récompense quotidienne (500 coins) |
| `/give <utilisateur> <montant>` | Donner des coins à un autre utilisateur |
| `/stats [utilisateur]` | Voir vos statistiques détaillées |
| `/leaderboard` | Voir le classement des 10 joueurs les plus riches |

### Jeux

| Commande | Description | Multiplicateur |
|----------|-------------|----------------|
| `/coinflip <choix> <mise>` | Pile ou face | x2 |
| `/dice <mise>` | Lancer de dés | x1.5 à x10 |
| `/slots <mise>` | Machine à sous | x1.5 à x50 |
| `/roulette <type> <mise>` | Roulette | x2 ou x36 |
| `/blackjack <mise>` | Blackjack | x2 ou x2.5 |
| `/crash <mise> <multiplicateur>` | Crash game | Variable |

### Administration (Réservé aux administrateurs)

| Commande | Description |
|----------|-------------|
| `/addcoins <utilisateur> <montant>` | Ajouter des coins à un utilisateur |
| `/removecoins <utilisateur> <montant>` | Retirer des coins à un utilisateur |
| `/setbalance <utilisateur> <montant>` | Définir la balance d'un utilisateur |
| `/resetuser <utilisateur>` | Réinitialiser complètement un utilisateur |
| `/botstats` | Voir les statistiques globales du bot |

### Utilitaires

| Commande | Description |
|----------|-------------|
| `/help` | Afficher l'aide et la liste des commandes |

## ⚙️ Configuration

Vous pouvez modifier les paramètres du bot dans le fichier `.env` :

```env
# Token du bot Discord
DISCORD_TOKEN=votre_token_ici

# Préfixe des commandes (par défaut: /)
PREFIX=/

# Balance de départ pour les nouveaux utilisateurs
STARTING_BALANCE=1000

# Récompense quotidienne
DAILY_REWARD=500
```

Les limites de paris peuvent être modifiées dans `config.py` :

```python
MIN_BET = 10      # Mise minimum
MAX_BET = 10000   # Mise maximum
```

## 📁 Structure du projet

```
gambling-bot-discord/
├── bot.py                  # Point d'entrée principal
├── config.py               # Configuration du bot
├── requirements.txt        # Dépendances Python
├── .env.example           # Exemple de fichier d'environnement
├── .gitignore             # Fichiers à ignorer par Git
├── README.md              # Documentation
├── database/
│   ├── db_manager.py      # Gestionnaire de base de données
│   └── gambling.db        # Base de données SQLite (créée automatiquement)
├── cogs/
│   ├── economy.py         # Commandes d'économie
│   ├── games.py           # Jeux de gambling
│   └── admin.py           # Commandes administratives
└── utils/
    ├── embeds.py          # Templates d'embeds Discord
    └── helpers.py         # Fonctions utilitaires et logique des jeux
```

## 🎲 Règles des jeux

### Coinflip
Pariez sur pile ou face. Si vous gagnez, vous doublez votre mise (x2).

### Dice
Lancez 2 dés :
- **12** (double 6) : x10
- **2** (double 1) : x5
- **10-11** : x3
- **7-9** : x1.5
- **3-6** : Perte

### Slots
Machine à sous avec 3 rouleaux :
- **7️⃣ 7️⃣ 7️⃣** : x50 (Jackpot!)
- **💎 💎 💎** : x20
- **🍇 🍇 🍇** : x10
- **🍊 🍊 🍊** : x5
- **🍋 🍋 🍋** : x3
- **🍒 🍒 🍒** : x2
- **2 symboles identiques** : x1.5
- **Aucune correspondance** : Perte

### Roulette
Pariez sur :
- **Rouge/Noir** : x2
- **Pair/Impair** : x2
- **Vert (0)** : x36

### Blackjack
Jouez contre le croupier. Le but est d'obtenir 21 ou de se rapprocher de 21 sans dépasser.
- **Blackjack naturel** : x2.5
- **Victoire normale** : x2
- **Égalité** : Mise retournée
- **Défaite** : Perte de la mise

### Crash
Définissez un multiplicateur de retrait. Si le crash se produit après votre multiplicateur, vous gagnez. Sinon, vous perdez.

## 🛠️ Technologies utilisées

- **Python 3.11**
- **discord.py** - Bibliothèque Discord
- **aiosqlite** - Base de données SQLite asynchrone
- **python-dotenv** - Gestion des variables d'environnement

## 📝 Base de données

Le bot utilise SQLite pour stocker les données. Deux tables principales :

### Table `users`
- `user_id` : ID Discord de l'utilisateur
- `balance` : Balance actuelle
- `total_won` : Total gagné
- `total_lost` : Total perdu
- `games_played` : Nombre de parties jouées
- `last_daily` : Date de la dernière récompense quotidienne
- `created_at` : Date de création du compte

### Table `game_history`
- `id` : ID de la partie
- `user_id` : ID de l'utilisateur
- `game_type` : Type de jeu
- `bet_amount` : Montant parié
- `result` : Résultat (positif = gain, négatif = perte)
- `timestamp` : Date et heure de la partie

## 🤝 Contribution

Les contributions sont les bienvenues! N'hésitez pas à :

1. Fork le projet
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📜 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## ⚠️ Avertissement

Ce bot utilise une monnaie virtuelle et est destiné uniquement au divertissement. Il ne s'agit pas de vrai argent et aucun gain réel ne peut être obtenu. Le gambling peut créer une dépendance - jouez de manière responsable!

## 📧 Support

Si vous avez des questions ou des problèmes, n'hésitez pas à ouvrir une issue sur GitHub.

## 🎉 Remerciements

Merci d'utiliser ce bot! Amusez-vous bien et bonne chance! 🍀

---

Créé avec ❤️ par NouillesMan
