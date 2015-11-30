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

class mrp_product_produce_mer(osv.osv_memory):

    _inherit = 'mrp.product.produce'
    _description = 'Product Produce'
    _columns = {
        'turn_id': fields.many2one('resource.calendar', 'Turns'),
        'operator_id': fields.many2one('hr.employee', 'Operator'),
        'location_src_id': fields.many2one('stock.location', 
            'Raw Materials Location'),
        'location_dest_id': fields.many2one('stock.location', 
            'Finished Products Location'),
        'weight': fields.float('Weight', digits_compute=dp.get_precision('Product Unit of Measure')),
    }
    
    # 19/10/2015 (felix) Method to check weight of the product
    def on_change_weight(self, cr, uid, ids, weight, product_id, context=None):
        obj_product = self.pool.get('product.product')
        src_product = obj_product.search(cr, uid, [('id', '=', product_id)])
        if src_product:
            weight_net = obj_product.browse(cr, uid, src_product[0], context)['weight_net']
        else:
            return True
        pw = (weight_net * 20) / 100
        pw_plus = weight_net + pw
        pw_less = weight_net - pw
        if weight > pw_plus:
            raise osv.except_osv(_('Warning!'), _('The weight is superior than 20 percent permitted.'))
        if weight < pw_less:
            raise osv.except_osv(_('Warning!'), _('The weight is less than 20 percent permitted.'))
        return True

mrp_product_produce_mer()
