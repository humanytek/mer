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

from openerp.osv import fields, osv
from openerp.tools.translate import _

import openerp.addons.decimal_precision as dp

class product_category(osv.osv):
    _inherit = 'product.category'
    
    _columns = {
        'labor_cost': fields.float('Cost of labor', digits_compute= dp.get_precision('Product Category')),
        'percentage_value': fields.float('Percentage value'),
        'power_factor': fields.float('Power Factor', digits_compute= dp.get_precision('Product Category')),
    }
    
product_category()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: