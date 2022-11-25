from odoo import fields, models, api
from datetime import datetime


class RentalRequest(models.Model):
    _name = "rent.request"
    _description = "rental request"

    customer_name = fields.Many2one('res.partner', 'Customer')
    request_date = fields.Date('request date', default=datetime.today())
    vehicle = fields.Many2one('fleet.vehicle', 'Vehicle')
    from_date = fields.Date('from date')
    to_date = fields.Date('to date')
    period = fields.Integer('Period')

    @api.onchange('from_date', 'to_date')
    def calculate_date(self):
        if self.from_date and self.to_date:
            d1 = datetime.strptime(str(self.from_date), '%Y-%m-%d')
            d2 = datetime.strptime(str(self.to_date), '%Y-%m-%d')
            d3 = d2 - d1
            self.period = str(d3.days)

    request_state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('returned', 'Returned'),

        ], default='draft'
    )
    rent = fields.Integer('Rent')
