{
    'name': 'Inventory SaaS',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Adds SaaS specific features to inventory and products.',
    # CRITICAL FIX: Added 'product' and 'website' to dependencies
    # 'product' is needed because product_template_form_view is inherited.
    # 'website' is needed because website.homepage is inherited.
    'depends': ['stock', 'product', 'website'],
    'data': [
        'views/product_view.xml',
        'views/website_templates.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
