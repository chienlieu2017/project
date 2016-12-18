# -*- coding: utf-8 -*-
##############################################################################
#
#    LEMME GROUP
#
##############################################################################

from openerp import api, fields, models
import openerp.addons.decimal_precision as dp


class ResCompany(models.Model):
    _inherit = 'res.company'

    lc_point_exchange_rate = fields.Float(
        string='Point Exchange Rate',
        digits=dp.get_precision('Discount'),)
