from odoo import api, fields, models
import logging
#Get the logger
_logger = logging.getLogger(__name__)

class CreditState(models.Model):
    _name = 'sport.state'
    _description = 'New Description'

    account_id = fields.Many2one('sport.account')
    type_id = fields.Many2one('sport.type_course')
    credit_count = fields.Integer(string="nombre de credit", compute="_compute_credit_count")

    _sql_constraints = [
        ('unique_account_type', 'unique(account_id, type_id)', 'This type already have a state')
    ]

    def _compute_credit_count(self):
        for state in self:
            _logger.info("_compute_credit_count")
            credit_count = 0
            for credit in state.account_id.credit_ids:
                if credit.type_id == state.type_id:
                    credit_count = credit_count + credit.number_actual
            state.credit_count = credit_count
