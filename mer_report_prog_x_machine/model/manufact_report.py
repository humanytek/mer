# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2013 BroadTech IT Solutions.
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

class manufact_report(osv.osv):

    _inherit = 'manufact.report'
    _description = "Manufacturing Orders Statistics"
    _columns = {
        'qty': fields.float('Quantity', readonly=True)
    }
    
    # 07/03/2016 (felix) Method to change some fields
    # - date_planned changed to date
    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""
            create or replace view manufact_report as (
                SELECT
                    min(m.id) as id,
                    m.date as date,
                    m.machine_id as machine_id,
                    m.product_id as product_id,
                    m.turn_id as turn_id,
                    m.product_qty as qty,
                    p.weight_net as weight_net
                FROM
                    mrp_production m
                    LEFT JOIN product_template p
                        on p.id = m.product_id
                GROUP BY
                    m.turn_id,
                    m.product_id,
                    m.machine_id,
                    m.date,
                    m.product_qty,
                    p.weight_net
            )""")

manufact_report()



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
