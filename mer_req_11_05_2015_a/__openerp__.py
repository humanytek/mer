# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Humanytek (<http://humanytek.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Mercurio: req_11_05_2015_a',
    'version': '0.1',
    'sequence': 1,
    'category': 'Custom',
    'complexity': 'easy',
    'sumary': 'mer_req_11_05_2015_a',
    'description': """
Customizations in Warehouse module

Details:
--------
* Add field "is_customizable" in Products/Products
* Add page "Customization" in Products/Products
* Add image in customization line in Products/Products
    """,
    'author': 'Humanytek',
    'website': 'https://github.com/humanytek/mer',
    'depends': [
        'base',
        'stock',
        'product',
    ],
    'data': [
        # Security and groups
    
        # Data
        
        # Views
        #'view/products.xml',
        'view/product_variants.xml',
        'view/product_custom_type.xml',
        
        # Reports
    ],
    'demo_xml': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
