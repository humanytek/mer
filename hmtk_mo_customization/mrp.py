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
import time
class mrp_production(osv.osv):
    _inherit = 'mrp.production'
    
    _columns = {
        'bom_id': fields.many2one('mrp.bom', 'Bill of Material', states={'done': [('readonly', True)]},
            help="Bill of Materials allow you to define the list of required raw materials to make a finished product."),
        'move_lines': fields.one2many('stock.move', 'raw_material_production_id', 'Products to Consume',
            domain=[('state', 'not in', ('done', 'cancel'))], states={'done': [('readonly', True)]}),
        'move_lines2': fields.one2many('stock.move', 'raw_material_production_id', 'Consumed Products',
            domain=[('state', 'in', ('done', 'cancel'))], states={'done': [('readonly', True)]}),
        'date' : fields.datetime('Date'),
        'product_lines': fields.one2many('mrp.production.product.line', 'production_id', 'Scheduled goods',),
                }
    
    def bom_id_change(self, cr, uid, ids, bom_id, location_src_id=False, product_id=False, state='draft', context=None):
        result = []
        result1 = []
        if state == 'draft':
            if not bom_id:
                return {'value': {
                    'routing_id': False,
                    'move_lines' : False,
                    'product_lines' : False
                }}
    #         if move_lines[0][2]:
    #             for move_id in move_lines[0][2]:
    #                 stock_rec = self.pool.get('stock.move').browse(cr, uid, move_id, context=context)
    #                 if stock_rec.state != 'draft' or stock_rec.state != 'cancel':
    #                     self.pool.get('stock.move').action_cancel(cr, uid, stock_rec.id, context=context)
            bom_point = self.pool.get('mrp.bom').browse(cr, uid, bom_id, context=context)
            move_ids = []
            routing_id = bom_point.routing_id.id or False
            res = {
                'routing_id': routing_id
            }
        
            product = self.pool.get('product.product').browse(cr, uid, product_id, context=context)
            
    #         for production in self.browse(cr, uid, ids, context=context):
    #             source_location_id = production.location_src_id.id
    #             if production.bom_id.routing_id and production.bom_id.routing_id.location_id and production.bom_id.routing_id.location_id.id != source_location_id:
    #                 source_location_id = production.bom_id.routing_id.location_id.id
    #             destination_location_id = production.product_id.property_stock_production.id
            source_location_id = location_src_id
            if bom_point.routing_id and bom_point.routing_id.location_id and bom_point.routing_id.location_id.id != location_src_id:
                source_location_id = bom_point.routing_id.location_id.id
            destination_location_id = product.property_stock_production.id
            for line in bom_point.bom_line_ids:
                vals = {
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_qty or 0.00,
                'name': line.product_id.name,
                'invoice_state' : 'none',
                'date_expected' : time.strftime("%Y-%m-%d %H:%M:%S"),
                'location_id' : source_location_id,
                'location_dest_id': destination_location_id,
    #             'raw_material_production_id' : production.id,
                'product_uom' : line.product_id.uom_id and line.product_id.uom_id.id or False,
                'state' : 'draft'
                }
                vals1 = {
                    'product_id' : line.product_id.id,
                    'name' : line.product_id.name,
                    'product_qty' : line.product_qty or 0.00,
                    'product_uom' : line.product_id.uom_id and line.product_id.uom_id.id or False,
                }
                result.append(vals)
                result1.append(vals1)
    #             move_id = self.pool.get('stock.move').create(cr, uid, vals, context=context)
    #             move_ids.append(move_id)
    #         res['move_lines']=  [(6, 0, move_ids)]
            res['move_lines'] = result
            res['product_lines'] = result1
            return {'value': res}
    
    def action_update(self, cr, uid, ids, context=None):
        for production in self.browse(cr, uid, ids, context=context):
            for stock_rec in production.move_lines:
                if stock_rec.state != 'draft' or stock_rec.state != 'cancel':
                    self.pool.get('stock.move').action_cancel(cr, uid, stock_rec.id, context=context)
                    self.pool.get('stock.move').unlink(cr, uid, stock_rec.id, context=context)
                else:
                    self.pool.get('stock.move').unlink(cr, uid, stock_rec.id, context=context)
            for stock_rec in production.move_lines2:
                if stock_rec.state != 'draft' or stock_rec.state != 'cancel':
                    self.pool.get('stock.move').action_cancel(cr, uid, stock_rec.id, context=context)
                    self.pool.get('stock.move').unlink(cr, uid, stock_rec.id, context=context)
                else:
                    self.pool.get('stock.move').unlink(cr, uid, stock_rec.id, context=context)
            for product in production.product_lines:
                self.pool.get('mrp.production.product.line').unlink(cr, uid, product.id, context=context)
            source_location_id = production.location_src_id.id
            if production.bom_id.routing_id and production.bom_id.routing_id.location_id and production.bom_id.routing_id.location_id.id != production.location_src_id:
                source_location_id = production.bom_id.routing_id.location_id.id
            destination_location_id = production.product_id.property_stock_production.id
            for line in production.bom_id.bom_line_ids:
                vals = {
                'product_id': line.product_id.id,
                'product_uom_qty': production.product_qty * line.product_qty or 0.00,
                'name': line.product_id.name,
                'invoice_state' : 'none',
                'date_expected' : time.strftime("%Y-%m-%d %H:%M:%S"),
                'location_id' : source_location_id,
                'location_dest_id': destination_location_id,
                'raw_material_production_id' : production.id,
                'product_uom' : line.product_id.uom_id and line.product_id.uom_id.id or False,
                'state' : 'draft'
                }
                vals1 = {
                    'product_id' : line.product_id.id,
                    'name' : line.product_id.name,
                    'product_qty' : production.product_qty * line.product_qty or 0.00,
                    'product_uom' : line.product_id.uom_id and line.product_id.uom_id.id or False,
                    'production_id' : production.id
                }
                move_id = self.pool.get('stock.move').create(cr, uid, vals, context=context)
                self.pool.get('stock.move').action_confirm(cr, uid, [move_id], context=context)
                self.pool.get('mrp.production.product.line').create(cr, uid, vals1, context=context)
                
        return True
    
    def action_confirm(self, cr, uid, ids, context=None):
        """ Confirms production order.
        @return: Newly generated Shipment Id.
        """
        user_lang = self.pool.get('res.users').browse(cr, uid, [uid]).partner_id.lang
        context = dict(context, lang=user_lang)
        stock_moves = []
        uncompute_ids = filter(lambda x: x, [not x.product_lines and x.id or False for x in self.browse(cr, uid, ids, context=context)])
        self.action_compute(cr, uid, uncompute_ids, context=context)
        for production in self.browse(cr, uid, ids, context=context):
            if production.move_lines:
                for move in production.move_lines:
                    stock_moves.append(move.id)
                if stock_moves:
                    self.pool.get('stock.move').action_confirm(cr, uid, stock_moves, context=context)
                production.write({'state': 'confirmed'})
            else:
                self._make_production_produce_line(cr, uid, production, context=context)
 
                stock_moves = []
                for line in production.product_lines:
                    if line.product_id.type != 'service':
                        stock_move_id = self._make_production_consume_line(cr, uid, line, context=context)
                        stock_moves.append(stock_move_id)
                    else:
                        self._make_service_procurement(cr, uid, line, context=context)
                if stock_moves:
                    self.pool.get('stock.move').action_confirm(cr, uid, stock_moves, context=context)
                production.write({'state': 'confirmed'})
        return 0
            
#     def write(self, cr, uid, ids, vals, context=None):
#         for production in self.browse(cr, uid, ids, context=context):
#             for stock_rec in production.move_lines:
#                 if stock_rec.state != 'draft' or stock_rec.state != 'cancel':
#                     self.pool.get('stock.move').action_cancel(cr, uid, stock_rec.id, context=context)
#                     self.pool.get('stock.move').unlink(cr, uid, stock_rec.id, context=context)
#                 else:
#                     self.pool.get('stock.move').unlink(cr, uid, stock_rec.id, context=context)
#             for stock_rec in production.move_lines2:
#                 if stock_rec.state != 'draft' or stock_rec.state != 'cancel':
#                     self.pool.get('stock.move').action_cancel(cr, uid, stock_rec.id, context=context)
#                     self.pool.get('stock.move').unlink(cr, uid, stock_rec.id, context=context)
#                 else:
#                     self.pool.get('stock.move').unlink(cr, uid, stock_rec.id, context=context)
#         res = super(mrp_production, self).write(cr, uid, ids, vals, context=context)
#         return res
    
mrp_production()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: