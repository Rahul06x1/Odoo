from odoo import fields, models, api
from datetime import datetime


class InheritFleet(models.Model):
    _inherit = 'fleet.vehicle'
    registration_date = fields.Date("Registration Date")
    # model_year=fields.Char("Model Year")

    # model_year = registration_date.year


class TimeSelection(models.Model):
    _name = "time.selection"
    _rec_name = "selection_time"
    selection_time = fields.Selection(string="Duration",
                                      selection=[
                                          ('hour', 'Hour'),
                                          ('day', 'Day'),
                                          ('week', 'Week'),
                                          ('month', 'Month'),

                                      ]
                                      )
    time_amount = fields.Integer('Rent Price')
    relation_id = fields.Many2one('vehicle.rental.property')


class VehicleRentalModel(models.Model):
    _name = "vehicle.rental.property"
    _rec_name = "combination"
    _description = "vehicle rental model"
    _inherit = 'mail.thread', 'mail.activity.mixin'

    # customer_name = fields.Many2one('res.partner', 'Customer')

    vehicle = fields.Many2one('fleet.vehicle', 'Vehicle', required=True, domain=[("state_id.name", "=", "Registered")])

    brand_name = fields.Char('Brand', help="Brand of the vehicle", related='vehicle.brand_id.name',
                             store=True)  # required=True,
    registration_date = fields.Date('Registration Date', related='vehicle.registration_date', readonly=0)
    # model_year = registration_date.year
    model_year = fields.Char("Model Year", related='vehicle.model_year', readonly=0)

    time = fields.One2many("time.selection", "relation_id")

    confirmed_rental_request = fields.One2many('rent.request', 'vehicle', readonly=1,
                                               domain=[('request_state', '=', 'confirmed')])

    @api.onchange('registration_date')
    def _onchange_type(self):
        print(self.registration_date)
        if self.vehicle.registration_date:
            print("date_yr", self.registration_date.year)
            self.model_year = self.registration_date.year
            print("model year", self.model_year)
            # print("model year", self.vehicle.model_year)
            # print("date_yr", self.vehicle.registration_date.year)
            # self.vehicle.model_year = self.vehicle.registration_date.year

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

    def get_vehicle_request(self):
        # self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Rental Request History',
            'view_mode': 'tree',
            'res_model': 'rent.request',
            'domain': [('vehicle', '=', self.id)],
            'context': "{'create': False}"
        }

    # @api.depends('vehicle.display_name', 'model_year')
    # def _compute_fields_combination(self):
    #     for test in self:
    #         test.combination = str(test.vehicle.display_name + '/' + test.vehicle.model_year)

    @api.depends('vehicle.display_name', 'model_year')
    def _compute_fields_combination(self):
        for test in self:
            test.combination = str(test.vehicle.display_name + '/' + test.vehicle.model_year)