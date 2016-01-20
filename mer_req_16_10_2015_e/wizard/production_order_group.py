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
import numpy

from openerp.osv import fields, osv
from openerp.tools.translate import _

import logging
_logger = logging.getLogger(__name__)

class production_order_group_mer(osv.osv_memory):

    _name = "production.order.group"
    _description = "Production Order Merge"

    # 12/10/2015 (felix) Check if there are two or more manufacturing orders selected
    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        if context is None:
            context={}
        res = super(production_order_group_mer, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar,submenu=False)
        if context.get('active_model','') == 'mrp.production' and len(context['active_ids']) < 2:
            raise osv.except_osv(_('Warning!'), _('Please select two or more orders to merge in the list view.'))
        return res
        
    # 12/10/2015 (felix) Merge the manufacturing orders
    def merge_orders(self, cr, uid, ids, context=None):
        if context is None:
            context = {}        
        # 12/10/2015 (felix) Checking if: 
        # the products are equals
        # bill of materials are equals
        # turns are equals
        # machines are equals
        # Raw Materials Location and Finished Products Location are equals
        obj_mrp_production = self.pool.get('mrp.production')
        if 'active_ids' in context:
            array_all_mrp = []
            for item in context['active_ids']:
                state = obj_mrp_production.browse(cr, uid, item, context)['state']
                if state <> 'draft':
                    raise osv.except_osv(_('Warning!'), _('Please the manufacturing orders must be in state New.'))
                product_id = obj_mrp_production.browse(cr, uid, item, context)['product_id'].id
                bom_id = obj_mrp_production.browse(cr, uid, item, context)['bom_id'].id
                turn_id = obj_mrp_production.browse(cr, uid, item, context)['turn_id'].id
                machine_id = obj_mrp_production.browse(cr, uid, item, context)['machine_id'].id
                location_src_id = obj_mrp_production.browse(cr, uid, item, context)['location_src_id'].id
                location_dest_id = obj_mrp_production.browse(cr, uid, item, context)['location_dest_id'].id
                array_dat = [product_id, bom_id, turn_id, machine_id, location_src_id, location_dest_id]
                array_all_mrp.append(array_dat)
                
            # Compare fields of one array with each other
            for a in array_all_mrp:
                comp = a
                for n in array_all_mrp:
                    if not numpy.array_equal(comp,n):
                        raise osv.except_osv(_('Warning!'), _('Some fields are not passing the rule to merge orders.'))
            
            # Fill the main fields of the new record
            origin = ''
            product_qty = 0
            for item in context['active_ids']:
                if obj_mrp_production.browse(cr, uid, item, context)['origin']:
                    origin += str(obj_mrp_production.browse(cr, uid, item, context)['origin'])+'; '
                product_qty += obj_mrp_production.browse(cr, uid, item, context)['product_qty']
                dic_mrp = {
                    'state': 'draft',
                    'product_id': obj_mrp_production.browse(cr, uid, item, context)['product_id'].id,
                    'product_qty': product_qty,
                    'product_uom': obj_mrp_production.browse(cr, uid, item, context)['product_uom'].id,
                    'routing_id': obj_mrp_production.browse(cr, uid, item, context)['routing_id'].id,
                    'user_id': obj_mrp_production.browse(cr, uid, item, context)['user_id'].id,
                    'bom_id': obj_mrp_production.browse(cr, uid, item, context)['bom_id'].id,
                    'turn_id': obj_mrp_production.browse(cr, uid, item, context)['turn_id'].id,
                    'machine_id': obj_mrp_production.browse(cr, uid, item, context)['machine_id'].id,
                    'location_src_id': obj_mrp_production.browse(cr, uid, item, context)['location_src_id'].id,
                    'location_dest_id': obj_mrp_production.browse(cr, uid, item, context)['location_dest_id'].id,
                    'company_id': obj_mrp_production.browse(cr, uid, item, context)['company_id'].id,
                    'priority': '1',
                    'allow_reorder': obj_mrp_production.browse(cr, uid, item, context)['allow_reorder'],
                    'sale_ref': obj_mrp_production.browse(cr, uid, item, context)['sale_ref'],
                    'sale_name': obj_mrp_production.browse(cr, uid, item, context)['sale_name'],
                    'move_prod_id': obj_mrp_production.browse(cr, uid, item, context)['move_prod_id'].id,
                    'origin': origin
                }
                obj_mrp_production.write(cr, uid, item, {'state':'cancel'}, context)
                
            # Create new mrp
            obj_mrp_production = self.pool.get('mrp.production')
            new_mrp = obj_mrp_production.create(cr, uid, dic_mrp, context)
                
            # Find and fill values to move_line
            obj_stock_move = self.pool.get('stock.move')
            obj_bom_line = self.pool.get('mrp.bom.line')
            obj_production_prod_line = self.pool.get('mrp.production.product.line')
            src_bom_line = obj_bom_line.search(cr, uid, [('bom_id', '=', dic_mrp['bom_id'])])
            array_mrp_lines = []
            array_schedule_prod = []
            
            for m in obj_bom_line.browse(cr, uid, src_bom_line, context):
                dic_mrp_line = {
                    'origin': dic_mrp['origin'],
                    'product_uom': dic_mrp['product_uom'],
                    'price_unit': m.product_id.lst_price,
                    'product_uom_qty': dic_mrp['product_qty'] * m.product_qty,
                    'company_id': dic_mrp['company_id'],
                    'location_id': dic_mrp['location_src_id'],
                    'priority': dic_mrp['priority'],
                    'state': 'draft',
                    'name': dic_mrp['origin'],
                    'partially_available': False,
                    'propagate': True,
                    'procure_method': 'make_to_stock',
                    'product_id': m.product_id.id,
                    'location_dest_id': dic_mrp['location_dest_id'],
                    'invoice_state': 'none',
                    'raw_material_production_id': new_mrp,
                }
                array_mrp_lines.append(dic_mrp_line)
                obj_stock_move.write(cr, uid, m.id, {'state':'cancel'}, context)
                
                # Read and get values to put them into mrp_production_product_line
                values_mrp_production_product_line = {
                    'production_id': new_mrp,
                    'product_id': m.product_id.id,
                    'product_qty': dic_mrp_line['product_uom_qty'],
                    'product_uos_qty': dic_mrp_line['product_uom_qty'],
                    'product_uom': dic_mrp['product_uom'],
                    'name': m.product_id.name,
                }
                array_schedule_prod.append(values_mrp_production_product_line)
                
            # Load move_line
            #for a in array_mrp_lines:
            #    obj_stock_move.create(cr, uid, a, context)
            # Load mrp_production_product_line
            for p in array_schedule_prod:
                obj_production_prod_line.create(cr, uid, p, context)
                
            # Create record in Products to Produce
            dic_p2p = {
                'origin': dic_mrp['origin'],
                'product_uom': dic_mrp['product_uom'],
                'product_uom_qty': dic_mrp['product_qty'],
                'company_id': dic_mrp['company_id'],
                'location_id': dic_mrp['location_src_id'],
                'priority': dic_mrp['priority'],
                'state': 'draft',
                'name': dic_mrp['origin'],
                'partially_available': False,
                'propagate': True,
                'procure_method': 'make_to_stock',
                'product_id': dic_mrp['product_id'],
                'location_dest_id': dic_mrp['location_dest_id'],
                'invoice_state': 'none',
                'production_id': new_mrp,
            }
            #obj_stock_move.create(cr, uid, dic_p2p, context)
            
        # Get number ID from search_view_id
        obj_mod = self.pool.get('ir.model.data')
        result = obj_mod._get_id(cr, uid, 'mrp', 'view_mrp_production_filter')
        id = obj_mod.read(cr, uid, result, ['res_id'])        
            
        return {
            'name': _('Manufacturing Orders'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'mrp.production',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'search_view_id': id['res_id']
        }

production_order_group_mer()
