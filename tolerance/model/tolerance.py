from odoo import fields, models, api


class InheritSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    tolerance = fields.Integer("Tolerance", compute='_compute_tolerance', readonly=0, store=True)

    @api.depends('order_id.partner_id.tolerance')
    def _compute_tolerance(self):
        for rec in self:
            rec.tolerance = rec.order_id.partner_id.tolerance


class InheritPurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    tolerance = fields.Integer("Tolerance", compute='_compute_tolerance', readonly=0, store=True)

    @api.depends('order_id.partner_id.tolerance')
    def _compute_tolerance(self):
        for rec in self:
            rec.tolerance = rec.order_id.partner_id.tolerance


class InheritResPartner(models.Model):
    _inherit = 'res.partner'
    tolerance = fields.Integer("Tolerance")


class InheritStockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):

        for rec in self.move_ids:
            if rec.purchase_line_id:
                tolerance = rec.purchase_line_id.tolerance
            if rec.sale_line_id:
                tolerance = rec.sale_line_id.tolerance
            min_tolerance = rec.product_uom_qty - tolerance
            max_tolerance = rec.product_uom_qty + tolerance
            if not min_tolerance <= rec.quantity_done <= max_tolerance:
                return {
                    'name': 'Tolerance Warning',
                    'type': 'ir.actions.act_window',
                    'res_model': 'tolerance.warning.wizard',
                    'view_mode': 'form',
                    'target': 'new'
                }
        res = super(InheritStockPicking, self).button_validate()
        return res
