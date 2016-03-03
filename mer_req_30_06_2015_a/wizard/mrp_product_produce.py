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
import logging
_logger = logging.getLogger(__name__)

class mrp_product_produce_mer(osv.osv_memory):

    _inherit = 'mrp.product.produce'
    _description = 'Product Produce'
    _columns = {
        'location_src_id': fields.many2one('stock.location', 
            'Raw Materials Location'),
        'location_dest_id': fields.many2one('stock.location', 
            'Finished Products Location'),
        'weight': fields.float('Weight', digits_compute=dp.get_precision('Product Unit of Measure')),
        'operators_ids': fields.one2many('mrp.product.produce.operators', 
            'operators_id', 'Operators'),
        'main_turn_id': fields.many2one('resource.calendar', type='many2one'),
        'machine_id': fields.many2one('mrp.workcenter', type='many2one'),
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
        
    # 26/02/2016 (felix) Original method to send the destiny location
    def do_produce(self, cr, uid, ids, context=None):
        production_id = context.get('active_id', False)
        assert production_id, "Production Id should be specified in context as a Active ID."
        data = self.browse(cr, uid, ids[0], context=context)
        self.pool.get('mrp.production').action_produce(cr, uid, production_id,
            data.product_qty, data.mode, data.location_dest_id, data, context=context)
            
        return {}
    
    # 03/03/2016 (felix) Get value of "turn_id" field
    def _get_turn_id(self, cr, uid, context=None):
        prod = False
        if context and context.get('active_id'):
            prod = self.pool.get('mrp.production').browse(cr, uid, 
                        context['active_id'], context=context)
        return prod.turn_id.id or False
        
    # 03/03/2016 (felix) Get value of "machine_id" field
    def _get_machine_id(self, cr, uid, context=None):
        prod = False
        if context and context.get('active_id'):
            prod = self.pool.get('mrp.production').browse(cr, uid, 
                        context['active_id'], context=context)
        return prod.machine_id.id or False
        
    _defaults = {
        'main_turn_id': _get_turn_id,
        'machine_id': _get_machine_id
    }

mrp_product_produce_mer()
