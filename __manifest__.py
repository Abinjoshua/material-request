# -*- coding: utf-8 -*-
{
    'name': "Material Request",
    'author': "Cybrosys",
    'website': "http://www.cybrosys.com",
    'category': 'Material Request',
    'sequence': 2,
    'application': True,
    'depends': ['base', 'purchase'],
    'data':
        ["security/ir.model.access.csv",
        "security/security.xml",
        "views/material_request_views.xml",
        "views/request_products_views.xml",
         "views/material_menu_views.xml"],
}
