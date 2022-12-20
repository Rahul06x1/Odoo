from odoo import models, api


class InheritSaleOrder(models.Model):
    _inherit = 'sale.order'

    def merge_sale_order_line(self, res):
        for line in res.order_line:
            if line.id in res.order_line.ids:
                line_ids = res.order_line.filtered(lambda m: m.product_id.id == line.product_id.id and m.price_unit == line.price_unit)
                quantity = 0
                for qty in line_ids:
                    quantity += qty.product_uom_qty
                line_ids[0].write({'product_uom_qty': quantity,
                                   'order_id': line_ids[0].order_id.id,
                                   'price_unit': line_ids[0].price_unit})
                line_ids[1:].unlink()

    @api.model
    def create(self, vals):
        res = super(InheritSaleOrder, self).create(vals)
        res.merge_sale_order_line(res)
        return res

    def write(self, vals):
        res = super(InheritSaleOrder, self).write(vals)
        self.merge_sale_order_line(self)
        return res
