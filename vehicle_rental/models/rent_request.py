from odoo import fields, models, api
from datetime import datetime
from odoo.exceptions import ValidationError


class RentalRequest(models.Model):
    _name = "rent.request"
    _description = "rental request"
    _rec_name = "sequence"

    sequence = fields.Char("Rental Order No", default="new")
    # sequence = fields.Char(compute='_vehicle_name_modelyear')

    customer_name = fields.Many2one('res.partner', 'Customer')
    request_date = fields.Date('request date', default=datetime.today())
    vehicle = fields.Many2one('vehicle.rental.property', 'Vehicle')
    from_date = fields.Date('from date')
    to_date = fields.Date('to date')
    period = fields.Integer('Period', readonly=1)
    model_year = fields.Char("model year", related='vehicle.model_year', readonly=0)
    company_id = fields.Many2one('res.company', 'Company')
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda self: self.env.company.currency_id.id, required=True)
    vehicle_rent = fields.Integer('Rent',readonly=1)
    # vehicle_rent = fields.Many2one('vehicle.rental.property.vehicle.rent', 'Rent')
    request_state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('returned', 'Returned'),

        ], default='draft'
    )


    @api.onchange('vehicle')
    def _onchange_type(self):
        # print(self.vehicle.vehicle_rent)
        self.vehicle_rent = self.vehicle.vehicle_rent

    # model_year = fields.Many2one('vehicle.rental.property.model.year', 'Vehicle')
    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('rent.request')
        return super(RentalRequest, self).create(vals)

    def action_confirm(self):
        self.request_state = "confirmed"
        self.vehicle.state = "not_available"

    def action_return(self):
        self.request_state = "returned"
        self.vehicle.state = "available"

    @api.onchange('from_date', 'to_date')
    def calculate_date(self):
        if self.from_date and self.to_date:
            d1 = datetime.strptime(str(self.from_date), '%Y-%m-%d')
            d2 = datetime.strptime(str(self.to_date), '%Y-%m-%d')
            d3 = d2 - d1
            self.period = str(d3.days)

    @api.constrains('to_date', 'from_date')
    def date_constrains(self):
        for rec in self:
            if rec.to_date < rec.from_date:
                raise ValidationError('Sorry, End Date Must be greater Than Start Date...')
