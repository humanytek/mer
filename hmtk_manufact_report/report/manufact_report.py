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

class manufact_report(osv.osv):
    _name = "manufact.report"
    _description = "Manufacturing Orders Statistics"
    _auto = False
    _rec_name = 'product_id'

    _columns = {
        'date' : fields.datetime('Date', readonly=True),
        'machine_id': fields.many2one('mrp.workcenter', 'Machine', readonly=True),
        'product_id': fields.many2one('product.product', 'Product', readonly=True),
        'turn_id': fields.many2one('resource.calendar', 'Turns', readonly=True),
#         'quantification_ids': fields.one2many('mrp.workcenter.quantification', 
#             'workcenter_id', 'Quantification'),
#         'quantification' :fields.many2one('mrp.workcenter.quantification','Quantification', readonly=True),
#         'packaging_ids': fields.one2many(
#             'product.packaging', 'product_tmpl_id', 'Logistical Units'),
#         'packaging' : fields.many2one('product.packaging','Logistical Units', readonly=True),
        'weight_net': fields.float('Net Weight',readonly=True)
        
        }
    
    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""
            create or replace view manufact_report as (
                SELECT
                    min(m.id) as id,
                    m.date_planned as date,
                    m.machine_id as machine_id,
                    m.product_id as product_id,
                    m.turn_id as turn_id,
                    p.weight_net as weight_net
                FROM
                    mrp_production m
                    LEFT JOIN product_template p
                        on p.id = m.product_id
                GROUP BY
                    m.turn_id,
                    m.product_id,
                    m.machine_id,
                    m.date_planned,
                    p.weight_net
                    
            )""")

manufact_report()



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: