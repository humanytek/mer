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

class report_indicator(osv.osv):
    _name = "report.indicator"
    _description = "report indicators"
    
    def _pgr_value(self, cr, uid, ids, name, product_id, arg, context=None):
        result = {}
        for indicator in self.browse(cr, uid, ids, context=context):
            result[indicator.id]={
                    'pgr': 0.0,
                    'real': 0.0,
                    'percent': 0.0
                }
            if indicator.name=='1era':
                cr.execute("SELECT SUM(product_qty) FROM mrp_production WHERE product_id=%s and state='done' ", (indicator.product_id.id,))
                era_pgr = cr.dictfetchone()
                #era_pgr_value= 
                result[indicator.id]['pgr'] = era_pgr['sum']
                cr.execute("SELECT SUM(product_uom_qty) FROM stock_move WHERE product_id=%s and state='done' and location_dest_id=24", (indicator.product_id.id,))
                era_real = cr.dictfetchone()
                result[indicator.id]['real'] = era_real['sum']
                result[indicator.id]['percent'] = era_real['sum'] and era_real['sum']  / era_pgr['sum'] or 0 or 0
                
            elif indicator.name=='2da':
                result[indicator.id]['pgr'] = 0.0
                cr.execute("SELECT SUM(product_uom_qty) FROM stock_move WHERE product_id=%s and state='done and location_dest_id IN (26,25)' ", (indicator.product_id.id,))
                eda_real = cr.dictfetchone()
                result[indicator.id]['real'] = eda_real['sum']            
                result[indicator.id]['percent'] = 0.0
                
            elif indicator.name=='% de rechazo':
                cr.execute("SELECT SUM(product_uom_qty) FROM stock_move WHERE product_id=%s and state='done' and location_dest_id=24", (indicator.product_id.id,))
                era_real = cr.dictfetchone()
                cr.execute("SELECT SUM(product_uom_qty) FROM stock_move WHERE product_id=%s and state='done' and location_dest_id IN (26,25) ", (indicator.product_id.id,))
                eda_real = cr.dictfetchone()
                result[indicator.id]['pgr'] = 0.0
                real_total =(eda_real['sum'] or 0 )+ (era_real['sum'] or 0 )
                if real_total !=0: 
                    result[indicator.id]['real'] = eda_real['sum'] and eda_real['sum'] / real_total
                result[indicator.id]['percent'] = 0.0
            else:
                
                result[indicator.id]['percent'] = 0.0
                prod_list=[]
                production_ids = self.pool.get('product.product').search(cr, uid, [('id', '=', indicator.product_id.id)], context=context)
                for product in self.pool.get('product.product').browse(cr, uid, production_ids, context=context):
                    prod_list.append(product.weight_net)
                    result[indicator.id]['pgr'] = sum(prod_list)
                    
                cr.execute("SELECT SUM(weight) FROM stock_move WHERE product_id=%s and state='done' ", (indicator.product_id.id,))
                all_weight = cr.dictfetchone()
                cr.execute("SELECT SUM(product_uom_qty) FROM stock_move WHERE product_id=%s and state='done' ", (indicator.product_id.id,))
                all_quantity = cr.dictfetchone()
                if all_quantity['sum']:
                    result[indicator.id]['real'] = all_weight['sum'] / all_quantity['sum']
                    if result[indicator.id]['pgr']:
                        result[indicator.id]['percent'] = result[indicator.id]['real']  / result[indicator.id]['pgr']
        return result
    
        
    _columns = {
        'name': fields.selection([('1era', '1era (jgos)'), ('2da', '2da (jgos)'), ('% de rechazo', '% de rechazo (%)'), ('Peso', 'Peso (Kg)')], 'Indicators'),
        'pgr': fields.function(_pgr_value, string='PGR', type='float', multi=True, store=True),
        'real': fields.function(_pgr_value, string='REAL', type='float', multi=True, store=True),
        'percent': fields.function(_pgr_value, string='%', type='float', multi=True, store=True),
        'product_id': fields.many2one('product.product','Product')
        }
    
    
    
class product_product(osv.osv):
    _inherit = "product.product"
    _description = "product"
       
    _columns = {
        'indicator_ids': fields.one2many('report.indicator', 'product_id','Indicators'),
        }
    
class mrp_management_report(osv.osv):
    _name = "mrp.management.report"
    _description = "Reporte Gerencial"
    _auto = False
    _rec_name = 'product_id'
    
    _columns = {
        'turn_id': fields.many2one('resource.calendar', 'Turn', readonly=True),
        'product_id': fields.many2one('product.product', 'Product', readonly=True),
        'indicator': fields.selection([('1era', '1era (jgos)'), ('2da', '2da (jgos)'), ('% de rechazo', '% de rechazo (%)'), ('Peso', 'Peso (Kg)')], 'Indicator',readonly=True),
        'pgr': fields.float('PGR', readonly=True),
        'real': fields.float('REAL', readonly=True),
        'percent': fields.float('%', readonly=True),
                }
    
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'mrp_management_report')
        cr.execute("""
            create view mrp_management_report as (
                SELECT
                    min(m.id) as id,
                    m.product_id as product_id,
                    m.turn_id as turn_id,
                    p.name as indicator,
                    p.pgr as pgr,
                    p.real as real,
                    p.percent as percent
                     
                FROM
                    mrp_production m
                    LEFT JOIN report_indicator p
                        on p.product_id = m.product_id                      
                WHERE
                    m.state = 'done'
                GROUP BY
                    m.product_id,
                    m.turn_id,
                    p.name,
                    p.pgr,
                    p.real,
                    p.percent
            )""")


       
mrp_management_report()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: