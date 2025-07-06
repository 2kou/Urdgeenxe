#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bot Téléfoot optimisé pour Render.com
Version web service pour hébergement cloud
"""

import asyncio
import signal
import sys
import os
import threading
from datetime import datetime
from telethon import TelegramClient
from telethon.errors import AuthKeyError, FloodWaitError
from flask import Flask, jsonify
import logging

# Configuration des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration depuis les variables d'environnement
API_ID = int(os.getenv('API_ID', '29177661'))
API_HASH = os.getenv('API_HASH', 'a8639172fa8d35dbfd8ea46286d349ab')
BOT_TOKEN = os.getenv('BOT_TOKEN', '7573497633:AAHk9K15yTCiJP-zruJrc9v8eK8I9XhjyH4')
ADMIN_ID = int(os.getenv('ADMIN_ID', '1190237801'))
PORT = int(os.getenv('PORT', '10000'))

# Import des modules locaux
from user_manager import UserManager
from bot_handlers import BotHandlers

# Application Flask pour satisfaire les exigences de Render.com
app = Flask(__name__)

# Variables globales pour le bot
bot_instance = None
bot_running = False

@app.route('/')
def health_check():
    """Endpoint de santé pour Render.com"""
    global bot_instance, bot_running
    
    status = {
        "service": "Téléfoot Bot",
        "status": "running" if bot_running else "starting",
        "bot_connected": bot_instance.client.is_connected() if bot_instance and bot_instance.client else False,
        "timestamp": datetime.now().isoformat()
    }
    return jsonify(status)

@app.route('/status')
def bot_status():
    """Status détaillé du bot"""
    global bot_instance, bot_running
    
    if not bot_instance:
        return jsonify({"error": "Bot non initialisé"}), 503
    
    return jsonify({
        "bot_running": bot_running,
        "client_connected": bot_instance.client.is_connected() if bot_instance.client else False,
        "users_count": len(bot_instance.user_manager.users) if bot_instance.user_manager else 0,
        "uptime": "Active depuis le démarrage"
    })

class TelefootRenderBot:
    """Bot Telegram optimisé pour Render.com"""
    
    def __init__(self):
        self.client = None
        self.user_manager = UserManager()
        self.handlers = None
        self.running = False
    
    async def initialize(self):
        """Initialise le client Telegram"""
        try:
            self.client = TelegramClient(
                'bot_session', 
                API_ID, 
                API_HASH
            )
            
            await self.client.start(bot_token=BOT_TOKEN)
            me = await self.client.get_me()
            logger.info(f"Bot connecté : @{me.username} ({me.id})")
            
            # Initialisation des handlers
            self.handlers = BotHandlers(self.client, self.user_manager)
            
            logger.info("Bot initialisé avec succès")
            return True
            
        except AuthKeyError:
            logger.error("Erreur d'authentification")
            return False
        except Exception as e:
            logger.error(f"Erreur d'initialisation : {e}")
            return False
    
    async def start(self):
        """Démarre le bot"""
        global bot_running
        
        if not await self.initialize():
            return False
        
        self.running = True
        bot_running = True
        logger.info("Bot démarré sur Render.com")
        
        try:
            if self.client:
                await self.client.run_until_disconnected()
        except KeyboardInterrupt:
            logger.info("Arrêt du bot demandé")
        except Exception as e:
            logger.error(f"Erreur : {e}")
        finally:
            await self.stop()
        
        return True
    
    async def stop(self):
        """Arrête le bot"""
        global bot_running
        
        self.running = False
        bot_running = False
        if self.client and self.client.is_connected():
            await self.client.disconnect()
        logger.info("Bot arrêté")

def run_bot():
    """Lance le bot dans un thread séparé"""
    global bot_instance
    
    async def start_bot():
        bot_instance = TelefootRenderBot()
        await bot_instance.start()
    
    # Créer une nouvelle boucle d'événements pour ce thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_bot())

def signal_handler(sig, frame):
    """Gestionnaire de signal"""
    logger.info(f"Signal {sig} reçu")
    sys.exit(0)

if __name__ == "__main__":
    # Configuration des signaux
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Démarrer le bot dans un thread séparé
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Lancer l'application Flask sur le port requis par Render.com
    logger.info(f"Démarrage du serveur Flask sur le port {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=False)