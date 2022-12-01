from odoo import fields, models, api
from datetime import datetime
from odoo.exceptions import UserError


class RentalRequest(models.Model):
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
    vehicle_rent = fields.Monetary('Rent')
    request_state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('returned', 'Returned'),
            ('invoiced', 'Invoiced'),

        ], default='draft'
    )
    period_type = fields.Many2one('time.selection', 'Period Type')

    time_amount = fields.Integer("Rent Priceee")



    @api.onchange('period_type')
    def _onchange_period_type(self):
        # print(self.env['time.selection'].search(['selection_time', '=', self.period_type]))
        # print(self.env['time.selection'].browse(1))
        self.time_amount = self.period_type.time_amount
        # self.period_type = self.selection_time

    @api.onchange('vehicle')
    def _onchange_type(self):
        # print(self.vehicle.vehicle_rent)
        self.vehicle_rent = self.vehicle.vehicle_rent
        # self.period_type = self.selection_time

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

    def action_create_invoice(self):
        self.request_state = "invoiced"
        invoice = self.env['account.move'].with_context(default_move_type='out_invoice').create({
            'move_type': 'out_invoice',
            'partner_id': self.customer_name.id,
            'currency_id': self.currency_id.id,
            'invoice_date': self.to_date,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.vehicle.id,
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
        print(invoice)

        # invoice = self.env['account.move'].create({
        #     'type': 'out_invoice',
        #     'journal_id': journal.id,
        #     'partner_id': product_id.id,
        #     'invoice_date': date_invoice,
        #     'date': date_invoice,
        #     'invoice_line_ids': [(0, 0, {
        #         'product_id': product_id.id,
        #         'quantity': 40.0,
        #         'name': 'product test 1',
        #         'discount': 10.00,
        #         'price_unit': 2.27,
        #     })]
        # })
        # return invoice
        # rslt = self.env['account.move'].create({
        #     'partner_id': self.customer_name.id,
        #     # 'currency_id': self.currency_two.id,
        #     'name': 'customer invoice',
        #     'type': 'out_invoice',
        #     # 'date_invoice': date,
        #     'account_id': self.env['account'].account_receivable.id,
        #     'invoice_line_ids': [(0, 0, {
        #         'name': 'test line',
        #         # 'origin': sale_order.name,
        #         # 'account_id': self.account_income.id,
        #         'price_unit': self.product_price_unit,
        #         'quantity': 1.0,
        #         'discount': 0.0,
        #         # 'uom_id': product.uom_id.id,
        #         # 'product_id': product.id,
        #         # 'sale_line_ids': [(6, 0, [line.id for line in sale_order.order_line])],
        #     })],
        # })
        # return rslt

    @api.onchange('from_date', 'to_date')
    def calculate_date(self):
        if self.from_date and self.to_date:
            d1 = datetime.strptime(str(self.from_date), '%Y-%m-%d')
            d2 = datetime.strptime(str(self.to_date), '%Y-%m-%d')
            d3 = d2 - d1
            self.period = str(d3.days)
            if self.period < 0:
                raise UserError("Sorry, End Date Must be greater Than Start Date.")

    # relation_id = fields.fields.One2many("time.selection", "relation_id")
    # relation_id = fields.Char("relation id", related='time.selection.relation_id')

    # ,domain=[("relation_id", "=", vehicle)])
    # # @api.model
    # @api.onchange('vehicle')
    # def _get_relation_id(self):
    #     print(self.vehicle)
    #     print(self.env['vehicle.rental.property'].search([('vehicle', '=', self.vehicle.id)]))
    #     print(self.env['vehicle.rental.property'].search([('time', '!=', False)]))
    #
    #     # print(self.env['time.selection'].search([('relation_id', '=', self.vehicle)]))
    #     # return [('vehicle', '=', self.vehicle.id)]
    #     domain = [('relation_id', '=', self.vehicle)]
    #     # return domain

    # , domain=[('relation_id', '=', vehicle)])

    # , domain=_get_relation_id)

    # def a(self):
    #     print(self.period_type)

    # @api.onchange('vehicle')
    # def onchange_partner_id(self):
    #     for rec in self:
    #         return {'domain': {'vehicle': [('vehicle.rental.property.vehicle', '=', rec.vehicle.id)]}}
    # period_type = fields.Many2one('time.selection', 'Period Type',domain=onchange_partner_id())
