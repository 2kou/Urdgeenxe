#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de déploiement automatique pour Render.com
Prépare tous les fichiers nécessaires pour l'hébergement
"""

import json
import os
import shutil
import zipfile
from datetime import datetime

def create_deployment_package():
    """Crée un package de déploiement pour Render.com"""
    
    print("📦 Création du package de déploiement Render.com...")
    
    # Créer le dossier de déploiement
    deploy_dir = "render_deployment"
    if os.path.exists(deploy_dir):
        shutil.rmtree(deploy_dir)
    os.makedirs(deploy_dir)
    
    # Fichiers essentiels à copier
    essential_files = [
        'render_deploy.py',
        'requirements_render.txt',
        'user_manager.py',
        'bot_handlers.py',
        'config.py',
        'users.json',
        'Dockerfile',
        'RENDER_DEPLOYMENT_GUIDE.md'
    ]
    
    # Copier les fichiers essentiels
    for file in essential_files:
        if os.path.exists(file):
            shutil.copy2(file, deploy_dir)
            print(f"✅ {file} copié")
        else:
            print(f"⚠️ {file} non trouvé")
    
    # Créer le fichier .env d'exemple
    env_content = """# Configuration pour Render.com
API_ID=29177661
API_HASH=a8639172fa8d35dbfd8ea46286d349ab
BOT_TOKEN=7573497633:AAHk9K15yTCiJP-zruJrc9v8eK8I9XhjyH4
ADMIN_ID=1190237801
"""
    
    with open(f"{deploy_dir}/.env.example", 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    # Créer le fichier README pour Render
    readme_content = """# Téléfoot Bot - Render Deployment

## Déploiement rapide

1. **Créer un Web Service sur Render.com**
2. **Connecter ce repository**
3. **Configurer les variables d'environnement** :
   - API_ID=29177661
   - API_HASH=a8639172fa8d35dbfd8ea46286d349ab
   - BOT_TOKEN=7573497633:AAHk9K15yTCiJP-zruJrc9v8eK8I9XhjyH4
   - ADMIN_ID=1190237801

4. **Paramètres du service** :
   - Build Command: `pip install -r requirements_render.txt`
   - Start Command: `python render_deploy.py`

5. **Déployer**

## Fonctionnalités

- Gestion de licences utilisateur
- Système d'activation admin
- Pronostics football
- Interface utilisateur complète

## Support

Bot développé pour la gestion de licences Téléfoot avec hébergement cloud optimisé.
"""
    
    with open(f"{deploy_dir}/README.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    # Créer une archive ZIP
    zip_name = f"telefoot-render-{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(deploy_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, deploy_dir)
                zipf.write(file_path, arcname)
    
    print(f"✅ Package créé : {zip_name}")
    print(f"📁 Dossier de déploiement : {deploy_dir}")
    
    return zip_name, deploy_dir

def create_github_actions():
    """Crée un workflow GitHub Actions pour le déploiement automatique"""
    
    github_dir = ".github/workflows"
    os.makedirs(github_dir, exist_ok=True)
    
    workflow_content = """name: Deploy to Render

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements_render.txt
    
    - name: Test bot import
      run: |
        python -c "from render_deploy import TelefootRenderBot; print('Bot import OK')"
    
    - name: Deploy to Render
      if: github.ref == 'refs/heads/main'
      run: |
        echo "Déploiement automatique vers Render.com"
        # Render déploie automatiquement depuis GitHub
"""
    
    with open(f"{github_dir}/deploy.yml", 'w', encoding='utf-8') as f:
        f.write(workflow_content)
    
    print("✅ Workflow GitHub Actions créé")

def show_deployment_instructions():
    """Affiche les instructions de déploiement"""
    
    print("\n" + "="*50)
    print("🚀 INSTRUCTIONS DE DÉPLOIEMENT RENDER.COM")
    print("="*50)
    
    print("\n1. 📁 UPLOADEZ LES FICHIERS :")
    print("   - Créez un repository GitHub")
    print("   - Uploadez le contenu du dossier 'render_deployment'")
    
    print("\n2. 🌐 CONFIGUREZ RENDER.COM :")
    print("   - Allez sur render.com")
    print("   - Créez un nouveau Web Service")
    print("   - Connectez votre repository GitHub")
    
    print("\n3. ⚙️ PARAMÈTRES DU SERVICE :")
    print("   - Build Command: pip install -r requirements_render.txt")
    print("   - Start Command: python render_deploy.py")
    
    print("\n4. 🔑 VARIABLES D'ENVIRONNEMENT :")
    print("   - API_ID=29177661")
    print("   - API_HASH=a8639172fa8d35dbfd8ea46286d349ab")
    print("   - BOT_TOKEN=7573497633:AAHk9K15yTCiJP-zruJrc9v8eK8I9XhjyH4")
    print("   - ADMIN_ID=1190237801")
    
    print("\n5. 🎯 DÉPLOIEMENT :")
    print("   - Cliquez sur 'Create Web Service'")
    print("   - Attendez le déploiement (2-3 minutes)")
    print("   - Vérifiez les logs pour 'Bot connecté'")
    
    print("\n6. ✅ VÉRIFICATION :")
    print("   - Testez /start sur Telegram")
    print("   - Vérifiez le statut 'Live' sur Render")
    
    print("\n" + "="*50)
    print("🎉 VOTRE BOT SERA OPÉRATIONNEL 24/7 !")
    print("="*50)

if __name__ == "__main__":
    print("🚀 Préparation du déploiement Render.com...")
    
    # Créer le package de déploiement
    zip_file, deploy_dir = create_deployment_package()
    
    # Créer les workflows GitHub Actions
    create_github_actions()
    
    # Afficher les instructions
    show_deployment_instructions()
    
    print(f"\n📦 Package prêt : {zip_file}")
    print(f"📁 Dossier prêt : {deploy_dir}")
    print("\n🎯 Suivez les instructions ci-dessus pour déployer sur Render.com")