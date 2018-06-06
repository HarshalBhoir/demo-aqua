# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
import logging
_logger = logging.getLogger(__name__)


class client_history_product(models.Model):
    _inherit = 'res.partner'

    # list_products = fields.Many2many(
    #     'client.product', compute='get_last_10_product')
    list_products = fields.Many2many(
        'product.template', compute='get_last_10_product')

    # Return the last 10 product bought by client on POS.
    def get_last_10_product(self):
        for partner in self:
            products = []
            order_ids = self.env['pos.order'].search(
                [('partner_id', '=', partner.id)], order='date_order desc')
            for order in order_ids:
                if order:
                    # product = self.env['client.product']
                    # date_order = order.date_order
                    for line in order.lines:
                        if not line.product_id in products:
                            # products.append(
                                # product.create(
                                #     {'product_id': line.product_id.product_tmpl_id.id, 'date_order': date_order})
                            # )
                            products.append(line.product_id.product_tmpl_id.id)
                            if len(products) > 9:
                                partner.list_products = products
                                return

            partner.list_products = products


class ClientProduct(models.Model):
    _name = 'client.product'

    product_id = fields.Many2one('product.template')
    date_order = fields.Datetime()
