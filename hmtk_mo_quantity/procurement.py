# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2013 BroadTech IT Solutions.
#    (http://wwww.broadtech-innovations.com)
#    contact@broadtech-innovations.com
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
from openerp import SUPERUSER_ID

class procurement_order(osv.osv):
    _inherit = 'procurement.order'
    
    def _prepare_mo_vals(self, cr, uid, procurement, context=None):
        res = super(procurement_order, self)._prepare_mo_vals(cr, uid, procurement, context=context)
        quantity = 0.00
        if procurement.product_id.qty_available - procurement.product_id.outgoing_qty - procurement.product_qty>=0:
            return {}
        elif procurement.product_id.qty_available - procurement.product_id.outgoing_qty<0:
            quantity = procurement.product_qty
        else:
            quantity = procurement.product_qty - (procurement.product_id.qty_available - procurement.product_id.outgoing_qty)
        res.update({'product_qty': quantity})
        return res
    
    def make_mo(self, cr, uid, ids, context=None):
        """ Make Manufacturing(production) order from procurement
        @return: New created Production Orders procurement wise
        """
        res = {}
        production_obj = self.pool.get('mrp.production')
        procurement_obj = self.pool.get('procurement.order')
        for procurement in procurement_obj.browse(cr, uid, ids, context=context):
            if self.check_bom_exists(cr, uid, [procurement.id], context=context):
                #create the MO as SUPERUSER because the current user may not have the rights to do it (mto product launched by a sale for example)
                vals = self._prepare_mo_vals(cr, uid, procurement, context=context)
                if vals:
                    produce_id = production_obj.create(cr, SUPERUSER_ID, vals, context=dict(context, force_company=procurement.company_id.id))
                    res[procurement.id] = produce_id
                    self.write(cr, uid, [procurement.id], {'production_id': produce_id})
                    self.production_order_create_note(cr, uid, procurement, context=context)
                    production_obj.action_compute(cr, uid, [produce_id], properties=[x.id for x in procurement.property_ids])
                    production_obj.signal_workflow(cr, uid, [produce_id], 'button_confirm')
                else:
                    res[procurement.id] = False
            else:
                res[procurement.id] = False
                self.message_post(cr, uid, [procurement.id], body=_("No BoM exists for this product!"), context=context)
        return res
    
procurement_order()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: