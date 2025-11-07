# Plan du Bot Discord de Gambling

## Architecture
- **Langage**: Python 3.11
- **Bibliothèque Discord**: discord.py
- **Base de données**: SQLite (simple et portable)
- **Structure**: Commandes slash (/) modernes

## Fonctionnalités principales

### Système d'économie
- Monnaie virtuelle (coins)
- Balance par utilisateur
- Système de daily rewards
- Leaderboard

### Jeux de gambling
1. **Coinflip** - Pile ou face avec mise
2. **Dice** - Lancer de dés avec multiplicateurs
3. **Slots** - Machine à sous avec symboles
4. **Roulette** - Rouge/Noir/Vert avec cotes
5. **Blackjack** - Jeu de cartes contre le dealer
6. **Crash** - Multiplicateur qui monte jusqu'au crash

### Commandes administratives
- Ajouter/retirer des coins
- Réinitialiser un utilisateur
- Statistiques globales

### Commandes utilitaires
- Voir sa balance
- Historique des paris
- Classement des joueurs
- Aide et règles

## Structure des fichiers
```
gambling-bot-discord/
├── bot.py                  # Point d'entrée principal
├── config.py               # Configuration
├── requirements.txt        # Dépendances
├── .env.example           # Exemple de variables d'environnement
├── .gitignore             # Fichiers à ignorer
├── README.md              # Documentation
├── database/
│   └── db_manager.py      # Gestion de la base de données
├── cogs/
│   ├── economy.py         # Commandes d'économie
│   ├── games.py           # Jeux de gambling
│   └── admin.py           # Commandes admin
└── utils/
    ├── embeds.py          # Templates d'embeds Discord
    └── helpers.py         # Fonctions utilitaires
```
