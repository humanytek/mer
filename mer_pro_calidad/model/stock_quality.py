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

class stock_quality_mer(osv.osv_memory):

    _name = "stock.quality"
    _description = "Process of quality"
    _columns = {
        'name': fields.char('Name', size=2048),
        'description': fields.char('Description', size=10000),
        'status': fields.selection([('a', 'Approvated'), ('r', 'Rejected')], 'Status'),
        'lot_id': fields.many2one('stock.production.lot', 'Lot')
    }

stock_quality_mer()
