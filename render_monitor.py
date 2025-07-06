"""
Système de monitoring automatique pour Render.com
Détecte les problèmes et envoie un message de réactivation
"""

import asyncio
import logging
import os
import time
from datetime import datetime
from telethon import TelegramClient, events
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

class RenderMonitor:
    def __init__(self):
        self.client = TelegramClient('render_monitor', API_ID, API_HASH)
        self.last_activity = time.time()
        self.monitoring = True
        self.restart_count = 0
        
    async def start(self):
        """Démarre le système de monitoring"""
        await self.client.start(bot_token=BOT_TOKEN)
        logger.info("🔄 Système de monitoring Render.com démarré")
        
        # Handler pour le message de réactivation
        @self.client.on(events.NewMessage(pattern=r'(?i).*réactiver.*bot.*automatique.*'))
        async def reactivation_handler(event):
            """Répond automatiquement aux messages de réactivation"""
            if event.sender_id == ADMIN_ID:
                await event.reply("ok")
                logger.info("✅ Réponse automatique 'ok' envoyée")
                self.restart_count += 1
                
                # Notification de statut
                await self.client.send_message(
                    ADMIN_ID,
                    f"🔄 **Système réactivé automatiquement**\n\n"
                    f"⏰ Heure: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"🔢 Redémarrage #: {self.restart_count}\n"
                    f"🌐 Statut: Bot opérationnel\n"
                    f"📡 Render.com: Service actif"
                )
        
        # Handler pour les messages de test de vie
        @self.client.on(events.NewMessage(pattern=r'(?i).*(ping|test|alive|status).*'))
        async def health_check_handler(event):
            """Répond aux vérifications de santé"""
            if event.sender_id == ADMIN_ID:
                await event.reply(
                    f"🟢 **Bot actif sur Render.com**\n\n"
                    f"⏰ Uptime: {time.time() - self.last_activity:.0f}s\n"
                    f"🔄 Redémarrages: {self.restart_count}\n"
                    f"📊 Statut: Opérationnel"
                )
        
        # Monitoring continu
        await self.monitor_loop()
    
    async def monitor_loop(self):
        """Boucle principale de monitoring"""
        while self.monitoring:
            try:
                # Mise à jour de l'activité
                self.last_activity = time.time()
                
                # Vérification périodique (toutes les 5 minutes)
                await asyncio.sleep(300)
                
                # Envoi d'un heartbeat au serveur
                await self.send_heartbeat()
                
            except Exception as e:
                logger.error(f"Erreur dans le monitoring: {e}")
                await asyncio.sleep(60)  # Attendre 1 minute avant de réessayer
    
    async def send_heartbeat(self):
        """Envoie un signal de vie"""
        try:
            await self.client.send_message(
                ADMIN_ID,
                f"💓 Heartbeat - {datetime.now().strftime('%H:%M:%S')}",
                silent=True
            )
        except Exception as e:
            logger.warning(f"Impossible d'envoyer le heartbeat: {e}")

    async def handle_restart_command(self, event):
        """Gère la commande de redémarrage"""
        try:
            await event.reply("🔄 Redémarrage du système...")
            logger.info("Redémarrage demandé par l'admin")
            
            # Notification avant redémarrage
            await self.client.send_message(
                ADMIN_ID,
                "🔄 **Redémarrage en cours...**\n\n"
                "⏰ Le bot redémarre automatiquement\n"
                "🔔 Vous recevrez une notification quand il sera prêt"
            )
            
            # Redémarrage propre
            await self.client.disconnect()
            await asyncio.sleep(2)
            await self.start()
            
        except Exception as e:
            logger.error(f"Erreur lors du redémarrage: {e}")

if __name__ == "__main__":
    monitor = RenderMonitor()
    
    try:
        asyncio.run(monitor.start())
    except KeyboardInterrupt:
        logger.info("Arrêt du monitoring")
    except Exception as e:
        logger.error(f"Erreur fatale: {e}")