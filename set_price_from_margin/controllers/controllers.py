# -*- coding: utf-8 -*-
from odoo import http

# class SetPriceFromMargin(http.Controller):
#     @http.route('/set_price_from_marrgin/set_price_from_marrgin/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/set_price_from_marrgin/set_price_from_marrgin/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('set_price_from_marrgin.listing', {
#             'root': '/set_price_from_marrgin/set_price_from_marrgin',
#             'objects': http.request.env['set_price_from_marrgin.set_price_from_marrgin'].search([]),
#         })

#     @http.route('/set_price_from_marrgin/set_price_from_marrgin/objects/<model("set_price_from_marrgin.set_price_from_marrgin"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('set_price_from_marrgin.object', {
#             'object': obj
#         })