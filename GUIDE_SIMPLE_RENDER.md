# 🚀 Guide Simple - Hébergement Render.com

## 🎯 Objectif
Héberger votre bot Téléfoot sur Render.com pour qu'il fonctionne 24h/24 et 7j/7

## 📋 Étapes Simples

### 1. Créer un compte GitHub (si vous n'en avez pas)
- Allez sur github.com
- Créez un compte gratuit

### 2. Créer un nouveau repository
- Cliquez sur "New repository"
- Nom : `telefoot-bot-render`
- Cochez "Public"
- Cliquez "Create repository"

### 3. Uploader les fichiers
Dans votre repository GitHub, uploadez TOUS les fichiers du dossier `render_deployment` :
- `render_deploy.py`
- `requirements_render.txt`
- `user_manager.py`
- `bot_handlers.py`
- `config.py`
- `users.json`
- `README.md`

### 4. Créer un compte Render.com
- Allez sur render.com
- Créez un compte gratuit
- Connectez votre compte GitHub

### 5. Créer un Web Service
- Cliquez sur "New +" en haut à droite
- Sélectionnez "Web Service"
- Choisissez votre repository `telefoot-bot-render`
- Cliquez "Connect"

### 6. Configuration du Service
Remplissez ces champs :

**Name**: `telefoot-bot`

**Build Command**: 
```
pip install -r requirements_render.txt
```

**Start Command**: 
```
python render_deploy.py
```

### 7. Variables d'environnement
Cliquez sur "Advanced" puis ajoutez ces variables :

| Key | Value |
|-----|-------|
| API_ID | 29177661 |
| API_HASH | a8639172fa8d35dbfd8ea46286d349ab |
| BOT_TOKEN | 7573497633:AAHk9K15yTCiJP-zruJrc9v8eK8I9XhjyH4 |
| ADMIN_ID | 1190237801 |

### 8. Déployer
- Cliquez sur "Create Web Service"
- Attendez 2-3 minutes
- Regardez les logs

## ✅ Vérification

Vous devriez voir dans les logs :
```
🤖 Bot connecté : @Googlekdnsbot
✅ Bot initialisé avec succès
🚀 Bot démarré sur Render.com
```

## 🎉 Félicitations !

Votre bot est maintenant hébergé sur Render.com et fonctionne 24/7 !

## 📱 Test

Envoyez `/start` à votre bot Telegram pour tester.

## 🔧 Dépannage

Si le bot ne démarre pas :
1. Vérifiez que tous les fichiers sont uploadés
2. Vérifiez les variables d'environnement
3. Regardez les logs d'erreur sur Render

## 💡 Conseils

- Le plan gratuit offre 750 heures/mois
- Le bot se met en veille après 15 minutes d'inactivité
- Pour éviter la veille, passez au plan payant ($7/mois)

## 📞 Support

En cas de problème, vérifiez :
1. Les logs sur Render.com
2. Que le bot répond sur Telegram
3. Les variables d'environnement sont correctes