from odoo import fields, models


class VehicleRentalModel(models.Model):
    _name = "vehicle.rental.property"
    _description = "vehicle rental model"

    vehicle = fields.Many2one('fleet.vehicle', 'Vehicle',domain = [("state_id.name", "=", "Registered")])

    # vehicle_name = fields.One2many('fleet.vehicle','brand_id','Vname')
    brand_name = fields.Char('Brand', required=True, help="Brand of the vehicle", related='vehicle.brand_id.name')
    registeration_date = fields.Date('regesteration date',related='vehicle.acquisition_date')
    model_year = fields.Char("model year",related='vehicle.model_year')


    # vehicle_rent =
    state = fields.Selection(
        selection=[
            ('available', 'Available'),
            ('not available', 'Not available'),
            ('sold', 'Sold'),

        ], default='available'
    )
   