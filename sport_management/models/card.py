from odoo import api, fields, models
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)

class SportCard(models.Model):
    _name = 'sport.sport_card'
    _description = 'Sport card'

    name = fields.Char(string='Name')
    barcode = fields.Char(string='Barcode', copy=False, oldname='ean13')
    validity = fields.Datetime()
    account_id = fields.Many2one('sport.account')
    client_id = fields.Many2one('res.partner')
    credit_count = fields.Integer(compute="_compute_credit_count")


    @api.depends('account_id')
    @api.onchange('account_id')
    def _compute_credit_count(self):
        for card in self:
            card.credit_count = card.account_id.credit_count

    def _scan_card(self):
        pass

    def scan_card(self):
        message = ""
        for card in self:
            client = card.client_id
            now = datetime.now()
            hour = now + timedelta(hours=24)
            lst_subscriptions = client.sub_ids

            for sub in lst_subscriptions:
                date = datetime.strptime(sub.session_id.start_date, '%Y-%m-%d %H:%M:%S')

                _logger.info(date <= hour)
                if date >= now and date <= hour:
                    if sub.state == "valid":
                        message = "presence déjà valider"
                    else :
                        if card.credit_count > 0:
                            card.account_id.remove_credit()
                            message = "presence valider"
                            sub.state = "valid"
                        else:
                            message = "plus de session"
                else:
                    message = "aucune session proche"
            return message
                
                