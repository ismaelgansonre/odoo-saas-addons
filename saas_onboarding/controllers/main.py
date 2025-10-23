# Fichier: saas_onboarding/controllers/main.py
import base64
import os
import secrets
from odoo import http
from odoo.http import request

# ATTENTION: Remplacez 'localhost:8069' par votre domaine principal pour l'onboarding
# Le dbfilter doit être désactivé sur ce domaine pour afficher l'onboarding/landing page
MAIN_DOMAIN = 'localhost:8069' 
TENANT_DOMAIN = 'mondev.com' # Le domaine racine pour les tenants
TENANT_SUFFIX = f'.{TENANT_DOMAIN}' # Suffixe pour la DB, doit correspondre à l'hôte !

class SaasOnboarding(http.Controller):

    # --------------------------------------------------------------------------
    # Logique de Redirection Automatique et Page d'Accueil
    # --------------------------------------------------------------------------
    @http.route('/', type='http', auth="public", website=True)
    def index_route(self, **kw):
        """
        Gère le point d'entrée unique. Redirige les clients existants vers leur DB.
        Affiche l'onboarding sur le domaine principal (MAIN_DOMAIN).
        """
        host = request.httprequest.get_host()
        
        # Le nom d'hôte sans le port (si présent)
        host_no_port = host.split(':')[0]

        # 1. Si nous sommes déjà dans une DB (cela signifie que dbfilter a trouvé une DB)
        if request.db:
            # Si c'est la DB Maître (souvent nommée 'odoo' ou 'localhost' dans les tests)
            # Et si nous sommes sur le domaine principal MAIN_DOMAIN, nous affichons l'onboarding
            # Sauf si l'utilisateur est déjà logué et qu'il y a une page d'accueil par défaut
            if host == MAIN_DOMAIN:
                 # Si l'utilisateur est déjà authentifié, le renvoyer vers son espace de travail /web
                if request.env.user.id and request.env.user != request.env.ref('base.public_user'):
                    return request.redirect('/web') 
                
                # Sinon, afficher l'onboarding sur le domaine principal
                return request.render('saas_onboarding.onboarding_landing_page')
            
            # Si nous sommes sur un domaine client (ex: client1.localhost), rediriger vers le login/web
            return request.redirect('/web/login')


        # 2. Si AUCUNE DB n'est sélectionnée (comportement souhaité sur MAIN_DOMAIN)
        if host == MAIN_DOMAIN or host_no_port == MAIN_DOMAIN.split(':')[0]:
            # Afficher l'écran d'onboarding/landing page qui gère les 3 objectifs
            return request.render('saas_onboarding.onboarding_landing_page')
        
        # Cas de domaine inconnu ou de sous-domaine sans DB associée
        return request.not_found()


    # --------------------------------------------------------------------------
    # Logique du Formulaire d'Onboarding (3 Objectifs)
    # --------------------------------------------------------------------------
    @http.route('/saas/onboarding/process', type='http', auth="public", website=True, methods=['POST'])
    def onboarding_step_process(self, action_type, **post):
        """
        Gère l'action choisie (Créer, Se Connecter, Rejoindre).
        Ceci contient la logique de provisionnement des DB (simulée).
        """
        
        # --- 1. Client Nouveau (Créer un nouveau système d'inventaire) ---
        if action_type == 'create_new':
            company_name = post.get('company_name')
            email = post.get('email')
            password = post.get('password')
            name = post.get('name')
            phone = post.get('phone') # Récupérer les infos de l'utilisateur

            if not company_name or not email or not password:
                return request.redirect('/')

            # 1. Nettoyage du nom pour le sous-domaine et la base de données
            subdomain = company_name.lower().replace(' ', '').replace('.', '').replace('-', '')
            
            # CRITICAL: Le nom de la DB DOIT correspondre exactement à l'hôte pour dbfilter = ^%h$
            # L'hôte sera 'maboite.mondev.com'
            db_name = f'{subdomain}{TENANT_SUFFIX}' 
            
            # --- LOGIQUE CRITIQUE DE PROVISIONNEMENT (SIMULATION) ---
            try:
                # TODO: Remplacer par l'appel RPC au db_manager pour créer la DB 'db_name'.
                
                # NOTE: Si la création échoue, vous devez créer manuellement une DB nommée EXACTEMENT db_name (ex: maboite.mondev.com)
                
                print(f"--- SIMULATION: Tentative de création de la DB nommée '{db_name}'...")
                
                # Construction de l'URL pour la redirection
                host_parts = MAIN_DOMAIN.split(':')
                # L'URL doit être http://maboite.mondev.com:8069/web
                new_url = f'http://{subdomain}.{TENANT_DOMAIN}:{host_parts[1]}/web'

                return request.render('saas_onboarding.onboarding_success_redirect', {
                    'url': new_url,
                    'db_name': db_name,
                    'company_name': company_name,
                    'message': f'Votre espace est créé à {subdomain}.{TENANT_DOMAIN}. Redirection...'
                })
                
            except Exception as e:
                # Gérer les erreurs de provisionnement (DB déjà existante, etc.)
                return request.render('saas_onboarding.onboarding_error', {'error': str(e)})

        # --- 2. Client Existant (Connexion sur un tenant connu) ---
        elif action_type == 'login_existing':
            # Cette option est simplement un lien vers l'écran de login par défaut.
            # L'utilisateur DOIT connaître son sous-domaine pour que le dbfilter fonctionne.
            return request.redirect('/web/login')
        
        # --- 3. Client Invité (Connexion avec code d'équipe) ---
        elif action_type == 'join_team':
            invitation_code = post.get('invitation_code')
            email = post.get('email')
            password = post.get('password')

            if not invitation_code or not email or not password:
                return request.render('saas_onboarding.onboarding_error', {'error': "Informations manquantes pour rejoindre l'équipe."})

            # --- LOGIQUE DE REJOINDRE ÉQUIPE (SIMULATION) ---
            
            # SIMULATION: Le code d'invitation est le nom du sous-domaine (ex: 'equipetest')
            existing_subdomain = invitation_code.lower().replace(' ', '').replace('.', '').replace('-', '')
            db_name = f'{existing_subdomain}{TENANT_SUFFIX}'
            
            # SIMULATION DE REDIRECTION
            host_parts = MAIN_DOMAIN.split(':')
            existing_url = f'http://{existing_subdomain}.{TENANT_DOMAIN}:{host_parts[1]}/web'

            return request.render('saas_onboarding.onboarding_success_redirect', {
                'url': existing_url,
                'db_name': db_name,
                'company_name': f'Équipe {invitation_code}',
                'message': 'Vous avez rejoint l\'équipe. Redirection vers leur espace de travail...'
            })

        # Fallback
        return request.redirect('/')
