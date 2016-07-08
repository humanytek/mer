# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
import time

from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class mrp_product_produce_operators_mer(osv.osv):

    _name = 'mrp.product.produce.operators'
    _description = 'Product Produce Operators'
    _columns = {
        'turn_id': fields.many2one('resource.calendar', 'Turns'),
        'operator_id': fields.many2one('hr.employee', 'Operator'),
        'hours': fields.float('Hours'),
        'operators_id': fields.many2one('mrp.product.produce', 'Operators')
    }

mrp_product_produce_operators_mer()
