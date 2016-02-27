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

class stock_production_lot_quality_mer(osv.osv):

    _name = 'stock.production.lot.quality'
    _description = 'Stock production lot with process of quality'    
    _columns = {
        'quality_id': fields.many2one('stock.quality', 'Process of quality'),
        'description': fields.text('Description'),
        'review': fields.selection([('a', 'Approvated'), ('r', 'Rejected')], 'Status'),
        'lot_id': fields.many2one('stock.production.lot', 'Serial number'),
    }
    _rec_name = 'quality_id'
    
    # 18/02/2016 (felix) Method to get and fill description of process of quality
    def on_change_quality(self, cr, uid, ids, quality_id, context=None):
        res = {}
        obj_stock_quality = self.pool.get('stock.quality')
        if quality_id:
            get_quality = obj_stock_quality.search(cr, uid, [('id', '=', quality_id)])
            for i in obj_stock_quality.browse(cr, uid, get_quality, context):
                res = {
                    'description': i.description
                }
        return {'value':res}

stock_production_lot_quality_mer()

