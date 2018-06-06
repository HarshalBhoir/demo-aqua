# -*- coding: utf-8 -*-
from odoo import http

# class ClientHistoryProduct(http.Controller):
#     @http.route('/client_history_product/client_history_product/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/client_history_product/client_history_product/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('client_history_product.listing', {
#             'root': '/client_history_product/client_history_product',
#             'objects': http.request.env['client_history_product.client_history_product'].search([]),
#         })

#     @http.route('/client_history_product/client_history_product/objects/<model("client_history_product.client_history_product"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('client_history_product.object', {
#             'object': obj
#         })