from odoo import models


class ToleranceWarningWizard(models.TransientModel):
    _name = 'tolerance.warning.wizard'

    def action_done(self):
        records = self.env['stock.picking'].browse(self.env.context.get('active_ids'))
        records.write({'state': 'done'})


