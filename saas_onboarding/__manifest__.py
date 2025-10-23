# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "SaaS Onboarding et Routing",
    'summary': """
        Module personnalisé pour gérer l'onboarding multi-étapes, 
        le routing client (dbfilter) et le provisionnement des nouveaux tenants.
    """,
    'description': """
        - Page d'accueil personnalisée pour l'enregistrement, la connexion et l'invitation.
        - Logique de redirection vers le sous-domaine/tenant approprié.
        - Web Tour personnalisé pour guider les nouveaux utilisateurs dans l'application Inventaire.
    """,
    'author': "Votre Nom",
    'website': "http://www.mondev.com",
    'category': 'Website/Website',
    'version': '1.0',

    # Les dépendances (modules nécessaires au fonctionnement de celui-ci)
    'depends': [
        'base', 
        'website', 
        'web_tour',  # Nécessaire pour les Web Tours
        'stock',     # Nécessaire si le Web Tour cible l'application Inventaire (stock)
    ],

    # Fichiers de données et de vues
    'data': [
        # Les vues XML pour la page d'onboarding, les formulaires et les redirections
        'views/onboarding_templates.xml',
    ],

    # Déclaration des assets (fichiers JS/CSS qui doivent être chargés dans le navigateur)
    'assets': {
        'web.assets_backend': [
            # Déclaration du Web Tour pour le backend Odoo
            'saas_onboarding/static/src/js/inventory_onboarding_tour.js',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
