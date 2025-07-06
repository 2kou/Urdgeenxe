#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de vérification du déploiement Render.com
Teste que tous les composants fonctionnent correctement
"""

import os
import json
import sys

def test_imports():
    """Test que tous les modules s'importent correctement"""
    print("🔍 Test des imports...")
    
    try:
        from telethon import TelegramClient
        print("✅ Telethon importé")
    except ImportError as e:
        print(f"❌ Erreur Telethon: {e}")
        return False
    
    try:
        from user_manager import UserManager
        print("✅ UserManager importé")
    except ImportError as e:
        print(f"❌ Erreur UserManager: {e}")
        return False
    
    try:
        from bot_handlers import BotHandlers
        print("✅ BotHandlers importé")
    except ImportError as e:
        print(f"❌ Erreur BotHandlers: {e}")
        return False
    
    try:
        from config import API_ID, API_HASH, BOT_TOKEN, ADMIN_ID
        print("✅ Configuration importée")
    except ImportError as e:
        print(f"❌ Erreur Config: {e}")
        return False
    
    return True

def test_configuration():
    """Test que la configuration est valide"""
    print("\n🔍 Test de la configuration...")
    
    # Variables d'environnement
    required_vars = ['API_ID', 'API_HASH', 'BOT_TOKEN', 'ADMIN_ID']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️ Variables manquantes: {', '.join(missing_vars)}")
        print("💡 Utilisez les valeurs par défaut du code")
    else:
        print("✅ Variables d'environnement présentes")
    
    # Test des valeurs de configuration
    from config import API_ID, API_HASH, BOT_TOKEN, ADMIN_ID
    
    if API_ID and len(str(API_ID)) > 5:
        print("✅ API_ID valide")
    else:
        print("❌ API_ID invalide")
        return False
    
    if API_HASH and len(API_HASH) > 20:
        print("✅ API_HASH valide")
    else:
        print("❌ API_HASH invalide")
        return False
    
    if BOT_TOKEN and ':' in BOT_TOKEN:
        print("✅ BOT_TOKEN valide")
    else:
        print("❌ BOT_TOKEN invalide")
        return False
    
    if ADMIN_ID and len(str(ADMIN_ID)) > 5:
        print("✅ ADMIN_ID valide")
    else:
        print("❌ ADMIN_ID invalide")
        return False
    
    return True

def test_data_files():
    """Test que les fichiers de données existent"""
    print("\n🔍 Test des fichiers de données...")
    
    # Test users.json
    if os.path.exists('users.json'):
        try:
            with open('users.json', 'r', encoding='utf-8') as f:
                users = json.load(f)
            print(f"✅ users.json valide ({len(users)} utilisateurs)")
        except json.JSONDecodeError:
            print("❌ users.json corrompu")
            return False
    else:
        print("⚠️ users.json manquant (sera créé automatiquement)")
    
    return True

def test_bot_creation():
    """Test que le bot peut être créé"""
    print("\n🔍 Test de création du bot...")
    
    try:
        from render_deploy import TelefootRenderBot
        bot = TelefootRenderBot()
        print("✅ Bot créé avec succès")
        return True
    except Exception as e:
        print(f"❌ Erreur création bot: {e}")
        return False

def show_deployment_summary():
    """Affiche un résumé du déploiement"""
    print("\n" + "="*50)
    print("📊 RÉSUMÉ DU DÉPLOIEMENT")
    print("="*50)
    
    print("\n📦 Fichiers prêts pour Render.com :")
    files_to_deploy = [
        'render_deploy.py',
        'requirements_render.txt',
        'user_manager.py',
        'bot_handlers.py',
        'config.py',
        'users.json'
    ]
    
    for file in files_to_deploy:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} manquant")
    
    print("\n🔧 Configuration Render.com :")
    print("Build Command: pip install -r requirements_render.txt")
    print("Start Command: python render_deploy.py")
    
    print("\n🔑 Variables d'environnement requises :")
    print("API_ID=29177661")
    print("API_HASH=a8639172fa8d35dbfd8ea46286d349ab")
    print("BOT_TOKEN=7573497633:AAHk9K15yTCiJP-zruJrc9v8eK8I9XhjyH4")
    print("ADMIN_ID=1190237801")

def main():
    """Fonction principale de vérification"""
    print("🚀 Vérification du déploiement Render.com")
    print("="*50)
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_configuration),
        ("Fichiers de données", test_data_files),
        ("Création du bot", test_bot_creation)
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        try:
            if not test_func():
                all_passed = False
        except Exception as e:
            print(f"❌ Erreur dans {test_name}: {e}")
            all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 TOUS LES TESTS PASSÉS !")
        print("✅ Prêt pour le déploiement sur Render.com")
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("🔧 Corrigez les erreurs avant de déployer")
    
    show_deployment_summary()
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)