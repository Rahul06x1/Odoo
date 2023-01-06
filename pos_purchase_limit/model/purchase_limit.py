from odoo import fields, models


class InheritProductTemplate(models.Model):
    _inherit = 'res.partner'
    activate_purchase_limit = fields.Boolean(string="Activate Purchase Limit")
    purchase_limit_amount = fields.Float()
