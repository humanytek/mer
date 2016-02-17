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


class mrp_workcenter_users_mer(osv.osv):

    _name = 'mrp.workcenter.users'
    _description = 'Add methos and fields mrp_workcenter_users'
    _columns = {
        'employee_id': fields.many2one('hr.employee', 'users_id', 'Name'),
        'job_id': fields.many2one('hr.job', 'Job'),
        'parent_id': fields.many2one('hr.employee', 'Manager'),
        'workcenter_id': fields.many2one('mrp.workcenter', 'Work centers'),
    }
    
    # 02/10/2015 (felix) Add method to get and push job_id and parent_id in form
    def on_change_employee(self, cr, uid, ids, employee_id, context=None):
        res = {}
        obj_employee = self.pool.get('hr.employee')
        src_employee = obj_employee.search(cr, uid, [('id', '=', employee_id)])
        if src_employee:
            get_employee = obj_employee.browse(cr, uid, src_employee[0], context)
            res = {
                'job_id': get_employee['job_id'],
                'parent_id': get_employee['parent_id']
            }
        return {'value': res}

mrp_workcenter_users_mer()
