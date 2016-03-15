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

class mrp_resume_report(osv.osv):

    _name = 'mrp.resume.report'
    _description = "Manufacturing Orders Resume"
    
    # 09/03/2016 (felix) Method to calc quantity of first
    def _calc_total_qty_1(self, cr, uid, ids, fields_name, args, context=None):
        res = {}
        total = 0.00
        for i in self.browse(cr, uid, ids, context):
            if i.qty_1:
                total += i.qty_1
            res[i.id] = total
        return res
    
    # 09/03/2016 (felix) Method to calc quantity of second
    def _calc_total_qty_2(self, cr, uid, ids, fields_name, args, context=None):
        res = {}
        total = 0.00
        for i in self.browse(cr, uid, ids, context):
            if i.qty_2:
                total += i.qty_2
            res[i.id] = total
        return res
    
    # 09/03/2016 (felix) Method to calc quantity of rejected
    def _calc_total_qty_3(self, cr, uid, ids, fields_name, args, context=None):
        res = {}
        total = 0.00
        for i in self.browse(cr, uid, ids, context):
            if i.qty_3:
                total += i.qty_3
            res[i.id] = total
        return res
    
    # 10/03/2016 (felix) Method to calc weight of first
    def _calc_weight_1(self, cr, uid, ids, fields_name, args, context=None):
        res = {}
        for i in self.browse(cr, uid, ids, context):
            res[i.id] = 0.00
            res[i.id] = i.total_qty_1 * i.weight
        return res
        
    # 10/03/2016 (felix) Method to calc weight of second
    def _calc_weight_2(self, cr, uid, ids, fields_name, args, context=None):
        res = {}
        
        return res
        
    # 10/03/2016 (felix) Method to calc weight of rejected
    def _calc_weight_3(self, cr, uid, ids, fields_name, args, context=None):
        res = {}
        for i in self.browse(cr, uid, ids, context):
            res[i.id] = 0.00
            res[i.id] = i.total_qty_3 * i.weight
        return res
        
    # 09/03/2016 (felix) Method to calc rejected in percent
    def _calc_rejected_pow(self, cr, uid, ids, fields_name, args, context=None):
        res = {}
        for i in self.browse(cr, uid, ids, context):
            res[i.id] = i.total_qty_3 / (i.total_qty_3 + i.total_qty_1)
        return res
    
    _columns = {
        'product_id': fields.many2one('product.product', 'Product'),
        'machine_id': fields.many2one('mrp.workcenter', 'Machine'),
        'qty_1': fields.float('Quantity First'),
        'qty_2': fields.float('Quantity Second'),
        'qty_3': fields.float('Quantity Rejected'),
        'total_qty_1': fields.function(_calc_total_qty_1, type='float', 
            string='First Quantity', digits=(10,2)),
        'total_qty_2': fields.function(_calc_total_qty_2, type='float', 
            string='Second Quantity', digits=(10,2)),
        'total_qty_3': fields.function(_calc_total_qty_3, type='float', 
            string='Quantity Rejected', digits=(10,2)),
        'weight_1': fields.function(_calc_weight_1, type='float', 
            string='First Weight', digits=(10,2)),
        'weight_2': fields.function(_calc_weight_2, type='float', 
            string='Second Weight', digits=(10,2)),
        'weight_3': fields.function(_calc_weight_3, type='float', 
            string='Weight Rejected', digits=(10,2)),
        'weight': fields.float('Weight', digits=(10,2)),
        'mrp_id': fields.many2one('mrp.production', 'Production'),
        'rejected_pow': fields.function(_calc_rejected_pow, type='float',
            string='Rejected pow', digits=(10,2)),
        'production_date': fields.date('Production date'),
    }
    _rec_name = 'mrp_id'
    
mrp_resume_report()



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
