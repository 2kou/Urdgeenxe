
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de redémarrage automatique pour le bot Téléfoot
"""

import asyncio
import subprocess
import time
import os
from datetime import datetime

class AutoRestart:
    def __init__(self):
        self.max_restarts = 10
        self.restart_count = 0
        self.last_restart = None
    
    async def monitor_bot(self):
        """Surveille le bot et le redémarre si nécessaire"""
        print("🔄 Démarrage du moniteur de redémarrage automatique")
        
        while self.restart_count < self.max_restarts:
            try:
                # Démarrer le bot principal
                print(f"🚀 Démarrage du bot (tentative {self.restart_count + 1})")
                process = await asyncio.create_subprocess_exec(
                    'python', 'main.py',
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                # Attendre que le processus se termine
                stdout, stderr = await process.communicate()
                
                self.restart_count += 1
                self.last_restart = datetime.now()
                
                print(f"⚠️ Bot arrêté (code: {process.returncode})")
                if stderr:
                    print(f"Erreur: {stderr.decode()}")
                
                # Attendre avant de redémarrer
                wait_time = min(30 * self.restart_count, 300)  # Max 5 minutes
                print(f"⏱️ Redémarrage dans {wait_time} secondes...")
                await asyncio.sleep(wait_time)
                
            except KeyboardInterrupt:
                print("\n⏹️ Arrêt du moniteur demandé")
                break
            except Exception as e:
                print(f"❌ Erreur dans le moniteur: {e}")
                await asyncio.sleep(60)
        
        print(f"⚠️ Nombre maximum de redémarrages atteint ({self.max_restarts})")

if __name__ == "__main__":
    restart_monitor = AutoRestart()
    asyncio.run(restart_monitor.monitor_bot())
