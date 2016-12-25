# -*- coding: utf-8 -*-
##############################################################################
#
#    LEMME GROUP > amemberofuit@gmail.com
#
##############################################################################

from datetime import datetime, timedelta
from openerp import api, fields, models
import openerp.addons.decimal_precision as dp
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from openerp.osv.fields import related


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
        string='Creation Date')
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
    is_expired = fields.Boolean(
        string='Expired?',
        compute='_is_expired')
    state_id = fields.Many2one(
        string='Status',
        comodel_name='card.stage')
    issue_hard_card = fields.Boolean(
        string='Is Issue Hard Card?',
        related='type_id.issue_hard_card',
        readonly=1)
    history_ids = fields.One2many(
        string='History',
        comodel_name='card.history',
        inverse_name='card_id')

    @api.multi
    def _is_expired(self):
        tday = fields.Date.today()
        for record in self:
            is_expired = False
            if not record.expiry_date:
                continue
            if tday > record.expiry_date:
                is_expired = True
            record.is_expired = is_expired

    @api.model
    def default_get(self, fields_list):
        res = super(CardCard, self).default_get(fields_list)
        res.update({'creation_date': fields.Date.context_today(self)})
        stage = self.env['card.stage'].search([], limit=1)
        if stage:
            res.update({'state_id': stage.id})
        return res

    @api.model
    def create(self, vals):
        if vals.get('name', '') in ('', '/'):
            vals.update({'name': self._get_card_nb()})
        return super(CardCard, self).create(vals)

    @api.model
    def _get_card_nb(self):
        sequence = self.env['ir.sequence'].get('sequence_seq_card_nb')
        return sequence
