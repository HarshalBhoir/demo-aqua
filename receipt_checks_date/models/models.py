# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

from odoo.exceptions import ValidationError

class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'
    
    # Add field in model to store the date receipt of checks
    receipt_date = fields.Date(string='Receipt date', readonly=False)
    
    # Check if the date entered is equal or superior to the record date
    @api.constrains('receipt_date')
    def check_date(self):
        if self.receipt_date < self.date:
            raise ValidationError(_('The date receipt of check must be equal or superior to : ' + self.date))
    
class PosOrder(models.Model):
    _inherit = 'pos.order'
    
    # Override the "statement_ids" field to make readonly at false
    statement_ids = fields.One2many('account.bank.statement.line', 'pos_statement_id', string='Payments', readonly=False)