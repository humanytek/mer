from openerp import models, fields, api
from openerp.osv import osv
from openerp.tools.translate import _


class ReverseLimit(models.Model):
    _inherit = 'stock.return.picking.line'

    max_qty = fields.Float(readonly=True)
    quantity = fields.Float()

    @api.onchange('quantity')
    def on_change_quantity(self):
        if self.quantity > self.max_qty:
            self.quantity = self.max_qty
            return {
                'warning': {
                    'title': "Cantidad invalida",
                    'message': "La cantidad no debe exceder el monto transferido"
                }
            }


class stock_return_picking(osv.osv_memory):
    _inherit = 'stock.return.picking'

    def default_get(self, cr, uid, fields, context=None):
        """
         To get default values for the object.
         @param self: The object pointer.
         @param cr: A database cursor
         @param uid: ID of the user currently logged in
         @param fields: List of fields for which we want default values
         @param context: A standard dictionary
         @return: A dictionary with default values for all field in ``fields``
        """
        result1 = []
        if context is None:
            context = {}
        if context and context.get('active_ids', False):
            if len(context.get('active_ids')) > 1:
                raise osv.except_osv(_('Warning!'), _("You may only return one picking at a time!"))
        res = super(stock_return_picking, self).default_get(cr, uid, fields, context=context)
        record_id = context and context.get('active_id', False) or False
        uom_obj = self.pool.get('product.uom')
        pick_obj = self.pool.get('stock.picking')
        pick = pick_obj.browse(cr, uid, record_id, context=context)
        quant_obj = self.pool.get("stock.quant")
        chained_move_exist = False
        if pick:
            if pick.state != 'done':
                raise osv.except_osv(_('Warning!'), _("You may only return pickings that are Done!"))

            for move in pick.move_lines:
                if move.move_dest_id:
                    chained_move_exist = True
                #Sum the quants in that location that can be returned (they should have been moved by the moves that were included in the returned picking)
                qty = 0
                quant_search = quant_obj.search(cr, uid, [('history_ids', 'in', move.id), ('qty', '>', 0.0), ('location_id', 'child_of', move.location_dest_id.id)], context=context)
                for quant in quant_obj.browse(cr, uid, quant_search, context=context):
                    if not quant.reservation_id or quant.reservation_id.origin_returned_move_id.id != move.id:
                        qty += quant.qty
                qty = uom_obj._compute_qty(cr, uid, move.product_id.uom_id.id, qty, move.product_uom.id)
                max_qty = qty  # Add max_qty
                result1.append({'product_id': move.product_id.id, 'quantity': qty, 'move_id': move.id, 'max_qty': max_qty})

            if len(result1) == 0:
                raise osv.except_osv(_('Warning!'), _("No products to return (only lines in Done state and not fully returned yet can be returned)!"))
            if 'product_return_moves' in fields:
                res.update({'product_return_moves': result1})
            if 'move_dest_exists' in fields:
                res.update({'move_dest_exists': chained_move_exist})
        return res
