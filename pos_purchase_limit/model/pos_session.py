from odoo import models


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_res_partner(self):
        result = super()._loader_params_res_partner()
        result['search_params']['fields'].extend(['activate_purchase_limit', 'purchase_limit_amount'])
        print('result', result)
        return result
