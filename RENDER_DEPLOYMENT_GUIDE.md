# 🚀 Guide d'hébergement sur Render.com

## Étape 1 : Préparation du Repository

### 1.1 Créer un repository GitHub
```bash
# Créer un nouveau repository sur GitHub
# Nom suggéré : telefoot-bot-render
```

### 1.2 Fichiers nécessaires
Copiez ces fichiers dans votre repository :
- `render_deploy.py` (bot principal)
- `requirements_render.txt` (dépendances)
- `user_manager.py` (gestionnaire utilisateurs)
- `bot_handlers.py` (gestionnaire commandes)
- `config.py` (configuration)
- `users.json` (base de données utilisateurs)

## Étape 2 : Configuration sur Render.com

### 2.1 Créer un nouveau Web Service
1. Allez sur [render.com](https://render.com)
2. Cliquez sur "New +" → "Web Service"
3. Connectez votre repository GitHub
4. Configurez les paramètres :

### 2.2 Paramètres du Service
```
Name: telefoot-bot
Environment: Python 3
Build Command: pip install -r requirements_render.txt
Start Command: python render_deploy.py
```

### 2.3 Variables d'environnement
Ajoutez ces variables dans l'onglet "Environment" :

```
API_ID=29177661
API_HASH=a8639172fa8d35dbfd8ea46286d349ab
BOT_TOKEN=7573497633:AAHk9K15yTCiJP-zruJrc9v8eK8I9XhjyH4
ADMIN_ID=1190237801
```

## Étape 3 : Déploiement

### 3.1 Déploiement automatique
1. Cliquez sur "Create Web Service"
2. Render va automatiquement :
   - Télécharger votre code
   - Installer les dépendances
   - Lancer le bot

### 3.2 Surveillance
- Suivez les logs en temps réel
- Le bot devrait afficher "🤖 Bot connecté"
- Vérifiez que le status est "Live"

## Étape 4 : Fonctionnalités disponibles

### 4.1 Commandes utilisateur
- `/start` - Démarrer le bot
- `/status` - Vérifier le statut
- `/help` - Aide
- `/pronostics` - Pronostics du jour

### 4.2 Commandes admin
- `/activer <user_id> <plan>` - Activer un utilisateur
- `/menu` - Interface à boutons

## Étape 5 : Avantages de Render.com

### 5.1 Avantages
- ✅ Hébergement gratuit (750h/mois)
- ✅ Déploiement automatique depuis GitHub
- ✅ SSL automatique
- ✅ Logs en temps réel
- ✅ Monitoring intégré

### 5.2 Limitations
- ⏰ 750 heures gratuites par mois
- 💤 Mise en veille après 15 min d'inactivité
- 🔄 Redémarrage automatique nécessaire

## Étape 6 : Maintenance

### 6.1 Mise à jour
1. Modifiez le code dans votre repository
2. Commit et push sur GitHub
3. Render redéploie automatiquement

### 6.2 Monitoring
- Surveillez les logs pour les erreurs
- Vérifiez le statut du service
- Redémarrez si nécessaire

## Étape 7 : Dépannage

### 7.1 Problèmes courants
```
❌ Bot ne démarre pas
→ Vérifiez les variables d'environnement
→ Vérifiez le BOT_TOKEN

❌ Erreur de mémoire
→ Utilisez le plan payant
→ Optimisez le code

❌ Mise en veille
→ Utilisez un service de ping
→ Passez au plan payant
```

### 7.2 Logs utiles
```
✅ Bot connecté : @Googlekdnsbot
✅ Bot initialisé avec succès
🚀 Bot démarré sur Render.com
```

## Étape 8 : Optimisations

### 8.1 Éviter la mise en veille
- Utilisez UptimeRobot pour pinger votre service
- Ou passez au plan payant ($7/mois)

### 8.2 Sauvegarde des données
- Utilisez une base de données externe
- Ou sauvegardez régulièrement `users.json`

## 📞 Support

En cas de problème :
1. Vérifiez les logs sur Render
2. Testez localement d'abord
3. Vérifiez les variables d'environnement
4. Contactez le support si nécessaire

## 🎯 Prochaines étapes

Votre bot Téléfoot sera opérationnel 24/7 sur Render.com avec :
- Gestion automatique des licences
- Interface utilisateur complète
- Monitoring et logs intégrés
- Déploiement automatique depuis GitHub