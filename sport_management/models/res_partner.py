from odoo import api, fields, models
import logging


_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    credit_ids = fields.One2many('sport.credit', 'client_id')
    card_ids = fields.One2many('sport.sport_card','client_id')
    sub_ids = fields.One2many('sport.subscription','client_id')
    credit_count = fields.Integer(compute="_compute_credit_count")
    card_count = fields.Integer(compute="_compute_card_cout")

    @api.depends('card_ids')
    def _compute_credit_count(self):
        _logger.info('COMPUTE CREDIT COUNT PARTNER')
        for partner in self:
            partner.credit_count = 0
            for card in partner.card_ids:
                _logger.info(card.credit_count)
                partner.credit_count += card.credit_count

    
    @api.depends('card_ids')
    def _compute_card_count(self):
        for partner in self:
            partner.card_count = 0
            for card in partner.card_ids:
                partner.card_count += 1

