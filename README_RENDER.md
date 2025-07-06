# Déploiement Téléfoot Bot sur Render.com

## Guide complet de déploiement

### 📋 Prérequis
- Compte GitHub
- Compte Render.com
- Fichiers du bot (fournis dans le package)

### 🚀 Étapes de déploiement

#### 1. Créer le repository GitHub
```bash
git init
git add .
git commit -m "Initial commit - Téléfoot Bot"
git branch -M main
git remote add origin https://github.com/votre-username/telefoot-bot.git
git push -u origin main
```

#### 2. Configuration Render.com
1. Connectez-vous à [render.com](https://render.com)
2. Cliquez sur "New Web Service"
3. Connectez votre repository GitHub
4. Configurez les paramètres :

**Build & Deploy:**
- **Build Command:** `pip install -r requirements_render.txt`
- **Start Command:** `python render_deploy_complete.py`

**Environment Variables:**
```
API_ID=29177661
API_HASH=a8639172fa8d35dbfd8ea46286d349ab
BOT_TOKEN=7573497633:AAHk9K15yTCiJP-zruJrc9v8eK8I9XhjyH4
ADMIN_ID=1190237801
```

#### 3. Fonctionnalités automatiques

**Monitoring automatique:**
- Le bot répond automatiquement "ok" aux messages de réactivation
- Surveillance continue du statut
- Redémarrage automatique en cas de problème

**Notifications:**
- Message de démarrage avec statut complet
- Heartbeat périodique pour vérifier la connectivité
- Notifications de redémarrage automatique

### 🔧 Commandes disponibles

**Utilisateurs:**
- `/start` - Démarrer le bot
- `/status` - Voir le statut de l'abonnement
- `/help` - Aide

**Admin:**
- `/activer <user_id> <plan>` - Activer un utilisateur
- `/ping` - Test de connectivité
- Message "réactiver bot automatique" → Bot répond "ok"

### 📊 Monitoring

Le bot inclut un système de monitoring qui :

1. **Détecte les déconnexions** automatiquement
2. **Répond "ok"** aux messages de réactivation
3. **Envoie des notifications** de statut
4. **Redémarre automatiquement** si nécessaire

### 🎯 Après déploiement

Une fois déployé, vous recevrez :
- Message de confirmation de démarrage
- URL du service Render
- Statut complet du bot
- Notifications automatiques

### 🛠️ Dépannage

**Problème de connexion:**
- Vérifiez les variables d'environnement
- Consultez les logs Render

**Bot non réactif:**
- Envoyez "réactiver bot automatique"
- Le bot répondra "ok" automatiquement

**Redémarrage manuel:**
- Utilisez le bouton "Manual Deploy" sur Render
- Le bot se reconnectera automatiquement

### 📱 Support

Pour toute assistance :
- Vérifiez les logs Render.com
- Testez avec `/ping`
- Consultez ce guide

---

**✅ Déploiement automatique configuré avec succès !**