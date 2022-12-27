# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class VehicleRental(http.Controller):

    @http.route('/vehicle_rental_web_form/', type="http", website=True, auth='public')
    def vehicle_rental_web_form(self, **kw):
        # customer_rec = request.env['res.partner'].sudo().search([])
        vehicle_rec = request.env['vehicle.rental.property'].sudo().search([])
        period_type_rec = request.env['time.selection'].sudo().search([])

        return http.request.render("vehicle_rental.vehicle_rental_page", {
            # 'customer_rec': customer_rec,
            'customer_rec': request.env.user.partner_id,
            'vehicle_rec': vehicle_rec,
            'period_type_rec': period_type_rec
        })

    @http.route('/create_rent_request/', type="http", website=True, auth='public')
    def create_rent_request(self, **kw):
        print(kw)
        partner = request.env['res.partner'].sudo().search([('name', '=', kw['customer_name'])], limit=1)
        print(partner)
        # if user:
        #     partner = user.partner_id.id
        #
        # # user_id = request.env['res.user'].browse(int(request.env['res.user']))
        #     kw['customer_name'] = partner
        if not partner:
            partner = request.env['res.partner'].sudo().create({
                'name': kw['customer_name']
            })

        # partner = partner.id

        # user_id = request.env['res.user'].browse(int(request.env['res.user']))
        kw['customer_name'] = partner.id

        print(kw)
        request.env['rent.request'].sudo().create(kw)
        return request.render("vehicle_rental.rent_request_thanks", {})
