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

class stock_quality_mer(osv.osv):

    # 03/03/2016 (felix) Moved to mrp modules
    #_name = 'stock.quality'
    _name = 'mrp.quality'
    _description = 'Process of quality'
    _columns = {
        'name': fields.char('Name', size=2048, required=True),
        'description': fields.text('Description', size=10000),
        'quality_in_mrp_ids': fields.one2many('mrp.product.produce.quality', 
            'quality_id', 'Quality in serial number')
    }

stock_quality_mer()
