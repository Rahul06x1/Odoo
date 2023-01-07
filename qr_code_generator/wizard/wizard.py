from odoo import fields, models


class QRCodeGeneratorWizard(models.TransientModel):
    _name = 'qr.code.generator.wizard'

    date_from = fields.Date("Date From")
    date_to = fields.Date("Date To")
