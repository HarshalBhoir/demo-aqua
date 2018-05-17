# -*- coding: utf-8 -*-
from odoo import http

# class ReceiptChecksDate(http.Controller):
#     @http.route('/receipt_checks_date/receipt_checks_date/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/receipt_checks_date/receipt_checks_date/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('receipt_checks_date.listing', {
#             'root': '/receipt_checks_date/receipt_checks_date',
#             'objects': http.request.env['receipt_checks_date.receipt_checks_date'].search([]),
#         })

#     @http.route('/receipt_checks_date/receipt_checks_date/objects/<model("receipt_checks_date.receipt_checks_date"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('receipt_checks_date.object', {
#             'object': obj
#         })