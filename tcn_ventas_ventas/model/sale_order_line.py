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

from openerp.osv import fields, osv
from openerp.tools.translate import _

import logging
_logger = logging.getLogger(__name__)

class sale_order_line_tcn(osv.Model):

    _inherit = 'sale.order.line'
    _description = 'Added fields and methods for Tucane'
    _columns = {
        'product_tmp_id': fields.many2one('product.template', 'Product', 
            domain=[('sale_ok', '=', True)], change_default=True, readonly=True, 
            states={'draft': [('readonly', False)]}, ondelete='restrict'),
       # Added new many2many field  @anoop 12/11/2015
        'attribute_value_ids': fields.many2many('product.attribute.value', string='Variants', help="BOM Product Variants needed form apply this line."),
        
    }
    
#     def onchange_attribute_value_ids(self, cr, uid, ids, attribute_value_ids, product_tmp_id, context=None):
#         if attribute_value_ids and product_tmp_id:
#             product_obj = self.pool.get('product.product')
#             product_ids = product_obj.search(cr, uid, [('product_tmpl_id', '=', product_tmp_id)], context=context)
#             if attribute_value_ids[0] and attribute_value_ids[0][2]:
#                 for prod in product_obj.browse(cr, uid, product_ids, context=context):
#                     variant_attr_ids = [attr.id for attr in prod.attribute_value_ids]
#                     attribute_ids = attribute_value_ids[0] and attribute_value_ids[0][2]
#                     flag = False
#                     for atr_id in attribute_ids:
#                         if not atr_id in variant_attr_ids:
#                             flag = False
#                             break
#                         else:
#                             flag = True
#                     if flag:
#                         return {'value': {'product_id': prod.id}}
#         return {'value': {'product_id': False}}
    
#     def onchange_product_tmp_id(self, cr, uid, ids, product_tmp_id, context=None):
#         if product_tmp_id:
#             product_obj = self.pool.get('product.product')
#             product_ids = product_obj.search(cr, uid, [('product_tmpl_id', '=', product_tmp_id)], context=context)
#             return {'value': {'product_id': product_ids and product_ids[0] or False, 'attribute_value_ids': [(6, 0, [])]}}
    
sale_order_line_tcn()
