# -*- coding: utf-8 -*-
from odoo import http

# class CrmCalculateClientAge(http.Controller):
#     @http.route('/crm_calculate_client_age/crm_calculate_client_age/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/crm_calculate_client_age/crm_calculate_client_age/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('crm_calculate_client_age.listing', {
#             'root': '/crm_calculate_client_age/crm_calculate_client_age',
#             'objects': http.request.env['crm_calculate_client_age.crm_calculate_client_age'].search([]),
#         })

#     @http.route('/crm_calculate_client_age/crm_calculate_client_age/objects/<model("crm_calculate_client_age.crm_calculate_client_age"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('crm_calculate_client_age.object', {
#             'object': obj
#         })