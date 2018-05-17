from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    credit_id = fields.Many2one('sport.credit')
