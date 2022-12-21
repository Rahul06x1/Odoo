# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class VehicleRental(http.Controller):

    @http.route('/vehicle_rental_web_form/', type="http", website=True, auth='public')
    def vehicle_rental_web_form(self, **kw):
        return http.request.render("vehicle_rental.vehicle_rental_page", {})

    @http.route('/create_rent_request/', type="http", website=True, auth='public')
    def create_rent_request(self, **kw):
        # request.env['rent.request'].sudo().create(kw)
        return request.render("vehicle_rental.rent_request_thanks", {})
