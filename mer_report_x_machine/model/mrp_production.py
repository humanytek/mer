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

class mrp_production_mer(osv.osv):

    _inherit = 'mrp.product.produce'
    _description = 'Production orders'
    
    # 01/03/2016 (felix) Method to get operator
    def _get_operator(self, cr, uid, ids, fields_name, args, context=None):
        res = {}
        for i in self.browse(cr, uid, ids, context):
            res[i.id] = ''
            for j in i.operators_ids:
                res[i.id] += j.operator_id.name+'\n'
        return res
        
    _columns = {
        'operator_list': fields.function(_get_operator, type='text', 
            string='Operator'),
    }

mrp_production_mer()
