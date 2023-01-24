from odoo import fields, models


class InheritProductTemplate(models.Model):
    _inherit = 'product.template'
    avg_landed_cost = fields.Float()
    last_purchase_qty = fields.Float()


class InheritSaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        for rec in self.order_line:
            if rec.product_uom_qty > rec.product_template_id.last_purchase_qty:
                rec.product_template_id.standard_price += rec.product_template_id.avg_landed_cost
        res = super(InheritSaleOrder, self).action_confirm()
        return res


class InheritStockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'
    average_landed_cost_rel_ids = fields.One2many("stock.average.landed.cost", "relation_id")

    def compute_average_landed_cost(self):
        order_line = [(5, 0, 0)]
        for line in self.valuation_adjustment_lines:
            order_line.append((0, 0, {
                'product_id': line.product_id.product_tmpl_id.id,
                'average_landed_cost': line.additional_landed_cost / line.quantity,
            }))
            self.average_landed_cost_rel_ids = order_line

    def button_validate(self):
        for rec in self.average_landed_cost_rel_ids:
            rec.product_id.avg_landed_cost = rec.average_landed_cost

        for rec in self.valuation_adjustment_lines:
            rec.product_id.last_purchase_qty = rec.quantity

        res = super(InheritStockLandedCost, self).button_validate()
        return res


class AverageLandedCost(models.Model):
    _name = 'stock.average.landed.cost'

    relation_id = fields.Many2one('stock.landed.cost')
    product_id = fields.Many2one('product.template', string='Product')
    average_landed_cost = fields.Float(
        string='Average Landed Cost')
