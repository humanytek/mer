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
    'name': 'HMTK Ventas/Ventas',
    'version': '1.1',
    'sequence': 1,
    'category': 'Custom',
    'complexity': 'easy',
    'description': """
Módulo de Ventas, modificado para cubrir requerimientos de Tucané.

Detalles:
---------
* Cambios en submenú Ventas/Ventas/Cotizaciones
    * Desglose de productos y sus respectivos atributos con variantes aparte
    * Quitar columna de atributos
    * Agregar columnas: Talla, Color, Departamento, Colección
    """,
    'author': 'Humanytek',
    'website': 'http://humanytek.com',
    'depends': [
        'base',
        'sale'
    ],
    'data': [
        # Seguridad y grupos
    
        # Data
        
        # Vistas
        'view/cotizaciones.xml',
        
        # Reportes
    ],
    'demo_xml': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
