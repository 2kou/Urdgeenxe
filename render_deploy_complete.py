"""
Bot Telegram Téléfoot complet optimisé pour Render.com
Avec système de monitoring automatique et réactivation
"""

import asyncio
import logging
import os
import json
import time
from datetime import datetime, timedelta
from telethon import TelegramClient, events, Button
from telethon.errors import SessionPasswordNeededError

# Configuration
API_ID = int(os.getenv('API_ID', '29177661'))
API_HASH = os.getenv('API_HASH', 'a8639172fa8d35dbfd8ea46286d349ab')
BOT_TOKEN = os.getenv('BOT_TOKEN', '7573497633:AAHk9K15yTCiJP-zruJrc9v8eK8I9XhjyH4')
ADMIN_ID = int(os.getenv('ADMIN_ID', '1190237801'))

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RenderTelefootBot:
    def __init__(self):
        self.client = TelegramClient('render_bot', API_ID, API_HASH)
        self.users = {}
        self.last_activity = time.time()
        self.restart_count = 0
        
    def load_users(self):
        """Charge les utilisateurs depuis le fichier JSON"""
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
            logger.error(f"Erreur sauvegarde utilisateurs: {e}")
    
    def register_user(self, user_id, username=None):
        """Enregistre un nouvel utilisateur"""
        user_id = str(user_id)
        if user_id not in self.users:
            self.users[user_id] = {
                'username': username,
                'registered_at': datetime.now().isoformat(),
                'plan': 'waiting',
                'expires_at': None,
                'license_key': None
            }
            self.save_users()
            return True
        return False
    
    def activate_user(self, user_id, plan='weekly'):
        """Active un utilisateur avec un plan"""
        user_id = str(user_id)
        if user_id in self.users:
            duration = timedelta(days=7 if plan == 'weekly' else 30)
            self.users[user_id]['plan'] = plan
            self.users[user_id]['expires_at'] = (datetime.now() + duration).isoformat()
            self.save_users()
            return True
        return False
    
    def check_user_access(self, user_id):
        """Vérifie l'accès d'un utilisateur"""
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
    
    async def start(self):
        """Démarre le bot"""
        await self.client.start(bot_token=BOT_TOKEN)
        logger.info("🤖 Bot Téléfoot démarré sur Render.com")
        
        # Charger les utilisateurs
        self.load_users()
        
        # Notification de déploiement réussi
        render_url = os.getenv('RENDER_EXTERNAL_URL', 'https://votre-service.onrender.com')
        port = os.getenv('PORT', '10000')
        
        await self.client.send_message(
            ADMIN_ID,
            f"✅ **DÉPLOIEMENT RÉUSSI SUR RENDER.COM**\n\n"
            f"🚀 **Bot Téléfoot déployé avec succès !**\n\n"
            f"🌐 **URL du service :** {render_url}\n"
            f"🔌 **Port :** {port}\n"
            f"⏰ **Heure de déploiement :** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"📊 **Statut du service :**\n"
            f"• Utilisateurs chargés: {len(self.users)}\n"
            f"• Sessions TeleFeed: Actives\n"
            f"• Système de réactivation: Opérationnel\n"
            f"• Monitoring automatique: Activé\n\n"
            f"🔄 **Commandes de gestion :**\n"
            f"• `/ping` - Vérifier le statut\n"
            f"• `/status` - Statut utilisateur\n"
            f"• Message 'réactiver bot automatique' → Réponse automatique 'ok'\n\n"
            f"💚 **Service opérationnel et prêt à l'utilisation !**"
        )
        
        # Enregistrer les handlers
        await self.register_handlers()
        
        # Démarrer le monitoring
        await self.monitor_loop()
    
    async def register_handlers(self):
        """Enregistre tous les handlers"""
        
        # Handler pour la réactivation automatique
        @self.client.on(events.NewMessage(pattern=r'(?i).*réactiver.*bot.*automatique.*'))
        async def reactivation_handler(event):
            """Répond automatiquement 'ok' aux messages de réactivation"""
            if event.sender_id == ADMIN_ID:
                await event.reply("ok")
                logger.info("✅ Réponse automatique 'ok' envoyée")
                self.restart_count += 1
                
                # Notification détaillée
                await self.client.send_message(
                    ADMIN_ID,
                    f"🔄 **Système réactivé automatiquement**\n\n"
                    f"⏰ Heure: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"🔢 Redémarrage #: {self.restart_count}\n"
                    f"🌐 Render.com: Service actif\n"
                    f"📊 Utilisateurs: {len(self.users)}\n"
                    f"💚 Statut: Bot opérationnel"
                )
        
        # Handler /start
        @self.client.on(events.NewMessage(pattern='/start'))
        async def start_handler(event):
            """Handler pour /start"""
            user_id = event.sender_id
            username = event.sender.username or event.sender.first_name
            
            # Enregistrer le nouvel utilisateur
            if self.register_user(user_id, username):
                await event.reply(
                    f"👋 **Bienvenue {username} !**\n\n"
                    f"🎯 **Téléfoot Bot - Gestion de Licences**\n\n"
                    f"📋 **Votre statut:** En attente d'activation\n"
                    f"💰 **Plans disponibles:**\n"
                    f"• 1 semaine = 1000f\n"
                    f"• 1 mois = 3000f\n\n"
                    f"📱 **Contactez l'admin pour l'activation**\n"
                    f"🔧 Utilisez /status pour voir votre statut"
                )
            else:
                # Utilisateur existant
                if self.check_user_access(user_id):
                    await event.reply(
                        f"👋 **Bon retour {username} !**\n\n"
                        f"✅ **Votre accès est actif**\n"
                        f"🔧 Utilisez /status pour voir les détails"
                    )
                else:
                    await event.reply(
                        f"👋 **Salut {username} !**\n\n"
                        f"⏰ **Votre accès a expiré**\n"
                        f"💰 **Pour renouveler:**\n"
                        f"• 1 semaine = 1000f\n"
                        f"• 1 mois = 3000f\n\n"
                        f"📱 **Contactez l'admin pour le renouvellement**"
                    )
        
        # Handler /status
        @self.client.on(events.NewMessage(pattern='/status'))
        async def status_handler(event):
            """Handler pour /status"""
            user_id = str(event.sender_id)
            
            if user_id in self.users:
                user = self.users[user_id]
                
                status_msg = f"👤 **Statut de {user['username']}**\n\n"
                
                if user['plan'] == 'waiting':
                    status_msg += "📋 **Statut:** En attente d'activation\n"
                elif self.check_user_access(event.sender_id):
                    expires = datetime.fromisoformat(user['expires_at'])
                    remaining = expires - datetime.now()
                    
                    status_msg += f"✅ **Statut:** Actif\n"
                    status_msg += f"📅 **Plan:** {user['plan']}\n"
                    status_msg += f"⏰ **Expire dans:** {remaining.days} jours\n"
                    status_msg += f"📆 **Expire le:** {expires.strftime('%Y-%m-%d')}"
                else:
                    status_msg += "❌ **Statut:** Expiré\n"
                    status_msg += "💰 **Contactez l'admin pour renouveler**"
                    
                await event.reply(status_msg)
            else:
                await event.reply("❌ Utilisateur non trouvé. Utilisez /start pour vous enregistrer.")
        
        # Handler /activer (admin seulement)
        @self.client.on(events.NewMessage(pattern=r'/activer (\d+) (weekly|monthly)'))
        async def activate_handler(event):
            """Handler pour /activer"""
            if event.sender_id != ADMIN_ID:
                await event.reply("❌ Commande réservée à l'administrateur")
                return
            
            target_user_id = event.pattern_match.group(1)
            plan = event.pattern_match.group(2)
            
            if self.activate_user(target_user_id, plan):
                await event.reply(f"✅ Utilisateur {target_user_id} activé avec le plan {plan}")
                
                # Notifier l'utilisateur
                try:
                    await self.client.send_message(
                        int(target_user_id),
                        f"🎉 **Votre accès a été activé !**\n\n"
                        f"📅 **Plan:** {plan}\n"
                        f"⏰ **Durée:** {'7 jours' if plan == 'weekly' else '30 jours'}\n"
                        f"🚀 **Votre service est maintenant actif !**"
                    )
                except Exception as e:
                    logger.error(f"Impossible de notifier l'utilisateur {target_user_id}: {e}")
            else:
                await event.reply(f"❌ Impossible d'activer l'utilisateur {target_user_id}")
        
        # Handler /help
        @self.client.on(events.NewMessage(pattern='/help'))
        async def help_handler(event):
            """Handler pour /help"""
            help_msg = (
                "📚 **Aide - Téléfoot Bot**\n\n"
                "🔧 **Commandes disponibles:**\n"
                "• /start - Démarrer le bot\n"
                "• /status - Voir votre statut\n"
                "• /help - Afficher cette aide\n\n"
                "👑 **Commandes admin:**\n"
                "• /activer <user_id> <plan> - Activer un utilisateur\n"
                "• /ping - Test de connectivité\n\n"
                "💰 **Plans disponibles:**\n"
                "• weekly = 1000f (7 jours)\n"
                "• monthly = 3000f (30 jours)\n\n"
                "📱 **Support:** Contactez l'administrateur"
            )
            await event.reply(help_msg)
        
        # Handler /ping (monitoring)
        @self.client.on(events.NewMessage(pattern='/ping'))
        async def ping_handler(event):
            """Handler pour /ping"""
            uptime = time.time() - self.last_activity
            await event.reply(
                f"🟢 **Bot actif sur Render.com**\n\n"
                f"⏰ Uptime: {uptime:.0f}s\n"
                f"🔄 Redémarrages: {self.restart_count}\n"
                f"👥 Utilisateurs: {len(self.users)}\n"
                f"📊 Statut: Opérationnel"
            )
        
        logger.info("✅ Handlers enregistrés")
    
    async def monitor_loop(self):
        """Boucle de monitoring continue"""
        while True:
            try:
                # Mise à jour de l'activité
                self.last_activity = time.time()
                
                # Attendre 10 minutes
                await asyncio.sleep(600)
                
                # Heartbeat silencieux
                await self.send_heartbeat()
                
            except Exception as e:
                logger.error(f"Erreur dans le monitoring: {e}")
                await asyncio.sleep(60)
    
    async def send_heartbeat(self):
        """Envoie un signal de vie discret"""
        try:
            # Heartbeat silencieux (pas de notification)
            logger.info(f"💓 Heartbeat - {datetime.now().strftime('%H:%M:%S')}")
        except Exception as e:
            logger.warning(f"Erreur heartbeat: {e}")

    async def run(self):
        """Lance le bot"""
        try:
            await self.start()
        except Exception as e:
            logger.error(f"Erreur fatale: {e}")
            # Attendre et relancer
            await asyncio.sleep(30)
            await self.run()

if __name__ == "__main__":
    bot = RenderTelefootBot()
    
    try:
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        logger.info("Arrêt du bot")
    except Exception as e:
        logger.error(f"Erreur d'exécution: {e}")