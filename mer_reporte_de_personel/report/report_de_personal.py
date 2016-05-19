# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2013 BroadTech IT Solutions.
#    (http://wwww.broadtech-innovations.com)
#    contact@boradtech-innovations.com
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

class personal_report(osv.osv):
    _name = "personal.report"
    _description = "Reporte de Personal"
    _auto = False
    _rec_name = 'product_id'
    
    _columns = {
        'operator_id': fields.many2one('hr.employee', 'Operator', readonly=True),
        'date' : fields.datetime('Date', readonly=True),
        'turn_id': fields.many2one('resource.calendar', 'Turn', readonly=True),
        'product_id': fields.many2one('product.product', 'Product', readonly=True),
        'qty_p': fields.float('Primera', readonly=True),
        'qty_s': fields.float('Segunda', readonly=True),
        'weight_net': fields.float('Weight',readonly=True),
        'machine_id': fields.many2one('mrp.workcenter', 'Machine', readonly=True),
        }
    
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'personal_report')
        cr.execute("""
            create view personal_report as (
                SELECT
                    min(m.id) as id,
                    m.operator_id as operator_id,
                    m.turn_id as turn_id,
                    p.date as date,
                    p.product_id as product_id,
                    p.weight as weight_net,
                    case when sl.first_condition=true then p.product_uos_qty else 0 end as qty_p,
                    case when sl.second_condition=true then p.product_uos_qty else 0 end as qty_s,
                    q.machine_id as machine_id
                     
                FROM
                    mrp_product_produce_operators m
                    LEFT JOIN stock_move p
                        ON p.id = m.operators_id1
                    LEFT JOIN stock_location sl 
                        ON sl.id=p.location_dest_id
                    LEFT JOIN mrp_product_produce n
                        ON sl.id=n.location_dest_id
                    LEFT JOIN mrp_production q
                        ON q.id = p.production_id
                    
                WHERE
                    q.state = 'done'
                GROUP BY
                    m.operator_id,
                    m.turn_id,
                    p.date,
                    p.product_id,
                    p.weight,
                    qty_p,
                    qty_s,                    
                    q.machine_id
            )""")
     
       
personal_report()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: