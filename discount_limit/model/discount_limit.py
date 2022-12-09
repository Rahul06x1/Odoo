from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    discount_limits = fields.Boolean("Discount Limit", config_parameter='discount_limit.discount_limits')
    discount_limit_amount = fields.Float(config_parameter='discount_limit.discount_limit_amount')


class InheritSaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        all_sale_order = self.search([])
        print(self)
        print(all_sale_order)
        calculated_discount = 0
        for rec in all_sale_order:
            for discount_per_sale_order in rec.order_line:
                # print(discount_per_sale_order.product_uom_qty)
                # print(discount_per_sale_order.price_unit)
                # print(discount_per_sale_order.price_subtotal)
                calculated_discount_per_line = (discount_per_sale_order.product_uom_qty * discount_per_sale_order.price_unit) - discount_per_sale_order.price_subtotal
                calculated_discount += calculated_discount_per_line
                print(calculated_discount_per_line)
                print(calculated_discount)
                print('-------------')
        res = super(InheritSaleOrder, self).action_confirm()
        return res

    # @api.onchange('partner_id')
    # def on_change_partner_id(self):
    #     x=self.env["sale.order"].search([])
    #     print(x)
    #     print(self.id)
    #     calculated_discount = 0
    #     for rec in self:
    #         for discount_per_sale_order in rec.order_line:
    #             print(discount_per_sale_order.product_uom_qty)
    #             print(discount_per_sale_order.price_unit)
    #             print(discount_per_sale_order.price_subtotal)
    #             calculated_discount += (discount_per_sale_order.product_uom_qty * discount_per_sale_order.price_unit) - discount_per_sale_order.price_subtotal
    #             print(calculated_discount)

    # @api.onchange('partner_id')
    # def on_change_partner_id(self):
    #     calculated_discount = 0
    #     for rec in self.order_line:
    #         print(rec.product_uom_qty)
    #         print(rec.price_unit)
    #         print(rec.price_subtotal)
    #         calculated_discount += (rec.product_uom_qty * rec.price_unit) - rec.price_subtotal
    #         print(calculated_discount)
