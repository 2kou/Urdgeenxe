"""
Bot Telegram Téléfoot pour Render.com avec serveur web intégré
Notification automatique de déploiement réussi avec URL et port
"""

import asyncio
import logging
import os
import json
import time
import threading
from datetime import datetime, timedelta
from telethon import TelegramClient, events
from flask import Flask, jsonify

# Configuration
API_ID = int(os.getenv('API_ID', '29177661'))
API_HASH = os.getenv('API_HASH', 'a8639172fa8d35dbfd8ea46286d349ab')
BOT_TOKEN = os.getenv('BOT_TOKEN', '7573497633:AAHk9K15yTCiJP-zruJrc9v8eK8I9XhjyH4')
ADMIN_ID = int(os.getenv('ADMIN_ID', '1190237801'))

# Configuration serveur
PORT = int(os.getenv('PORT', '10000'))
RENDER_URL = os.getenv('RENDER_EXTERNAL_URL', f'https://telefoot-bot.onrender.com')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelefootBotServer:
    def __init__(self):
        self.client = TelegramClient('telefoot_bot', API_ID, API_HASH)
        self.users = {}
        self.restart_count = 0
        self.app = Flask(__name__)
        self.setup_web_server()
        self.deployment_success = False
        
    def setup_web_server(self):
        """Configure le serveur web pour Render"""
        
        @self.app.route('/')
        def home():
            return jsonify({
                "service": "Téléfoot Bot",
                "status": "Opérationnel",
                "deployment": "Réussi" if self.deployment_success else "En cours",
                "url": RENDER_URL,
                "port": PORT,
                "users": len(self.users),
                "uptime": time.time()
            })
        
        @self.app.route('/health')
        def health():
            return jsonify({
                "status": "healthy",
                "bot_connected": self.client.is_connected() if hasattr(self.client, 'is_connected') else True,
                "users_count": len(self.users),
                "restart_count": self.restart_count
            })
        
        @self.app.route('/stats')
        def stats():
            return jsonify({
                "total_users": len(self.users),
                "active_users": sum(1 for u in self.users.values() if u.get('plan') != 'waiting'),
                "pending_users": sum(1 for u in self.users.values() if u.get('plan') == 'waiting'),
                "server_info": {
                    "url": RENDER_URL,
                    "port": PORT,
                    "restart_count": self.restart_count
                }
            })
    
    def start_web_server(self):
        """Démarre le serveur web en arrière-plan"""
        def run_server():
            self.app.run(host='0.0.0.0', port=PORT, debug=False)
        
        server_thread = threading.Thread(target=run_server)
        server_thread.daemon = True
        server_thread.start()
        logger.info(f"Serveur web démarré sur le port {PORT}")
    
    def load_users(self):
        """Charge les utilisateurs"""
        try:
            with open('users.json', 'r', encoding='utf-8') as f:
                self.users = json.load(f)
        except FileNotFoundError:
            self.users = {}
            self.save_users()
    
    def save_users(self):
        """Sauvegarde les utilisateurs"""
        try:
            with open('users.json', 'w', encoding='utf-8') as f:
                json.dump(self.users, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erreur sauvegarde: {e}")
    
    def register_user(self, user_id, username=None):
        """Enregistre un utilisateur"""
        user_id = str(user_id)
        if user_id not in self.users:
            self.users[user_id] = {
                'username': username,
                'registered_at': datetime.now().isoformat(),
                'plan': 'waiting',
                'expires_at': None
            }
            self.save_users()
            return True
        return False
    
    def activate_user(self, user_id, plan='weekly'):
        """Active un utilisateur"""
        user_id = str(user_id)
        if user_id in self.users:
            duration = timedelta(days=7 if plan == 'weekly' else 30)
            self.users[user_id]['plan'] = plan
            self.users[user_id]['expires_at'] = (datetime.now() + duration).isoformat()
            self.save_users()
            return True
        return False
    
    def check_user_access(self, user_id):
        """Vérifie l'accès utilisateur"""
        user_id = str(user_id)
        if user_id not in self.users:
            return False
        
        user = self.users[user_id]
        if user['plan'] == 'waiting':
            return False
        
        if user['expires_at']:
            expires = datetime.fromisoformat(user['expires_at'])
            return datetime.now() < expires
        
        return True
    
    async def send_deployment_notification(self):
        """Envoie la notification de déploiement réussi"""
        try:
            await self.client.send_message(
                ADMIN_ID,
                f"✅ **DÉPLOIEMENT RÉUSSI SUR RENDER.COM**\n\n"
                f"🚀 **Bot Téléfoot déployé avec succès !**\n\n"
                f"🌐 **URL du service :** {RENDER_URL}\n"
                f"🔌 **Port :** {PORT}\n"
                f"⏰ **Heure de déploiement :** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                f"📊 **Statut du service :**\n"
                f"• Utilisateurs chargés: {len(self.users)}\n"
                f"• Serveur web: Actif sur port {PORT}\n"
                f"• Système de réactivation: Opérationnel\n"
                f"• Monitoring automatique: Activé\n\n"
                f"🔗 **Endpoints disponibles :**\n"
                f"• {RENDER_URL}/ - Statut général\n"
                f"• {RENDER_URL}/health - Santé du service\n"
                f"• {RENDER_URL}/stats - Statistiques\n\n"
                f"🔄 **Commandes de gestion :**\n"
                f"• `/ping` - Vérifier le statut\n"
                f"• `/status` - Statut utilisateur\n"
                f"• Message 'réactiver bot automatique' → Réponse automatique 'ok'\n\n"
                f"💚 **Service opérationnel et prêt à l'utilisation !**"
            )
            self.deployment_success = True
            logger.info("Notification de déploiement envoyée")
        except Exception as e:
            logger.error(f"Erreur notification déploiement: {e}")
    
    async def start(self):
        """Démarre le bot"""
        await self.client.start(bot_token=BOT_TOKEN)
        logger.info("Bot Téléfoot connecté")
        
        # Démarrer le serveur web
        self.start_web_server()
        
        # Charger les utilisateurs
        self.load_users()
        
        # Envoyer la notification de déploiement
        await self.send_deployment_notification()
        
        await self.register_handlers()
        await self.monitor_loop()
    
    async def register_handlers(self):
        """Enregistre tous les handlers"""
        
        # HANDLER PRINCIPAL : Réactivation automatique Render.com
        @self.client.on(events.NewMessage(pattern=r'(?i).*réactiver.*bot.*automatique.*'))
        async def reactivation_handler(event):
            """Répond automatiquement 'ok' aux messages de réactivation"""
            if event.sender_id == ADMIN_ID:
                await event.reply("ok")
                logger.info("✅ Réponse automatique 'ok' envoyée")
                self.restart_count += 1
                
                await self.client.send_message(
                    ADMIN_ID,
                    f"🔄 **Bot réactivé automatiquement**\n\n"
                    f"⏰ Heure: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"🔢 Redémarrage #: {self.restart_count}\n"
                    f"🌐 URL: {RENDER_URL}\n"
                    f"🔌 Port: {PORT}\n"
                    f"👥 Utilisateurs: {len(self.users)}"
                )
        
        @self.client.on(events.NewMessage(pattern='/start'))
        async def start_handler(event):
            """Handler /start"""
            user_id = event.sender_id
            username = event.sender.username or event.sender.first_name
            
            if self.register_user(user_id, username):
                await event.reply(
                    f"👋 **Bienvenue {username} !**\n\n"
                    f"🎯 **Téléfoot Bot - Gestion de Licences**\n\n"
                    f"📋 **Votre statut:** En attente d'activation\n"
                    f"💰 **Plans disponibles:**\n"
                    f"• 1 semaine = 1000f\n"
                    f"• 1 mois = 3000f\n\n"
                    f"📱 **Contactez l'admin pour l'activation**"
                )
            else:
                if self.check_user_access(user_id):
                    await event.reply(f"👋 **Bon retour {username} !**\n\n✅ **Votre accès est actif**")
                else:
                    await event.reply(f"👋 **Salut {username} !**\n\n⏰ **Votre accès a expiré**")
        
        @self.client.on(events.NewMessage(pattern='/ping'))
        async def ping_handler(event):
            """Handler /ping avec informations serveur"""
            await event.reply(
                f"🟢 **Bot actif sur Render.com**\n\n"
                f"🌐 **URL:** {RENDER_URL}\n"
                f"🔌 **Port:** {PORT}\n"
                f"👥 **Utilisateurs:** {len(self.users)}\n"
                f"🔄 **Redémarrages:** {self.restart_count}\n"
                f"📊 **Statut:** Opérationnel\n\n"
                f"🔗 **Endpoints:**\n"
                f"• /health - Santé du service\n"
                f"• /stats - Statistiques détaillées"
            )
        
        # Autres handlers essentiels...
        @self.client.on(events.NewMessage(pattern='/status'))
        async def status_handler(event):
            """Handler /status"""
            user_id = str(event.sender_id)
            
            if user_id in self.users:
                user = self.users[user_id]
                
                if user['plan'] == 'waiting':
                    status_msg = "📋 **Statut:** En attente d'activation"
                elif self.check_user_access(event.sender_id):
                    expires = datetime.fromisoformat(user['expires_at'])
                    remaining = expires - datetime.now()
                    status_msg = f"✅ **Statut:** Actif\n📅 **Plan:** {user['plan']}\n⏰ **Expire dans:** {remaining.days} jours"
                else:
                    status_msg = "❌ **Statut:** Expiré"
                    
                await event.reply(status_msg)
            else:
                await event.reply("❌ Utilisateur non trouvé. Utilisez /start")
        
        logger.info("✅ Handlers enregistrés")
    
    async def monitor_loop(self):
        """Boucle de monitoring"""
        while True:
            try:
                await asyncio.sleep(600)  # 10 minutes
                logger.info(f"💓 Heartbeat - URL: {RENDER_URL}, Port: {PORT}")
            except Exception as e:
                logger.error(f"Erreur monitoring: {e}")
                await asyncio.sleep(60)

    async def run(self):
        """Lance le bot"""
        try:
            await self.start()
        except Exception as e:
            logger.error(f"Erreur fatale: {e}")
            await asyncio.sleep(30)
            await self.run()

if __name__ == "__main__":
    bot = TelefootBotServer()
    
    try:
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        logger.info("Arrêt du bot")
    except Exception as e:
        logger.error(f"Erreur: {e}")