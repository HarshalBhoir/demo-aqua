from odoo import api, fields, models
from odoo.exceptions import ValidationError
import logging


_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    credit_ids = fields.One2many('sport.credit', 'client_id')
    badge_ids = fields.One2many('sport.badge','client_id')
    sub_ids = fields.One2many('sport.subscription','client_id')
    is_coach = fields.Boolean(default=False)
    account_id = fields.Many2one('sport.account', string="Compte", compute='_compute_account_id')

    @api.depends('badge_ids')
    def _compute_account_id(self):
        for partner in self:
            for badge in partner.badge_ids:
                partner.account_id = badge.account_id