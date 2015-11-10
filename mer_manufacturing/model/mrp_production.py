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

from datetime import date, datetime
from dateutil import relativedelta
import json
import time

from openerp.osv import fields, osv
from openerp.tools.float_utils import float_compare, float_round
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from openerp.exceptions import Warning
from openerp import SUPERUSER_ID, api
import openerp.addons.decimal_precision as dp
from openerp.addons.procurement import procurement
import logging
_logger = logging.getLogger(__name__)


class mrp_production_mer(osv.osv):

    _inherit = 'mrp.production'
    _description = 'Add methos and fields mrp_production'
    _columns = {
        'machine_id': fields.many2one('mrp.workcenter', 'Machine'),
        'move_lines': fields.one2many('stock.move', 'raw_material_production_id',
            'Products to Consume', domain=[('state', 'not in', ('done', 'cancel'))]),
        'turn_id': fields.many2one('resource.calendar', 'Turns'),
        'bom_id': fields.many2one('mrp.bom', 'Bill of Material',
            help="Bill of Materials allow you to define the list of required raw materials to make a finished product."),
    }
    
    # 09/10/2015 (felix) Method to check and get a new bill of materials
    def write(self, cr, uid, ids, values, context=None):
        
        # 12/10/2015 (felix) Check move lines and change if there were changes
        if 'move_lines' in values:
            obj_production_prod_line = self.pool.get('mrp.production.product.line')
            mrp_id = context['params']['id']
            array_ids_production = []
            
            # Get current products from move_lines
            for p in self.browse(cr, uid, ids, context):
                for l in p.move_lines:
                    src_production_prod_line = obj_production_prod_line.search(cr, uid, [('product_id', '=', l.product_id.id), ('production_id', '=', mrp_id)])
                    if src_production_prod_line:
                        id_production_prod_line = obj_production_prod_line.browse(cr, uid, src_production_prod_line[0], context)['id']
                        array_ids_production.append(id_production_prod_line)
            
            # Get new products in a dic
            c = 0
            for m in values['move_lines']:
                if m[2] <> False:
                    if 'product_uos_qty' in m[2]:
                        qty = {'product_qty': m[2]['product_uos_qty']}
                        obj_production_prod_line.write(cr, uid, array_ids_production[c], qty, context)
                    obj_production_prod_line.write(cr, uid, array_ids_production[c], m[2], context)
                    c += 1
        
        # 09/10/2015 (felix) Check bill of materials
        if 'bom_id' in values:
            production_id = self.browse(cr, uid, ids[0], context)['id']
            old_bom_id = self.browse(cr, uid, ids[0], context)['bom_id']
            location_src_id = self.browse(cr, uid, ids[0], context)['location_src_id']
            location_dest_id = self.browse(cr, uid, ids[0], context)['location_dest_id']
            product_qty = self.browse(cr, uid, ids[0], context)['product_qty']
            origin = self.browse(cr, uid, ids[0], context)['name']
            
            # Compare kind of state to stock_move from mrp_production
            state = self.browse(cr, uid, ids[0], context)['state']
            if state == 'draft':
                state = 'draft'
            elif state == 'cancel':
                state = 'cancel'
            elif state == 'confirmed':
                state = 'waiting'
            elif state == 'ready':
                state = 'confirmed'
            elif state == 'in_production':
                state = 'assigned'
            elif state == 'done':
                state = 'done'
            
            new_bom_id = values['bom_id']
            if old_bom_id.id <> new_bom_id:
                # Objects
                obj_stock_move = self.pool.get('stock.move')
                obj_bom = self.pool.get('mrp.bom')
                obj_bom_line = self.pool.get('mrp.bom.line')
                obj_production_prod_line = self.pool.get('mrp.production.product.line')
                
                # Values to get them from mrp_bom according to new_bom_id selected
                src_list_bom = obj_bom_line.search(cr, uid, [('bom_id', '=', new_bom_id)])
                if src_list_bom:
                    array_list_bom = []
                    array_schedule_prod = []
                    
                    for l in obj_bom_line.browse(cr, uid, src_list_bom, context):
                        
                        # Calculate quantity for each product
                        finally_product_qty = l.product_qty * product_qty
                        
                        # Read and get values to put them into stock_move
                        values_stock_move = {
                            'raw_material_production_id': production_id,
                            'product_id': l.product_id.id,
                            'product_uom_qty': finally_product_qty,
                            'product_uom': l.product_id.uom_id.id,
                            'price_unit': l.product_id.lst_price,
                            'invoice_state': 'none',
                            'location_id': location_src_id.id,
                            'location_dest_id': location_dest_id.id,
                            'procure_method': 'make_to_stock',
                            'propagate': True,
                            'partially_available': False,
                            'state': state,
                            'priority': '1',
                            'origin': origin,
                            'name': origin,
                        }
                        array_list_bom.append(values_stock_move)
                        
                        # Read and get values to put them into mrp_production_product_line
                        values_mrp_production_product_line = {
                            'production_id': production_id,
                            'product_id': l.product_id.id,
                            'product_qty': finally_product_qty,
                            'product_uos_qty': finally_product_qty,
                            'product_uom': l.product_id.uom_id.id,
                            'name': l.product_id.name,
                        }
                        array_schedule_prod.append(values_mrp_production_product_line)
                
                # Take old records and delete them
                """ In stock_move """
                src_list_stock_move = obj_stock_move.search(cr, uid, [('raw_material_production_id', '=', production_id)])
                if src_list_stock_move:
                    array_stock_move = []
                    for i in obj_stock_move.browse(cr, uid, src_list_stock_move, context):
                        array_stock_move.append(i.id)
                    obj_stock_move.write(cr, uid, array_stock_move, {'state':'draft'}, context)
                    obj_stock_move.unlink(cr, uid, array_stock_move, context)
                """ In mrp_production_product_line """
                src_production_prod_line = obj_production_prod_line.search(cr, uid, [('production_id', '=', production_id)])
                if src_production_prod_line:
                    array_production_prod_line = []
                    for i in obj_production_prod_line.browse(cr, uid, src_production_prod_line, context):
                        array_production_prod_line.append(i.id)
                    obj_production_prod_line.unlink(cr, uid, array_production_prod_line, context)
                    
                # Add new records
                """ In stock_move """
                for p in array_list_bom:
                    obj_stock_move.create(cr, uid, p)
                """ In mrp_production_product_line """
                for s in array_schedule_prod:
                    obj_production_prod_line.create(cr, uid, s)
        
        return super(mrp_production_mer, self).write(cr, uid, ids, values, context=context)
        
    # 19/10/2015 (felix) Method to check relation between machine, turn, and product
    def on_change_machine(self, cr, uid, ids, machine_id, product_id, context=None):
        res = {}
        obj_quantification = self.pool.get('mrp.workcenter.quantification')
        src_quantification = obj_quantification.search(cr, uid, [('workcenter_id', '=', machine_id), ('product_id', '=', product_id)])
        if src_quantification:
            turn_id = obj_quantification.browse(cr, uid, src_quantification[0], context)['turn_id']
            res = {'turn_id':turn_id.id}
        else:
            raise osv.except_osv(_('Warning!'), _('The product is not associated to this Machine.'))
        return {'value':res}
    
mrp_production_mer()
