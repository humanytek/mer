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

from datetime import date, datetime
from dateutil import relativedelta
import json
import time

from openerp.osv import fields, osv
from openerp.tools.float_utils import float_compare, float_round
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from openerp.exceptions import Warning
from openerp import SUPERUSER_ID, api
import openerp.addons.decimal_precision as dp
from openerp.addons.procurement import procurement
import logging
_logger = logging.getLogger(__name__)


class stock_picking_mer(osv.osv):

    _inherit = 'stock.picking'
    _description = 'Add method and fields stock_picking'
        
    # 24/09/2015 (felix) Method to get date_commitment from sale_order
    def _get_date_commitment(self, cr, uid, ids, field_name, args, context=None):
        res = {}
        obj_sale_order = self.pool.get('sale.order')
        for i in self.browse(cr, uid, ids, context):
            res[i.id] = ''
            if i.origin:
                get_sale_order = obj_sale_order.search(cr, uid, [('name', 'like', i.origin)])
                if get_sale_order:
                    res[i.id] = obj_sale_order.browse(cr, uid, get_sale_order[0], context)['date_commitment']
        return res
    
    _columns = {
        'date_commitment': fields.function(_get_date_commitment, type='date', 
            string='Date commitment'),
    }

stock_picking_mer()
