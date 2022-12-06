from odoo import fields, models


class MaterialRequestToApprove(models.Model):
    _name = "material.request.to.approve"
    _description = "material request to approve"

    employee_name_id = fields.Many2one('material.request', 'Vehicle')

