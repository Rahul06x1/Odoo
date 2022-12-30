from odoo import fields, models, api


class InheritPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    material_request_id = fields.Many2one('material.request', string='Material ID')


class InheritStockPicking(models.Model):
    _inherit = 'stock.picking'

    material_request_id = fields.Many2one('material.request', string='Material ID')


class MaterialRequestOrderLine(models.Model):
    _name = "material.request.order.line"
    product_name_id = fields.Many2one('product.product', string='Product')
    product_qty = fields.Integer("Quantity")
    product_receive_mode = fields.Selection(string="Receive Mode",
                                            selection=[
                                                ('create_purchase_order', 'Purchase Order'),
                                                ('internal_transfer', 'Internal Transfer'),
                                            ]
                                            )

    material_request_rel_id = fields.Many2one('material.request')


class MaterialRequest(models.Model):
    _name = "material.request"
    _description = "material request"
    _rec_name = "sequence"
    _inherit = 'mail.thread', 'mail.activity.mixin'

    sequence = fields.Char("Rental Order No", default="new")
    employee_name_id = fields.Many2one('hr.employee', string='Employee')
    purchase_order_ids = fields.Char()
    purchase_id = fields.Many2many('purchase.order')

    material_request_order_line_rel_id = fields.One2many(
        comodel_name='material.request.order.line',
        inverse_name='material_request_rel_id',
        string="Order Lines",
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('to_approve', 'To Approve'),
            ('approved', 'Approved'),
            ('confirmed', 'Confirmed'),
            ('reject', 'Rejected'),

        ], default='draft'
    )

    def action_submit_material_request(self):
        self.write({'state': 'to_approve'})
        self.sale_order_id.action_confirm()

    def action_approve_material_request(self):
        # self.state = "approved"
        self.write({'state': 'approved'})

    def action_confirm_material_request(self):
        # self.state = "confirmed"
        self.write({'state': 'confirmed'})
        order_line = []
        vendor_list = []
        for rec in self.material_request_order_line_rel_id:

            if rec.product_receive_mode == "create_purchase_order":

                for vendor in rec.product_name_id.seller_ids:
                    if vendor.partner_id in vendor_list:
                        order_line.append((0, 0, {
                            'product_id': rec.product_name_id.id,
                            'product_qty': rec.product_qty,
                            'price_unit': vendor.price,
                        }))
                        check_vendor = self.env['purchase.order'].search(
                            [('material_request_id', '=', self.id), ("partner_id", '=', vendor.partner_id.id)])
                        rfq = check_vendor.write({
                            "order_line": order_line,
                        })
                    else:
                        vendor_list.append(vendor.partner_id)
                        rfq = rec.env['purchase.order'].create({

                            'material_request_id': self.id,
                            'partner_id': vendor.partner_id.id,

                            "order_line": [(0, 0, {
                                'product_id': rec.product_name_id.id,

                                'product_qty': rec.product_qty,
                                'price_unit': vendor.price,
                            })],
                        })

        move_id = []
        for rec in self.material_request_order_line_rel_id:
            if rec.product_receive_mode == "internal_transfer":
                move_id.append((0, 0, {

                    "name": "internal transfer",
                    'product_id': rec.product_name_id.id,
                    'location_id': rec.product_name_id.property_stock_inventory.id,
                    'location_dest_id': self.employee_name_id.work_location_id.id,
                    'product_uom_qty': rec.product_qty,
                }))
        it = self.env['stock.picking'].create({
            'material_request_id': self.id,
            'partner_id': self.employee_name_id.id,
            "picking_type_id": self.env.ref('stock.picking_type_internal').id,
            'location_id': self.material_request_order_line_rel_id.product_name_id.property_stock_inventory.id,
            'location_dest_id': self.employee_name_id.work_location_id.id,

            "move_ids": move_id,
        })
        print(it)

    def action_reject_material_request(self):
        # self.state = "reject"
        self.write({'state': 'reject'})

    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('material.request')
        return super(MaterialRequest, self).create(vals)

    def get_purchase_order(self):

        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Order',
            'view_mode': 'tree,form',
            'res_model': 'purchase.order',
            'domain': [('material_request_id', '=', self.id)],
            'context': "{'create': False}"
        }

    def get_internal_transfer(self):

        return {
            'type': 'ir.actions.act_window',
            'name': 'Internal Transfer',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'domain': [('material_request_id', '=', self.id)],
            'context': "{'create': False}"
        }
