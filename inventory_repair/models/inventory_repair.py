from odoo import fields, models, api


class SaleOrderInherit(models.Model):
    _inherit = "sale.order"
    inventory_repair = fields.Boolean(string='Repair', readonly=1)

    @api.onchange('partner_id')
    def customer_onchange(self):
        list = []
        for i in self.env['inventory.repair'].search([]):
            list.append(i.customer_id.name)
        if self.partner_id.name in list:
            return {'value': {}, 'warning': {'title': 'warning',
                                             'message': 'This User has Some Pending Repair Requests'}}


class InventoryRepair(models.Model):
    _name = "inventory.repair"
    _rec_name = "sale_order_id"
    _inherit = 'mail.thread', 'mail.activity.mixin'

    sale_order_id = fields.Many2one('sale.order', "Sale Order", required=True, domain="[('state', '=', 'sale')]")
    customer_id = fields.Many2one('res.partner', "Customer")
    product_id = fields.Many2one('product.template', string='Product')
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('confirm', 'Confirm'),
            ('done', 'Done'),

        ], default='draft'
    )

    @api.onchange('sale_order_id')
    def _onchange_sale_order_id(self):
        products = self.sale_order_id.order_line.product_id
        return {'domain': {'product_id': [('id', 'in', products.ids)]}}

    @api.onchange('sale_order_id')
    def _onchange_type(self):
        self.customer_id = self.sale_order_id.partner_id

    def action_confirm(self):
        self.state = "confirm"
        self.sale_order_id.inventory_repair = True

    def action_done(self):
        self.state = "done"
