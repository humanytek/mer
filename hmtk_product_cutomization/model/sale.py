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

class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'
    
    def _get_image(self, cr, uid, ids, field_name, args, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context):
            res[line.id] = None
            if line.product_id.image:
                res[line.id] = line.product_id.image
        return res
    
    _columns = {
        'insert_text': fields.char('Insert', size=500),
        'product_image': fields.function(_get_image, type='binary', string='Image'),
        'insert_id': fields.many2one('product.customization', 'Inserts'),
        'prod_is_customizable': fields.boolean('Is customizable')
    }
    
    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
        res = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty=qty,
            uom=uom, qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
            lang=lang, update_tax=update_tax, date_order=date_order, packaging=packaging, fiscal_position=fiscal_position, flag=flag, context=context)
        
        if res != None:
            product_obj = self.pool.get('product.product')
            if product:
                prod = product_obj.browse(cr, uid, product, context=context)
                res['value'].update({'product_image': prod.image})
                if prod.is_customizable:
                    res['value'].update({'prod_is_customizable': True})
                else:
                    res['value'].update({'insert_text': '', 'prod_is_customizable': False})
        
        return res
    
#     def onchange_product_tmp_id(self, cr, uid, ids, product_tmp_id, context=None):
#         res = super(sale_order_line, self).onchange_product_tmp_id(cr, uid, ids, product_tmp_id, context=context)
#         if res != None:
#             product_obj = self.pool.get('product.product')
#             if res.get('value').get('product_id'):
#                 product_id = res.get('value').get('product_id')
#                 product = product_obj.browse(cr, uid, product_id, context=context)
#                 if product.is_customizable:
#                     res['value'].update({'prod_is_customizable': True})
#                 else:
#                     res['value'].update({'insert_text': '', 'prod_is_customizable': False})
#         return res
    
    def onchange_insert_id(self, cr, uid, ids, insert_id, context=None):
        product_obj = self.pool.get('product.customization')
        product_insert = product_obj.browse(cr, uid, insert_id, context=context)
        if product_insert.description:
            return {'value': {'insert_text': product_insert.description}}
        else:
            return {'value': {'insert_text': ''}}
    
sale_order_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: