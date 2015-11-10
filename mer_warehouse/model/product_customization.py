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


class product_customization_mer(osv.osv):

    _name = 'product.customization'
    _description = 'Add methods and fields product_customization'
    
    # 30/10/2015 (felix) Method to get image from product
    def _get_image(self, cr, uid, ids, field_name, args, context=None):
        res = {}
        for i in self.browse(cr, uid, ids, context):
            res[i.id] = None
            if i.product_id.image:
                res[i.id] = i.product_id.image
        return res
    
    _columns = {
        'filter_product_id': fields.many2one('product.custom.type', 
            'Filter product type'),
        'product_id': fields.many2one('product.template', 'Product'),
        'mark': fields.char('Mark', size=5000),
        'description': fields.char('Description', size=5000),
        'image': fields.function(_get_image, type='binary', string='Image'),
        'product_base_id': fields.many2one('product.template', 'Product base'),
        'product_base_2_id': fields.many2one('product.product', 'Product base'),
    }

product_customization_mer()
