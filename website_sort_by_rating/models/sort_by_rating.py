from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"
    product_rating_avg = fields.Float(related='rating_avg', store=1)


class WebsiteInherit(models.Model):
    _inherit = "website"

    def _get_product_sort_mapping(self):
        res = super(WebsiteInherit, self)._get_product_sort_mapping()
        res.append(('product_rating_avg desc', 'Rating'))

        return res
