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
    'name': 'Mercurio: Process of Quality',
    'version': '1.3',
    'sequence': 1,
    'category': 'Custom',
    'complexity': 'easy',
    'sumary': 'mer_process_quality',
    'description': """
Process of Quality

Details:
--------
* Add catalog of reasons for each lot in Manufacturing/Configuration
* Form view, moved to: Manufacturing/Manufacturing/Manufacturing orders (Wizard)
    """,
    'author': 'Humanytek',
    'website': 'https://github.com/humanytek/mer',
    'depends': [
        'base',
        'mrp',
        'mer_req_30_06_2015_a'
    ],
    'data': [
        # Security and groups
    
        # Data
        
        # Views
        #'view/serial_numbers.xml',
        'view/process_quality_config.xml',
        
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
