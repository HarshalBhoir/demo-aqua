# -*- coding: utf-8 -*-
{
    'name': "sport_management",

    'summary': """
        This is a great module""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Noosys",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'website', 'calendar','contacts'],

    # always loaded
    'data': [
        'data/module_data.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/sport_type_course_view.xml',
        'views/sport_account_view.xml',
        'views/sport_credit_view.xml',
        'data/cron.xml',
        'views/res_partner_view.xml',
        'views/sport_badge_view.xml',
        'views/sale_order_view.xml',
        'views/sport_session_view.xml',
        'views/sport_subscription_view.xml',
        'views/web_template.xml',
        'views/client_interface.xml',
        'views/sport_course_view.xml',
        'views/sport_credit_type_view.xml',
        'views/product_template_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    
    'application': True,
}