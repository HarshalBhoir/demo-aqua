# -*- coding: utf-8 -*-
{
    'name': "set_price_from_margin",

    'summary': """
        Odoo module to set the price of product from the margin""",

    'description': """
        Odoo module to set the price of product from the margin
    """,

    'author': "B To Be Connect",
    'website': "http://www.btbc.fr/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
