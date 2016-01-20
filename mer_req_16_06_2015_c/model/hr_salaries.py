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


class hr_salaries_mer(osv.osv):

    _name = 'hr.salaries'
    _description = 'Create new object, methos, and fields in hr_salaries'
    _columns = {
        'name': fields.char('Name', size=2048),
        'description': fields.text('Description'),
        'amount': fields.float('Amount', digits=(10,2)),
        'frecuency_id': fields.many2one('product.uom', 'Frecuency'),
        'hr_salary_ids': fields.one2many('hr.employee', 'salaries_id', 
            'Salaries')
    }
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Name field must be unique')
    ]
    
    # 24/09/2015 (felix) Return name, amount, and frecuency as the name
    def name_get(self, cr, uid, ids, context=None):
        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name', 'amount', 'frecuency_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            amount = record['amount']
            if record['frecuency_id'] and amount:
                name = name+': $'+str(amount)+' / '+record['frecuency_id'][1]
            res.append((record['id'], name))
        return res
    
hr_salaries_mer()
