from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_confirmation_template(self):
        mail_template = self.env.ref('website_pay_mail.email_template_name')
        mail_template.send_mail(self.id, force_send=True)
