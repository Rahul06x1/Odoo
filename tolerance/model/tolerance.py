from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # partner_id = fields.Many2one('res.partner', string='Partner ID')
    tolerance = fields.Integer("Tolerance", related='order_id.partner_id.tolerance', readonly=0)

    # @api.depends('sale.order.partner_id')
    # def _compute_tolerance(self):
    #     print(self)
    #     print(self.partner_id)


class InheritResPartner(models.Model):
    _inherit = 'res.partner'
    tolerance = fields.Integer("Tolerance")

# class Tolerance(models.Model):
#     _name = "tolerance"
#     _description = "Tolerance"
