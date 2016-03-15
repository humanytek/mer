# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2016 Humanytek.
#    (http://humanytek.com)
#    soporte@humanytek.com
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

from openerp import tools
from openerp.osv import fields, osv

class mrp_resume_report_operators(osv.osv):

    _name = 'mrp.resume.report.operators'
    _description = "Report Location of Employees"
    _columns = {
        'machine_id': fields.many2one('mrp.workcenter', 'Machine'),
        'production_date': fields.date('Production date'),
        'operator_id': fields.many2one('hr.employee', 'Operator'),
        'hours': fields.float('Hours'),
    }
    _rec_name = 'operator_id'
    
mrp_resume_report_operators()

