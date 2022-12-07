from odoo import fields, models, api


class InheritPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    material_request_id = fields.Many2one('material.request', string='Meterial ID')


class InheritStockPicking(models.Model):
    _inherit = 'stock.picking'

    material_request_id = fields.Many2one('material.request', string='Meterial ID')


class MaterialRequestOrderLine(models.Model):
    _name = "material.request.order.line"
    # _inherit = 'product.template'
    product_name_id = fields.Many2one('product.product', string='Product')
    product_qty = fields.Integer("Quantity")
    product_receive_mode = fields.Selection(string="Receive Mode",
                                            selection=[
                                                ('create_purchase_order', 'Create Purchase Order'),
                                                ('internal_transfer', 'Internal Transfer'),
                                            ]
                                            )
    # seller_id = fields.Many2one('product_template.seller_ids', string='Vendor')
    # seller_id = fields.Char(string='Vendor', related='product.template.seller_ids')
    # product_tmpl_id = fields.Many2one(
    #     'product.template', 'Product Template', check_company=True,
    #     index=True, ondelete='cascade')
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

    # purchase_id = fields.Many2one('purchase.order')
    # material_request_seq_rel_id = fields.Many2one('material.request')
    # purchase_order_rel_id = fields.Many2one("purchase.order")
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
        self.state = "to_approve"

    def action_approve_material_request(self):
        self.state = "approved"

    def action_confirm_material_request(self):
        self.state = "confirmed"
        rfq_list = []
        for rec in self.material_request_order_line_rel_id:
            # print(rec.product_name_id.seller_ids.partner_id.id)
            # print(rec.product_name_id.id)
            # print(rec.product_name_id.name)

            # print(rec.seller_id.id)
            if rec.product_receive_mode == "create_purchase_order":
                # print(rec.product_name_id.product.template)

                rfq = rec.env['purchase.order'].create({

                    'material_request_id': self.id,
                    'partner_id': rec.product_name_id.seller_ids.partner_id.id,
                    "order_line": [(0, 0, {
                        'product_id': rec.product_name_id.id,
                        # 'product_id': self.env['material.request.order.line'],

                        # 'name': p_finished.name,
                        'product_qty': rec.product_qty,
                        'price_unit': rec.product_name_id.list_price,
                    })],
                })
                print(rfq, "kkkkk")
        #         rfq_list.append(rfq.id)
        #         # print(rfq_list)
        # print(rfq_list)
        # self.purchase_order_ids = rfq_list

        # return {
        #     'name': 'create_invoice',
        #     'type': 'ir.actions.act_window',
        #     'view_mode': 'form',
        #     'res_id': rfq.id,
        #     'res_model': 'purchase.order',
        #     'target': 'current'
        # }
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

        print(move_id)
        # return {
        #     'name': 'create_internal_transfer',
        #     'type': 'ir.actions.act_window',
        #     'view_mode': 'form',
        #     'res_id': it.id,
        #     'res_model': 'stock.picking',
        #     'target': 'current'
        # }

    def action_reject_material_request(self):
        self.state = "reject"

    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('material.request')
        return super(MaterialRequest, self).create(vals)

    def get_purchase_order(self):
        print(self.sequence)
        print(self.env["purchase.order"])
        print('self.purchase_order_ids', self.purchase_order_ids)
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

    # self.ensure_one()
    # purchase_orders = self.env['purchase.order'].search([
    #     ('order_line.invoice_lines.analytic_line_ids.account_id', '=', self.id)
    # ])
    # result = {
    #     "type": "ir.actions.act_window",
    #     "res_model": "purchase.order",
    #     "domain": [['id', 'in', purchase_orders.ids]],
    #     "name": "Purchase Orders",
    #     'view_mode': 'tree',
    # }
    # if len(purchase_orders) == 1:
    #     result['view_mode'] = 'form'
    #     result['res_id'] = purchase_orders.id
    # return result
