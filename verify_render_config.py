#!/usr/bin/env python3
"""
Script de vérification complète de la configuration Render.com
"""

import os
import json
import sys

def check_files():
    """Vérifie la présence des fichiers requis"""
    print("📁 VÉRIFICATION DES FICHIERS:")
    
    required_files = [
        'render_deploy.py',
        'requirements_render.txt', 
        'user_manager.py',
        'bot_handlers.py',
        'config.py',
        'users.json'
    ]
    
    all_present = True
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file} ({size} bytes)")
        else:
            print(f"❌ {file} MANQUANT")
            all_present = False
    
    return all_present

def check_requirements():
    """Vérifie le fichier requirements"""
    print("\n📦 DÉPENDANCES:")
    
    try:
        with open('requirements_render.txt', 'r') as f:
            deps = f.read().strip().split('\n')
        
        required_deps = ['telethon', 'flask', 'requests']
        for dep in deps:
            if dep.strip():
                print(f"✅ {dep}")
        
        # Vérifier que Flask est présent
        has_flask = any('flask' in dep.lower() for dep in deps)
        if has_flask:
            print("✅ Flask inclus pour serveur web")
        else:
            print("❌ Flask manquant - requis pour Render.com")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur lecture requirements: {e}")
        return False

def check_render_deploy():
    """Vérifie render_deploy.py"""
    print("\n🔧 RENDER_DEPLOY.PY:")
    
    try:
        with open('render_deploy.py', 'r') as f:
            content = f.read()
        
        checks = [
            ('Flask importé', 'from flask import Flask' in content),
            ('Port configuré', 'PORT = int(os.getenv' in content),
            ('Routes définies', '@app.route' in content),
            ('Threading utilisé', 'threading' in content),
            ('TelegramClient présent', 'TelegramClient' in content),
            ('App Flask créée', 'app = Flask(__name__)' in content),
            ('Serveur lancé', 'app.run(' in content)
        ]
        
        all_good = True
        for check_name, result in checks:
            status = "✅" if result else "❌"
            print(f"{status} {check_name}")
            if not result:
                all_good = False
        
        return all_good
        
    except Exception as e:
        print(f"❌ Erreur lecture render_deploy.py: {e}")
        return False

def check_config():
    """Vérifie la configuration"""
    print("\n⚙️ CONFIGURATION:")
    
    try:
        # Vérifier config.py
        with open('config.py', 'r') as f:
            config_content = f.read()
        
        config_checks = [
            ('API_ID défini', 'API_ID' in config_content),
            ('API_HASH défini', 'API_HASH' in config_content),
            ('BOT_TOKEN défini', 'BOT_TOKEN' in config_content),
            ('ADMIN_ID défini', 'ADMIN_ID' in config_content)
        ]
        
        for check_name, result in config_checks:
            status = "✅" if result else "❌"
            print(f"{status} {check_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur config.py: {e}")
        return False

def check_users():
    """Vérifie users.json"""
    print("\n👥 USERS.JSON:")
    
    try:
        with open('users.json', 'r') as f:
            users = json.load(f)
        
        print(f"✅ {len(users)} utilisateurs chargés")
        
        for user_id, user_data in users.items():
            status = user_data.get('status', 'unknown')
            print(f"  • {user_id}: {status}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur users.json: {e}")
        return False

def show_deployment_config():
    """Affiche la configuration de déploiement"""
    print("\n🚀 CONFIGURATION RENDER.COM:")
    print("-" * 40)
    print("Build Command:")
    print("  pip install -r requirements_render.txt")
    print()
    print("Start Command:")
    print("  python render_deploy.py")
    print()
    print("Variables d'environnement:")
    print("  API_ID=29177661")
    print("  API_HASH=a8639172fa8d35dbfd8ea46286d349ab")
    print("  BOT_TOKEN=7573497633:AAHk9K15yTCiJP-zruJrc9v8eK8I9XhjyH4")
    print("  ADMIN_ID=1190237801")
    print("  PORT=10000 (optionnel)")

def main():
    """Fonction principale"""
    print("🔍 VÉRIFICATION COMPLÈTE - RENDER.COM")
    print("=" * 50)
    
    # Changer de répertoire si nécessaire
    if os.path.exists('render_deployment'):
        os.chdir('render_deployment')
        print("📂 Vérification dans render_deployment/")
    
    checks = [
        ("Fichiers requis", check_files()),
        ("Dépendances", check_requirements()),
        ("Script de déploiement", check_render_deploy()),
        ("Configuration", check_config()),
        ("Base de données", check_users())
    ]
    
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES VÉRIFICATIONS:")
    
    all_passed = True
    for check_name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {check_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 TOUTES LES VÉRIFICATIONS RÉUSSIES!")
        print("✅ Package prêt pour Render.com")
        show_deployment_config()
    else:
        print("❌ CERTAINES VÉRIFICATIONS ONT ÉCHOUÉ")
        print("🔧 Corrigez les erreurs avant de déployer")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)