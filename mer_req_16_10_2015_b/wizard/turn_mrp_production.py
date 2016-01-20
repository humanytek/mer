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
import time

from openerp.osv import fields, osv
from openerp.tools.translate import _

import logging
_logger = logging.getLogger(__name__)

class turn_mrp_production_mer(osv.osv_memory):

    _name = 'turn.mrp.production'
    _description = 'Assign a specific turn'
    _columns = {
        'turn_id': fields.many2one('resource.calendar', 'Turns'),
    }

    # 05/10/2015 (felix) Method to assign a specific turn 
    # to different manufacturing orders at the same time
    def assign_turn(self, cr, uid, ids, context=None):
        value = {}
        obj_mrp_production = self.pool.get('mrp.production')
        for i in self.browse(cr, uid, ids, context):
            if i.turn_id.id:
                value = {'turn_id': i.turn_id.id}
        if context['active_ids']:            
            obj_mrp_production.write(cr, uid, context['active_ids'], value, context)
        return True

turn_mrp_production_mer()
