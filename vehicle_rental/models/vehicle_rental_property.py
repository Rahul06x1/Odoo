from odoo import fields, models


class InheritFleet(models.Model):
    _inherit = 'fleet.vehicle'
    registration_date = fields.Date("Registration Date")


class VehicleRentalModel(models.Model):
    _name = "vehicle.rental.property"
    _rec_name = "customer_name"
    _description = "vehicle rental model"
    _inherit = 'mail.thread', 'mail.activity.mixin'

    customer_name = fields.Many2one('res.partner', 'Customer')
    vehicle = fields.Many2one('fleet.vehicle', 'Vehicle', domain=[("state_id.name", "=", "Registered")])

    brand_name = fields.Char('Brand', help="Brand of the vehicle", related='vehicle.brand_id.name',
                             store=True)  # required=True,
    registration_date = fields.Date('registration date', related='vehicle.registration_date', readonly=0)
    model_year = fields.Char("model year", related='vehicle.model_year', readonly=0)

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
