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

class stock_production_lot_mer(osv.osv):

    # 03/03/2016 (felix) Changed from stock to production
    #_inherit = 'stock.production.lot'
    _inherit = 'mrp.product.produce'
    _description = 'Product produce'
    
    # 18/02/2016 (felix) Method to get the quality status
    # 03/03/2016 (felix) Does not used
    """
    def _get_status_review(self, cr, uid, ids, field_name, args, context=None):
        res = {}
        for i in self.browse(cr, uid, ids, context):
            res[i.id] = ''
            for q in i.quality_ids:
                if q.review == 'a':
                    res[i.id] = 'a'
                elif q.review == 'r':
                    res[i.id] = 'r'
                    return res
        return res
        
        # Field of the method
        'quality_status': fields.function(_get_status_review, type='selection',
            selection=[('a','Approvated'),('r','Rejected')],
            string='Quality status', store=True),
        
    """
    
    _columns = {
        'quality_ids': fields.one2many('mrp.product.produce.quality', 'product_produce_id', 
            'Quality'),
    }
    

stock_production_lot_mer()
