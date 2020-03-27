# -*- coding: utf-8 -*-
from odoo import http

# class Emsin(http.Controller):
#     @http.route('/emsin/emsin/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/emsin/emsin/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('emsin.listing', {
#             'root': '/emsin/emsin',
#             'objects': http.request.env['emsin.emsin'].search([]),
#         })

#     @http.route('/emsin/emsin/objects/<model("emsin.emsin"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('emsin.object', {
#             'object': obj
#         })