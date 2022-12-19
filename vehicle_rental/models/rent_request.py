from odoo import fields, models, api
from datetime import datetime
from odoo.exceptions import UserError


class RentRequest(models.Model):
    _name = "rent.request"
    _description = "rental request"
    _rec_name = "sequence"
    _inherit = 'mail.thread', 'mail.activity.mixin'

    sequence = fields.Char("Rental Order No", default="new")
    customer_name = fields.Many2one('res.partner', 'Customer')
    request_date = fields.Date('Request Date', default=datetime.today())
    vehicle = fields.Many2one('vehicle.rental.property', 'Vehicle')

    from_date = fields.Date('From date')
    to_date = fields.Date('To date')
    period = fields.Integer('Period', readonly=1)
    model_year = fields.Char("Model year", related='vehicle.model_year', readonly=0)
    company_id = fields.Many2one('res.company', 'Company')
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda self: self.env.company.currency_id.id, required=True)
    request_state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('returned', 'Returned'),
            ('invoiced', 'Invoiced'),

        ], default='draft'
    )
    period_type = fields.Many2one('time.selection', 'Period Type')

    time_amount = fields.Monetary("Rent Price")

    @api.onchange('period_type')
    def _onchange_period_type(self):
        self.time_amount = self.period_type.time_amount

    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('rent.request')
        return super(RentRequest, self).create(vals)

    def action_confirm(self):
        self.request_state = "confirmed"
        self.vehicle.state = "not_available"

    def action_return(self):
        self.request_state = "returned"
        self.vehicle.state = "available"

    def action_create_invoice(self):
        self.request_state = "invoiced"
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.customer_name.id,
            'currency_id': self.currency_id.id,
            'invoice_date': self.to_date,

            'invoice_line_ids': [(0, 0, {
                'name': "Vehicle Rent",
                'quantity': 1,
                'price_unit': self.time_amount,
            })],
        })

        return {
            'name': 'create_invoice',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_id': invoice.id,
            'res_model': 'account.move',
            'target': 'current'
        }

    @api.onchange('from_date', 'to_date')
    def calculate_date(self):
        if self.from_date and self.to_date:
            d1 = datetime.strptime(str(self.from_date), '%Y-%m-%d')
            d2 = datetime.strptime(str(self.to_date), '%Y-%m-%d')
            d3 = d2 - d1
            self.period = str(d3.days)
            if self.period < 0:
                raise UserError("Sorry, End Date Must be greater Than Start Date.")
