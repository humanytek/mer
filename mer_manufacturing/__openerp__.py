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
    'name': 'HMTK Manufacturing',
    'version': '0.1',
    'sequence': 1,
    'category': 'Custom',
    'complexity': 'easy',
    'sumary': 'Customizations in Manufacturing module',
    'description': """
Customizations in Manufacturing module

Details:
--------
* Add one2many field to append an user in a specific machine in Manufacturing/Configuration/Work Centers
* Add field "machine_id" in Manufacturing/Manufacturing/Manufacturing Orders
* Hide page "Work orders" in Manufacturing/Manufacturing/Manufacturing Orders
* Make filter and grouping by Turn in Manufacturing/Manufacturing/Manufacturing Orders
* Add menu: Manufacturing/Products/Product Variants
* Add action and tree view to show product variants in Manufacturing/Products/Product Variants
* Add field "turn_id" to associate one turn in a specific manufacturing order in Manufacturing/Manufacturing/Manufacturing Orders
* Add wizard to assign turn to some manufacturing orders at the same time
* Add attribute "required" in field "lot_id" in wizard Produce
* Add field "quantification_ids" in Manufacturing/Configuration/Work Centers
* Add fields: turn_id, operator_id, location_src_id, weight, and location_dest_id in Wizard Produce in Manufacturing/Manufacturing/Manufacturing Orders
* Add attribute "required" in field "code" in Manufacturing/Products/Bill of Materials
* Modify return of name in Bill of Materials in Manufacturing/Products/Bill of Materials
* Modify return of Products to consume in Manufacturing/Products/Bill of Materials
* Refresh records in Scheduled Products in Manufacturing/Products/Bill of Materials
* Add checking to weight before to produce some product in Wizard Produce in Manufacturing/Manufacturing/Manufacturing Orders
    """,
    'author': 'Humanytek',
    'website': 'https://github.com/humanytek/mer',
    'depends': [
        'base',
        'mrp',
        'mrp_operations',
        'hr'
    ],
    'data': [
        # Security and groups
    
        # Data
        
        # Views
        'view/manufacturing_orders.xml',
        'view/bill_of_materials.xml',
        'view/product_variants.xml',
        'view/work_centers_config.xml',
        
        # Other views
        #'view/products_to_consume.xml',
        
        # Wizard
        'wizard/production_order_group.xml',
        'wizard/turn_mrp_production.xml',
        'wizard/wizard_produce.xml',
        
        # Reports
    ],
    'demo_xml': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
