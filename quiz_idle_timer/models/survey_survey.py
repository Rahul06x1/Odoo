from odoo import fields, models


class InheritSurveySurvey(models.Model):
    _inherit = 'survey.survey'

    idle_timer = fields.Float()
