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
import openerp.addons.decimal_precision as dp

class mrp_product_produce_mer(osv.osv):

    _inherit = 'mrp.product.produce'
    _description = 'Product Produce'
    _columns = {
        'user_ids': fields.many2many('hr.employee', 'workcenter_employee_rel', 'workcenter_id', 'employee_id', 'Users'),
    }

    def default_get(self, cr, uid, fields, context=None):
        res = super(mrp_product_produce_mer, self).default_get(cr, uid, fields, context=context)
        data = self.pool.get('mrp.production').browse(cr, uid, context['active_ids'], context)
        user_list = []
        for user_id in data.machine_id.workcenter_ids:
            if user_id and user_id.id:
                user_list.append(user_id.employee_id.id)
        tomerge = list(set(user_list))
        if 'user_ids' in fields:
            res.update({'user_ids': [(6, 0, tomerge)]})
        return res

mrp_product_produce_mer()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
