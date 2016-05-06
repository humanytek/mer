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

from openerp.osv import osv, fields, expression
from openerp.tools.translate import _

class product_template(osv.osv):
    _inherit = "product.template"
    
    def copy(self, cr, uid, id, default=None, context=None):
        res = super(product_template, self).copy(cr, uid, id, default=default, context=context)
        template = self.browse(cr, uid, id, context=context)
        for new_prod in self.browse(cr, uid, res, context=context):
            if new_prod.product_variant_ids:
                to_delete = []
                for prod_var in new_prod.product_variant_ids:
                    to_delete.append(prod_var.id)
        for attr_id in template.attribute_line_ids:
            attr_list = []
            for val in attr_id.value_ids:
                attr_list.append(val.id)
            self.pool.get('product.attribute.line').create(cr, uid, {
                                                                     'attribute_id': attr_id.attribute_id and attr_id.attribute_id.id,
                                                                     'value_ids': [(6, 0, attr_list)],
                                                                     'product_tmpl_id': res}, context=context)
        for variant in template.product_variant_ids:
            variant_list = []
            for item in variant.attribute_value_ids:
                variant_list.append(item.id)
            self.pool.get('product.product').create(cr, uid, {
                                                            'attribute_value_ids': [(6, 0, variant_list)],
                                                            'product_tmpl_id': res}, context=context)
            if variant:
                self.pool.get('product.product').unlink(cr, uid, to_delete, context=context)
        return res
    
    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
