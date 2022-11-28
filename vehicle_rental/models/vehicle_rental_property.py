from odoo import fields, models, api
from datetime import datetime


class InheritFleet(models.Model):
    _inherit = 'fleet.vehicle'
    registration_date = fields.Date("Registration Date")
    # model_year=fields.Char("Model Year")

    # model_year = registration_date.year


class VehicleRentalModel(models.Model):
    _name = "vehicle.rental.property"
    _rec_name = "combination"
    _description = "vehicle rental model"
    _inherit = 'mail.thread', 'mail.activity.mixin'

    # customer_name = fields.Many2one('res.partner', 'Customer')

    vehicle = fields.Many2one('fleet.vehicle', 'Vehicle', required=True, domain=[("state_id.name", "=", "Registered")])

    brand_name = fields.Char('Brand', help="Brand of the vehicle", related='vehicle.brand_id.name',
                             store=True)  # required=True,
    registration_date = fields.Date('registration date', related='vehicle.registration_date', readonly=0)
    # model_year = registration_date.year
    model_year = fields.Char("model year", related='vehicle.model_year', readonly=0)

    @api.onchange('vehicle.registration_date')
    def _onchange_type(self):
        if self.vehicle.registration_date:
            print(self.vehicle.registration_date.year)
            self.model_year = self.vehicle.registration_date.year
        print(self.model_year)
            # self.fleet.vehicle.model_year = self.fleet.vehicle.registration_date.year

    company_id = fields.Many2one('res.company', 'Company')
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda self: self.env.company.currency_id.id, required=True)
    vehicle_rent = fields.Monetary('Rent', currency_field='currency_id')

    state = fields.Selection(
        selection=[
            ('available', 'Available'),
            ('not_available', 'Not available'),
            ('sold', 'Sold'),

        ], default='available'
    )
    combination = fields.Char(string='Combination', compute='_compute_fields_combination')

    @api.depends('vehicle.display_name', 'model_year')
    def _compute_fields_combination(self):
        for test in self:
            test.combination = test.vehicle.display_name
            # + '/' + test.vehicle.model_year)
