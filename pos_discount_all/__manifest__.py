# -*- coding: utf-8 -*-
{
    'name': 'POS Both Discounts',
    'version': '1',
    'category': 'Point Of Sale',
    'sequence': 1,
    'author': 'Damien',
    'website': '',
    'summary': 'POS Both Discounts',
    'description': """POS Both Discounts""",
    'depends': ['point_of_sale', 'account'],
    'data': [
        'views/point_of_sale.xml'
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'qweb': ['static/src/xml/pos.xml'],
    'images': [],
}
