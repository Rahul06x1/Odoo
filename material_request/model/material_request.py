from odoo import fields, models


class MaterialRequestOrderLine(models.Model):
    _name = "material.request.order.line"
    # _inherit = 'product.template'
    product_name_id = fields.Many2one('product.product', string='Product')
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

    employee_name_id = fields.Many2one('hr.employee', string='Employee')
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
        for rec in self.material_request_order_line_rel_id:
            print(rec.product_name_id.seller_ids.partner_id.id)
            print(rec.product_name_id.id)
            print(rec.product_name_id.name)

            # print(rec.seller_id.id)
            if rec.product_receive_mode == "create_purchase_order":
                # print(rec.product_name_id.product.template)
                rfq = rec.env['purchase.order'].create({
                    'partner_id': rec.product_name_id.seller_ids.partner_id.id,
                    "order_line": [(0, 0, {
                        'product_id': rec.product_name_id.id,
                        # 'product_id': self.env['material.request.order.line'],

                        # 'name': p_finished.name,
                        # 'product_qty': 2.0,
                        'price_unit': rec.product_name_id.list_price,
                    })],
                })

                return {
                    'name': 'create_invoice',
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_id': rfq.id,
                    'res_model': 'purchase.order',
                    'target': 'current'
                }

    def action_reject_material_request(self):
        self.state = "reject"

        # order = order.with_company(order.company_id)
        # pending_section = None
        # # Invoice values.
        # invoice_vals = order._prepare_invoice()
        # # Invoice line values (keep only necessary sections).
        # for line in order.order_line:
        #     if line.display_type == 'line_section':
        #         pending_section = line
        #         continue
        #     if not float_is_zero(line.qty_to_invoice, precision_digits=precision):
        #         if pending_section:
        #             line_vals = pending_section._prepare_account_move_line()
        #             line_vals.update({'sequence': sequence})
        #             invoice_vals['invoice_line_ids'].append((0, 0, line_vals))
        #             sequence += 1
        #             pending_section = None
        #         line_vals = line._prepare_account_move_line()
        #         line_vals.update({'sequence': sequence})
        #         invoice_vals['invoice_line_ids'].append((0, 0, line_vals))
        #         sequence += 1
        # invoice_vals_list.append(invoice_vals)
