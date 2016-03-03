# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2013 BroadTech IT Solutions.
#    (http://wwww.broadtech-innovations.com)
#    contact@boradtech-innovations.com
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
    'version': '1.3',
    'category': 'Customer Relationship Management',
    'summary': 'Manage Point of sale activities',
    'description': """
Manage Customer Claims.
=======================
This application allows you to track your customers/suppliers claims and grievances.

It is fully integrated with the email gateway so that you can create
automatically new claims based on incoming emails.

    """,
    'author': 'Broadtech-innovations',
    'depends': ['mrp'],
    'website': 'http://wwww.broadtech-innovations.com',
    'data': [
            'mrp_view.xml'
        ],
    'qweb': [],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
