# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp
import logging

_logger = logging.getLogger(__name__)


class SetPriceFromMargin(models.Model):
    _inherit = 'product.template'

    # margin = fields.Float(digits=dp.get_precision('Product margin'))
    margin = fields.Float()
    type_margin = fields.Selection([
        ('rate', 'Rate'),
        ('amount', 'Amount')
    ])

    #
    @api.depends('margin')
    def _set_list_price(self):
        for price in self:
            price.list_price = price.price_calculation()

    # Change price on change margin
    @api.onchange('margin')
    def update_price_on_change_margin(self):
        for price in self:
            price.list_price = price.price_calculation()

    # Change price on change type margin
    @api.onchange('type_margin')
    def update_price_on_change_type_margin(self):
        for price in self:
            price.list_price = price.price_calculation()

    # Change price on change standard price
    @api.onchange('standard_price')
    def update_price_on_change_standard_price(self):
        for price in self:
            price.list_price = price.price_calculation()

    # Calculation of price
    def price_calculation(self):
        for price in self:
            if price.type_margin == 'rate':
                tmp_price = float(price.standard_price) * (1 + (float(price.margin) / 100))
            elif price.type_margin == 'amount':
                tmp_price = float(price.standard_price) + float(price.margin)
            else:
                tmp_price = price.list_price

        return tmp_price
