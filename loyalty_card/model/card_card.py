# -*- coding: utf-8 -*-
##############################################################################
#
#    LEMME GROUP
#
##############################################################################

from datetime import datetime, timedelta
from openerp import api, fields, models
import openerp.addons.decimal_precision as dp


class CardCard(models.Model):
    _name = 'card.card'
    _description = 'Loyalty Card'
    _order = 'name'

    name = fields.Char(
        string='Card Number',
        default='/')
    type_id = fields.Many2one(
        string='Type',
        comodel_name='card.type',
        required=1)
    partner_id = fields.Many2one(
        string='Customer',
        comodel_name='res.partner')
    creation_date = fields.Date(
        string='Creation Date',
        default=fields.Date.today())
    activate_date = fields.Date(
        string='Activated Date')
    expiry_date = fields.Date(
        string='Expiry Date')
    point_in_period = fields.Float(
        string='Points in Period',
        digits=dp.get_precision('Discount'))
    total_point = fields.Float(
        string='Total Points',
        digits=dp.get_precision('Discount'))
    history_ids = fields.One2many(
        string='History',
        comodel_name='card.history',
        inverse_name='card_id')

    @api.model
    def create(self, vals):
        if vals.get('name', '') in ('', '/'):
            vals.update({'name': self._get_card_nb()})
        return super(CardCard, self).create(vals)

    @api.model
    def _get_card_nb(self):
        sequence = self.env['ir.sequence'].get('sequence_seq_card_nb')
        return sequence
