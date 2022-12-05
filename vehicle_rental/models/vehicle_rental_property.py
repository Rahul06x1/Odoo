from odoo import fields, models, api
from datetime import date


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
    _rec_name = "vehicle"
    _description = "vehicle rental model"
    _inherit = 'mail.thread', 'mail.activity.mixin'
    # _inherits = {"rent.request": "to_date"}

    # customer_name = fields.Many2one('res.partner', 'Customer')

    vehicle = fields.Many2one('fleet.vehicle', 'Vehicle', required=True, domain=[("state_id.name", "=", "Registered")])

    brand_name = fields.Char('Brand', help="Brand of the vehicle", related='vehicle.brand_id.name',
                             store=True)  # required=True,
    registration_date = fields.Date('Registration Date', related='vehicle.registration_date', readonly=0)
    # model_year = registration_date.year
    model_year = fields.Char("Model Year", related='vehicle.model_year', readonly=0)
    # rent_request_id = fields.Many2one('rent.request', 'TO DATE')

    time = fields.One2many("time.selection", "relation_id")
    warning = fields.Boolean(string='Warning', compute="check_warning_late")
    # , compute='_set_warning')
    late = fields.Boolean(string='Late', compute="check_warning_late")
    # to_date = fields.Date("to date", related='rent.request.to_date')

    confirmed_rental_request = fields.One2many('rent.request', 'vehicle', readonly=1,
                                               domain=[('request_state', '=', 'confirmed')])

    to_date = fields.Date("To Date", compute="get_to_date", readonly=0)

    # today = fields.Date("Today", default=date.today())

    #
    def get_to_date(self):
        for rec in self:
            rent_request_id = rec.env['rent.request'].search([('vehicle', '=', rec.id)], limit=1)
            # print(self.env['rent.request'].vehicle)
            # print(self.id)

            # print(rent_request_id)
            rec.to_date = rent_request_id.to_date
            # print(self.to_date)

    @api.depends('to_date')
    def check_warning_late(self):
        self.warning = False
        self.late = False
        for rec in self:
            if rec.to_date:
                today = date.today()
                diff = rec.to_date - today

                print(diff, 'ss')
                print(diff.days, 'dd')

                if 0 <= diff.days <= 2:

                    rec.warning = True
                else:
                    rec.warning = False
                if rec.to_date < date.today():
                    rec.warning = False
                    rec.late = True
                else:
                    rec.late = False

    @api.onchange('registration_date')
    def _onchange_type(self):
        print(self.registration_date)
        # print(self.rent_request_id)
        # print(self.to_date)

        for rec in self:
            if rec.vehicle.registration_date:
                print("date_yr", rec.registration_date.year)
                rec.model_year = rec.registration_date.year
                print("model year", rec.model_year)
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

    # combination = fields.Char(string='Combination', compute='_compute_fields_combination')
    # @api.one
    # @api.depends('to_date')
    # def _set_warning(self):
    #     self.warning = (datetime.today() == self.env["rent.request"].to_date)

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

    # @api.depends('vehicle.display_name', 'model_year')
    # def _compute_fields_combination(self):
    #     for test in self:
    #         test.combination = str('test.vehicle.display_name' + '/' + 'test.vehicle.model_year')
