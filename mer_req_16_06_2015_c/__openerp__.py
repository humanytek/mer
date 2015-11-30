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
    'name': 'Mercurio: req_16_06_2015_c',
    'version': '0.1',
    'sequence': 1,
    'category': 'Custom',
    'complexity': 'easy',
    'sumary': 'mer_req_16_06_2015_c',
    'description': """
Customizations in HR module

Details:
--------
* Add menu to administrate kind of salaries
* Add salary field in Employees form
    """,
    'author': 'Humanytek',
    'website': 'https://github.com/humanytek/mer',
    'depends': [
        'base',
        'hr',
        'hr_attendance',
        'hr_timesheet',
    ],
    'data': [
        # Security and groups
    
        # Data
        
        # Views
        'view/employees.xml',
        'view/kind_salaries_config.xml',
        
        # Reports
    ],
    'demo_xml': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
