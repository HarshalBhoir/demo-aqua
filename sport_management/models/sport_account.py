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
    badge_ids = fields.One2many('sport.badge', 'account_id', string="account's badges list")
    credit_count = fields.Integer(compute="_compute_credit_count")
    badge_count = fields.Integer(compute="_compute_badge_count")
    active = fields.Boolean(default=True)
    owner_id = fields.Many2one('res.partner', string="Owner")
    member_ids = fields.One2many('res.partner', 'account_id')
    
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

    def _compute_badge_count(self):
        for account in self:
            account.badge_count = 0
            for badge in account.badge_ids:
                account.badge_count += 1

    @api.depends('active')
    def toogle_active(self):
        for account in self:
            if account.active == True:
                account.active = False
            else:
                account.active = True
