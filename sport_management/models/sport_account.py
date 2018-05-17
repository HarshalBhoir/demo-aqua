from odoo import api, fields, models
import logging
#Get the logger
_logger = logging.getLogger(__name__)

class SportAccount(models.Model):
    _name = 'sport.account'
    _description = 'Seance account for sport module'

    name = fields.Char(string='Name')
    date_create = fields.Datetime(string = 'Creation date', default=fields.Datetime.now)
    credit_ids = fields.One2many('sport.credit', 'account_id', string="account's credit list")
    card_ids = fields.One2many('sport.sport_card', 'account_id', string="account's cards list")
    credit_count = fields.Integer(compute="_compute_credit_count")
    card_count = fields.Integer(compute="_compute_card_count")
    active = fields.Boolean(default=True)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Account owner', required=False)
    

    def _add_credit(self):
        pass

    def remove_credit(self):
        for account in self:
            index = 0
            account.credit_ids.sorted(key=lambda c:c.date_valid)
            if account.credit_ids[index].status == "valid":
                account.credit_ids[index].number_actual = account.credit_ids[index].number_actual - 1
            else:
                index = index + 1


    @api.depends('credit_ids')
    def _compute_credit_count(self):
        for account in self:
            account.credit_count = 0
            for credit in account.credit_ids:
                if credit.status == "valid":
                    account.credit_count += credit.number_actual

    def _compute_card_count(self):
        for account in self:
            account.card_count = 0
            for card in account.card_ids:
                account.card_count += 1

    @api.depends('active')
    def toogle_active(self):
        for account in self:
            if account.active == True:
                account.active = False
            else:
                account.active = True
