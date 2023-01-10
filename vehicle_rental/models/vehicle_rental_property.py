from odoo import fields, models, api
from datetime import date


class InheritFleet(models.Model):
    _inherit = 'fleet.vehicle'
    registration_date = fields.Date("Registration Date")


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
    company_id = fields.Many2one('res.company', 'Company')
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda self: self.env.company.currency_id.id, required=True)
    time_amount = fields.Monetary('Rent Price')
    relation_id = fields.Many2one('vehicle.rental.property')


class VehicleRentalModel(models.Model):
    _name = "vehicle.rental.property"
    _rec_name = "sequence"

    _description = "vehicle rental model"
    _inherit = 'mail.thread', 'mail.activity.mixin'

    sequence = fields.Char(compute='name_get')
    vehicle = fields.Many2one('fleet.vehicle', 'Vehicle', required=True, domain=[("state_id.name", "=", "Registered")])

    brand_name = fields.Char('Brand', help="Brand of the vehicle", related='vehicle.brand_id.name',
                             store=True)
    registration_date = fields.Date('Registration Date', related='vehicle.registration_date', readonly=0)
    model_year = fields.Char("Model Year", related='vehicle.model_year', readonly=0)

    time = fields.One2many("time.selection", "relation_id")
    warning = fields.Boolean(string='Warning', compute="check_warning_late")
    late = fields.Boolean(string='Late', compute="check_warning_late")

    confirmed_rental_request = fields.One2many('rent.request', 'vehicle', readonly=1,
                                               domain=[('request_state', '=', 'confirmed')])

    to_date = fields.Date("To Date", compute="get_to_date", readonly=0)

    @api.depends('model_year', 'vehicle')
    def name_get(self):
        sequence = []
        for rec in self:
            sequence.append(
                (rec.id, '%s / %s' % (rec.vehicle.name,
                                      rec.model_year)))
        return sequence

    def get_to_date(self):
        for rec in self:
            rent_request_id = rec.env['rent.request'].search([('vehicle', '=', rec.id)], limit=1)

            rec.to_date = rent_request_id.to_date

    @api.depends('to_date')
    def check_warning_late(self):
        self.warning = False
        self.late = False
        for rec in self:
            if rec.to_date:
                today = date.today()
                diff = rec.to_date - today

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

        for rec in self:
            if rec.vehicle.registration_date:
                rec.model_year = rec.registration_date.year

    company_id = fields.Many2one('res.company', 'Company')
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda self: self.env.company.currency_id.id, required=True)

    state = fields.Selection(
        selection=[
            ('available', 'Available'),
            ('not_available', 'Not available'),
            ('sold', 'Sold'),

        ], default='available'
    )

    def get_vehicle_request(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Rental Request History',
            'view_mode': 'tree',
            'res_model': 'rent.request',
            'domain': [('vehicle', '=', self.id)],
            'context': "{'create': False}"
        }
