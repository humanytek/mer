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
    'name': 'Mercurio: Report Production Resume',
    'version': '1.0',
    'sequence': 1,
    'category': 'Custom',
    'complexity': 'easy',
    'sumary': 'mer_report_production_resume',
    'description': """
Report Production Resume

Details:
--------
* Create a visual report in graph view added on menu: Manufacturing/Report/Production resume
    """,
    'author': 'Humanytek',
    'website': 'https://github.com/humanytek/mer',
    'depends': [
        'base',
        'mrp',
        'hmtk_manufact_report',
        'mer_req_30_06_2015_a'
    ],
    'data': [
        # Security and groups
    
        # Data
        
        # Views
        'view/mrp_resume_report_view.xml',
        
        # Other views
        
        # Wizard
                
        # Reports
    ],
    'demo_xml': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
