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
    'name': 'Mercurio: req_30_06_2015_a',
    'version': '1.5',
    'sequence': 1,
    'category': 'Custom',
    'complexity': 'easy',
    'sumary': 'mer_req_30_06_2015_a',
    'description': """
Customizations in Manufacturing module

Details:
--------
* Add fields: turn_id, operator_id, hours, location_src_id, weight, and location_dest_id in Wizard Produce in Manufacturing/Manufacturing/Manufacturing Orders
* Add behavior in methods to produce a product, change location_dest_id fields, take value from produce wizard
    """,
    'author': 'Humanytek',
    'website': 'https://github.com/humanytek/mer',
    'depends': [
        'base',
        'mrp',
        'mrp_operations',
        'hr',
    ],
    'data': [
        # Security and groups
    
        # Data
        
        # Views
        
        # Other views
        
        # Wizard
        'wizard/wizard_produce.xml',
        
        # Reports
    ],
    'demo_xml': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
