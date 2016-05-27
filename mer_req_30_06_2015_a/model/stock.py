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

from collections import OrderedDict
from openerp.osv import fields, osv, orm
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
from openerp.tools import float_compare, float_is_zero
from openerp.tools.translate import _
from openerp import tools, SUPERUSER_ID
from openerp.addons.product import _common

class mrp_production_mer(osv.osv):

    _inherit = 'stock.move'
    _description = 'Stock move'

    # 27/02/2016 (felix) Original method in order to get location_dest_id
    def action_consume(self, cr, uid, ids, product_qty, location_id=False, location_dest_id=False, restrict_lot_id=False, restrict_partner_id=False,
                       consumed_for=False, context=None):
        """ Consumed product with specific quantity from specific source location.
        @param product_qty: Consumed/produced product quantity (= in quantity of UoM of product)
        @param location_id: Source location
        @param restrict_lot_id: optionnal parameter that allows to restrict the choice of quants on this specific lot
        @param restrict_partner_id: optionnal parameter that allows to restrict the choice of quants to this specific partner
        @param consumed_for: optionnal parameter given to this function to make the link between raw material consumed and produced product, for a better traceability
        @return: New lines created if not everything was consumed for this line
        """
        if context is None:
            context = {}
        res = []
        production_obj = self.pool.get('mrp.production')

        if product_qty <= 0:
            raise osv.except_osv(_('Warning!'), _('Please provide proper quantity.'))
        #because of the action_confirm that can create extra moves in case of phantom bom, we need to make 2 loops
        ids2 = []
        for move in self.browse(cr, uid, ids, context=context):
            if move.state == 'draft':
                ids2.extend(self.action_confirm(cr, uid, [move.id], context=context))
            else:
                ids2.append(move.id)

        prod_orders = set()
        for move in self.browse(cr, uid, ids2, context=context):
            prod_orders.add(move.raw_material_production_id.id or move.production_id.id)
            move_qty = move.product_qty
            if move_qty <= 0:
                raise osv.except_osv(_('Error!'), _('Cannot consume a move with negative or zero quantity.'))
            quantity_rest = move_qty - product_qty
            # Compare with numbers of move uom as we want to avoid a split with 0 qty
            quantity_rest_uom = move.product_uom_qty - self.pool.get("product.uom")._compute_qty_obj(cr, uid, move.product_id.uom_id, product_qty, move.product_uom)
            if float_compare(quantity_rest_uom, 0, precision_rounding=move.product_uom.rounding) != 0:
                new_mov = self.split(cr, uid, move, quantity_rest, context=context)
                if move.production_id:
                    self.write(cr, uid, [new_mov], {'production_id': move.production_id.id}, context=context)
                res.append(new_mov)
            vals = {'restrict_lot_id': restrict_lot_id,
                    'restrict_partner_id': restrict_partner_id,
                    'consumed_for': consumed_for}
            if location_id:
                vals.update({'location_id': location_id})

            # 27/02/2016 (felix) Add location_dest_id field
            if location_dest_id:
                vals.update({'location_dest_id': location_dest_id})

            self.write(cr, uid, [move.id], vals, context=context)
        # Original moves will be the quantities consumed, so they need to be done
        self.action_done(cr, uid, ids2, context=context)
        if res:
            self.action_assign(cr, uid, res, context=context)
        if prod_orders:
            production_obj.signal_workflow(cr, uid, list(prod_orders), 'button_produce')
        return res


mrp_production_mer()
