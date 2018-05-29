from odoo import api, fields, models
from datetime import datetime
from datetime import timedelta

import logging

_logger = logging.getLogger(__name__)
#credit model, use to keep history of credit on the credit
class SportCredit(models.Model):
    _name = 'sport.credit'
    _description = 'Sport credit'

    name = fields.Char(string='Name', compute="_compute_credit_name")
    client_id = fields.Many2one('res.partner')
    type_id = fields.Many2one('sport.type_course')
    account_id = fields.Many2one('sport.account')
    date_valid = fields.Datetime(default=datetime.now() + timedelta(days=365))
    number_actual = fields.Integer(String="Crédit rstant")
    total = fields.Float(compute='_compute_total')
    quotation_ids = fields.One2many('sale.order', 'credit_id')
    quotation_count = fields.Integer(compute="_compute_quotation_count")
    date_buy = fields.Datetime(default=datetime.now(), string="Date d'achat")
    qty_buy = fields.Integer(string="Quantité initial")
    product_id = fields.Many2one('product.template', string="Carte")
    status = fields.Selection([
        ('valid', 'Valid'),
        ('invalid', 'Invalid'),
    ], string="Credit status", default="valid")

    @api.multi
    def _compute_credit_name(self):
        self.name = self.env['ir.sequence'].next_by_code('sale.order') or _('New')

    @api.onchange('quotation_ids')
    def _compute_quotation_count(self):
        for credit in self:
            credit.quotation_count = 0
            for quotation in credit.quotation_ids:
                credit.quotation_count += 1

    def _compute_date_valid(self):
        pass
    
    @api.depends('number_actual', 'type_id')
    def _compute_total(self):
        for credit in self:
            credit.total = credit.number_actual * credit.type_id.price

    @api.depends('status')
    def _set_invalid(self):
        for credit in self:
            credit.status = "invalid"


    @api.depends('status')
    def _toogle_validity(self):
        for credit in self:
            if credit.status == "invalid":
                credit.status = "valid"
            else:
                credit.status = "invalid"


    def create_sale_order(self):
        for credit in self:

            order = None

            vals = {

                'currency_id':self.env.ref('base.main_company').currency_id.id,
                'partner_id':credit.client_id.id,
                'partner_invoice_id':credit.client_id.id,
                'partner_shipping_id':credit.client_id.id,
                'pricelist_id':credit.client_id.property_product_pricelist.id,
                'credit_id':credit.id,
            }


            order = self.env['sale.order'].create(vals)
            product = credit.type_id.product_id
            vals = {
                'name': product.name,
                'order_id':order.id,
                'price_unit':credit.type_id.price,
                'product_id':product.id,
                'product_uom_qty':credit.number_actual,
            }

            order.line = self.env['sale.order.line'].create(vals)
            
    def invalid_expire_credit(self):
        credits = self.env['sport.credit'].search([['status','=','valid']])
        for credit in credits:
            _logger.info("CREDIT : " + credit.name)
            date = datetime.strptime(credit.date_valid, '%Y-%m-%d %H:%M:%S')
            now = datetime.now()
            if date.year <= now.year and date.month <= now.month and date.day <= now.day:
                credit.status = "invalid"

    
    @api.depends('status')
    def toogle_active(self):
        for credit in self:
            if credit.status == "valid":
                credit.status = "invalid"
            else:
                credit.status = "valid"