# -*- coding: utf-8 -*-
##############################################################################
#
#    LEMME GROUP > amemberofuit@gmail.com
#
##############################################################################

from openerp import api, fields, models
import openerp.addons.decimal_precision as dp


class sale_configuration(models.TransientModel):
    _inherit = 'sale.config.settings'

    lc_point_exchange_rate = fields.Float(
        string='Point Exchange Rate',
        digits=dp.get_precision('Discount'),)

    @api.multi
    def set_lc_point_exchange_rate(self):
        self.ensure_one()
        user = self.env['res.users'].browse(self.env.uid)
        user.company_id.lc_point_exchange_rate = self.lc_point_exchange_rate

    @api.model
    def get_default_lc_point_exchange_rate(self, fields):
        if 'lc_point_exchange_rate' not in fields:
            return {}
        user = self.env['res.users'].browse(self.env.uid)
        lc_point_exchange_rate = user.company_id.lc_point_exchange_rate or 0.0
        res = {'lc_point_exchange_rate': lc_point_exchange_rate}
        return res
