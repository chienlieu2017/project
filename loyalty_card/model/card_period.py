# -*- coding: utf-8 -*-
##############################################################################
#
#    LEMME GROUP > amemberofuit@gmail.com
#
##############################################################################

from datetime import datetime, timedelta
from openerp import api, fields, models

PERIOD = [('month', 'Month(s)'), ('year', 'Year(s)')]


class CardPeriod(models.Model):
    _name = 'card.period'
    _description = 'Loyalty Card Period'
    _order = 'period,nb'

    name = fields.Char(
        string='Period',
        compute='_get_period_name',
        store=1)
    nb = fields.Integer(
        string='Number of Months / Years',
        required=1)
    period = fields.Selection(
        PERIOD,
        string='Period',
        required=1)

    @api.multi
    @api.depends('nb', 'period')
    def _get_period_name(self):
        period = dict(PERIOD)
        for record in self:
            record.name = '{} {}'.format(record.nb, period.get(record.period))

    @api.multi
    def get_period_end_date(self, start_d=None):
        self.ensure_one()
        if not start_d:
            start_d = datetime.now()
        return None
