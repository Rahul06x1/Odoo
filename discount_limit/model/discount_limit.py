from odoo import fields, models
from odoo.exceptions import ValidationError
from odoo.tools import date_utils


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    discount_limits = fields.Boolean("Discount Limit", config_parameter='discount_limit.discount_limits')
    discount_limit_amount = fields.Float(config_parameter='discount_limit.discount_limit_amount')


class InheritSaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        all_sale_order = self.search([])
        discount_per_order_line = 0
        for rec in self.order_line:
            discount_per_order_line += rec.discount

        calculated_discount = 0
        for rec in all_sale_order:
            order_date = rec.date_order.date()
            start_date_of_month = date_utils.start_of(rec.date_order.date(), 'month')
            end_date_of_month = date_utils.end_of(rec.date_order.date(), 'month')

            if start_date_of_month <= order_date <= end_date_of_month:

                for discount_per_sale_order in rec.order_line:
                    calculated_discount_per_line = (discount_per_sale_order.product_uom_qty
                                                    * discount_per_sale_order.price_unit) \
                                                   - discount_per_sale_order.price_subtotal
                    calculated_discount += calculated_discount_per_line

        discount_limit = float(self.env['ir.config_parameter'].sudo().get_param('discount_limit.discount_limit_amount'))

        if calculated_discount > discount_limit and discount_per_order_line > 0 \
                and bool(self.env['ir.config_parameter'].sudo().get_param('discount_limit.discount_limits')) == True:
            raise ValidationError("Total discount of the month is exceed the limit")
        res = super(InheritSaleOrder, self).action_confirm()
        return res
