# 🔒 Guide de Sécurité - Token Discord

## ⚠️ IMPORTANT: Ton token a été exposé!

Tu as partagé ton token Discord publiquement. Cela signifie que n'importe qui peut maintenant contrôler ton bot.

## 🚨 Actions URGENTES à faire MAINTENANT:

### 1. Réinitialiser ton token

1. Va sur https://discord.com/developers/applications
2. Sélectionne ton application
3. Clique sur "Bot" dans le menu de gauche
4. Clique sur le bouton **"Reset Token"**
5. Confirme la réinitialisation
6. **COPIE le nouveau token** (tu ne pourras le voir qu'une seule fois!)

### 2. Configurer le fichier .env

Une fois que tu as ton NOUVEAU token:

1. Dans le dossier `gambling-bot-discord`, crée un fichier nommé `.env`
2. Ajoute le contenu suivant:

```env
DISCORD_TOKEN=TON_NOUVEAU_TOKEN_ICI
PREFIX=/
STARTING_BALANCE=1000
DAILY_REWARD=500
```

3. Remplace `TON_NOUVEAU_TOKEN_ICI` par ton nouveau token

### 3. Vérifier que .env est dans .gitignore

Le fichier `.env` est déjà dans le `.gitignore`, ce qui signifie qu'il ne sera JAMAIS envoyé sur GitHub. C'est normal et c'est pour ta sécurité!

## ✅ Bonnes pratiques de sécurité

### ❌ NE JAMAIS:
- Partager ton token publiquement (messages, forums, Discord, etc.)
- Commiter le fichier `.env` sur GitHub
- Partager des screenshots contenant ton token
- Envoyer ton token par e-mail

### ✅ TOUJOURS:
- Garder ton token dans le fichier `.env` local
- Réinitialiser ton token s'il a été exposé
- Vérifier que `.env` est dans `.gitignore`
- Utiliser des variables d'environnement pour les secrets

## 🔐 Pourquoi c'est important?

Avec ton token, quelqu'un peut:
- Contrôler complètement ton bot
- Envoyer des messages depuis ton bot
- Bannir des utilisateurs
- Supprimer des messages
- Accéder aux serveurs où ton bot est présent
- Potentiellement compromettre ton compte Discord

## 📝 Après avoir réinitialisé ton token

1. Crée le fichier `.env` avec le nouveau token
2. Lance le bot avec `python bot.py`
3. Le bot devrait se connecter sans problème

Si tu as des questions, n'hésite pas à demander!
