from odoo import fields, models, api
from odoo.tools.float_utils import float_round


class InheritResPartner(models.Model):
    _inherit = 'res.partner'

    product_bought_count = fields.Integer(string="Bought Count", compute='_compute_bought_count')

    @api.depends('sale_order_ids')
    def _compute_bought_count(self):
        self.product_bought_count = len(self.sale_order_ids.order_line.product_template_id.ids)

    def get_product_bought(self):
        for rec in self.sale_order_ids.order_line:
            print(rec.product_template_id.id)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Product Bought',
            'view_mode': 'tree,form',
            'res_model': 'product.template',
            'domain': [('id', '=', self.sale_order_ids.order_line.product_template_id.ids)],
            'context': "{'create': False}"
        }


class InheritProductTemplate(models.Model):
    _inherit = 'product.template'

    total_sale_count = fields.Integer(string="Total Sale Count", compute='_compute_total_sale_count')

    @api.depends('total_sale_count')
    def _compute_total_sale_count(self):
        # for product in self:
        #     product.total_sale_count = float_round(
        #         sum([p.sales_count for p in product.with_context(active_test=False).product_variant_ids]),
        #         precision_rounding=product.uom_id.rounding)
        record = self.env["sale.order"].search([('state', '!=', ['draft', 'sent'])])
        self.total_sale_count = 0
        print(record)
        for rec in record:
            for line in rec.order_line:
                print(line.product_id.product_tmpl_id)
                if line.product_id.product_tmpl_id.id == self.id:
                    self.total_sale_count = self.total_sale_count + line.product_uom_qty

    @api.onchange('list_price')
    def _onchange_list_price(self):

        print(self.list_price)
        print(self._origin.id)
        all_sale_order_line = self.env['sale.order.line'].search([('product_template_id', '=', self._origin.id)])
        print(all_sale_order_line)

        for rec in all_sale_order_line:
            if rec.order_id.state == 'draft':
                rec.price_unit = self.list_price


