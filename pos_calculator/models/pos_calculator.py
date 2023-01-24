from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    virtual_calculator = fields.Boolean("Virtual Calculator", config_parameter='pos_calculator.virtual_calculator')
