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
    'name': 'Reporte Gerencial',
    'version': '1.0',
    'category': 'MRP',
    'summary': 'Reporte Gerencial',
    'description': """
Management Report.
=======================
This application allows you to track your management report. 


    """,
    'author': 'Broadtech-innovations',
    'depends': ['product'],
    'website': 'http://wwww.broadtech-innovations.com',
    'data': [
#              'stock_view.xml',
        'report/reporte_gerencial_view.xml',
        ],
    'qweb': [],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
