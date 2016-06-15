# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2013 BroadTech IT Solutions.
#    (http://wwww.broadtech-innovations.com)
#    contact@broadtech-innovations.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Manufacturing Order Customization',
    'version': '1.5',
    'category': 'Manufacturing Order Customization',
    'summary': 'Manufacturing Order Quantity Calculation',
    'description': """
Manage Manufacturing Order Quantity.
=======================
This application will change the manufacturing order quantity with respect to available product quantity

    """,
    'author': 'Broadtech-innovations',
    'depends': ['mrp', 'procurement', 'procurement_jit'],
    'website': 'http://wwww.broadtech-innovations.com',
    'data': [ ],
    'qweb': [ ],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
