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
    'name': 'HMTK Sales',
    'version': '0.1',
    'sequence': 1,
    'category': 'Custom',
    'complexity': 'easy',
    'sumary': 'Customizations in Sales module',
    'description': """
Customizations in Sales module

Details:
--------
* Add "Commitment date" in Sales/Sales/[Quotations|Sales]
* Add groups of security in Sales/Sales/[Quotations|Sales]
* Add customizations in sale order line in Sales/Sales/[Quotations|Sales]
* Modify behavior of product_id in sale order line in Sales/Sales/[Quotations|Sales]
    """,
    'author': 'Humanytek',
    'website': 'https://github.com/humanytek/mer',
    'depends': [
        'base',
        'sale',
    ],
    'data': [
        # Security and groups
        'security/mer_sales_security.xml',
        'security/ir.model.access.csv',
        
        # Data
        
        # Views
        'view/quotations.xml',
        'view/sales_orders.xml',
        
        # Reports
    ],
    'demo_xml': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
