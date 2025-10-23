/** @odoo-module **/

import { tour } from "@web_tour/tour_service/tour_service";
import { _t } from "@web/core/l10n/translation";

// 1. Définir le tour
tour.register('inventory_custom_onboarding_tour', {
    url: "/web",
    rainbow_mode: true, // Pour rendre les étapes très visibles
    sequence: 200, // Une séquence élevée pour s'assurer qu'il s'exécute après le chargement
    steps: [
        // Étape 1: Bienvenue dans l'App Inventaire
        {
            // Vérifie que l'icône "Inventaire" est présente dans le menu
            trigger: '.o_app[data-menu-xmlid="stock.menu_stock_root"]',
            content: _t("Bienvenue dans votre système de gestion d'inventaire ! Cliquez ici pour commencer."),
            position: 'bottom',
            timeout: 60000,
        },
        // Étape 2: Accéder aux Produits
        {
            trigger: '.o_menu_sections [data-menu-xmlid="stock.menu_stock_product_product"]',
            content: _t("Commençons par créer votre premier produit. Cliquez sur 'Produits'."),
            position: 'right',
        },
        // Étape 3: Créer un nouveau produit
        {
            trigger: '.o_list_button_add',
            content: _t("Créez un nouveau produit pour commencer votre catalogue."),
            position: 'bottom',
        },
        // Étape 4: Nom du produit
        {
            trigger: 'input[name="name"]',
            content: _t("Donnez un nom à votre produit (ex: T-shirt Bleu)."),
            position: 'right',
            run: "text T-shirt d'Exemple",
        },
        // Étape 5: Enregistrer le produit
        {
            trigger: '.o_form_button_save',
            content: _t("Excellent ! Enregistrez votre nouveau produit."),
            position: 'bottom',
        },
        // Étape 6: Fin du Tour
        {
            trigger: '.o_main_navbar',
            content: _t("C'est terminé ! Vous pouvez maintenant gérer vos stocks."),
            position: 'bottom',
            auto: true,
            timeout: 5000,
        },
    ],
});
