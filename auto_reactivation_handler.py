"""
Handler pour la réactivation automatique Render.com
À intégrer dans le bot principal
"""

from telethon import events
from datetime import datetime

def setup_reactivation_handler(bot, admin_id, user_manager):
    """Configure le handler de réactivation automatique"""
    
    @bot.on(events.NewMessage(pattern=r'(?i).*réactiver.*bot.*automatique.*'))
    async def reactivation_handler(event):
        """Répond automatiquement 'ok' aux messages de réactivation Render.com"""
        if event.sender_id == admin_id:
            await event.reply("ok")
            print(f"✅ Réponse automatique 'ok' envoyée à {event.sender_id}")
            
            # Notification détaillée
            await bot.send_message(
                admin_id,
                f"🔄 **Bot réactivé automatiquement par Render.com**\n\n"
                f"⏰ Heure: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"🌐 Statut: Service opérationnel\n"
                f"📊 Utilisateurs actifs: {len(user_manager.users)}\n"
                f"💚 Monitoring: Actif"
            )
    
    @bot.on(events.NewMessage(pattern=r'(?i).*(ping|test|alive|status).*'))
    async def health_check_handler(event):
        """Répond aux vérifications de santé"""
        if event.sender_id == admin_id:
            await event.reply(
                f"🟢 **Bot actif sur Render.com**\n\n"
                f"📊 Utilisateurs: {len(user_manager.users)}\n"
                f"💚 Statut: Opérationnel\n"
                f"🔄 Monitoring: Actif"
            )
    
    print("🔄 Système de réactivation automatique Render.com configuré")