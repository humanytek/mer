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

class stock_production_lot_mer(osv.osv_memory):

    _inherit = 'stock.production.lot'
    _description = 'Stock production lot'
    
    # 18/02/2016 (felix) Method to get the quality status
    def _get_status_review(self, cr, uid, ids, field_name, args, context=None):
        res = {}
        for i in self.browse(cr, uid, ids, context):
            res[i.id] = 0
            for q in i.quality_ids:
                if q.review == 'a':
                    res[i.id] = 1
                elif q.review == 'r':
                    res[i.id] = 2
                    return res
        return res
    
    _columns = {
        'quality_ids': fields.one2many('stock.production.lot.quality', 'lot_id', 
            'Quality'),
        'quality_status': fields.function(_get_status_review, type='integer', 
            string='Quality status'),
    }
    
    # 18/02/2016 (felix) Method to get the quality status
    def quality_status_light(self, cr, uid, ids, context=None):
        return True    

stock_production_lot_mer()
