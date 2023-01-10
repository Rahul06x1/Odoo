try:
    import qrcode
except ImportError:
    qrcode = None
try:
    import base64
except ImportError:
    base64 = None
from io import BytesIO
from odoo import models, fields
from odoo.exceptions import UserError


class QRCodeGeneratorWizard(models.TransientModel):
    _name = 'qr.code.generator.wizard'

    text = fields.Text("Enter your text")
    qr_code = fields.Binary('QRcode')

    def generate_qr_code_btn(self):
        for rec in self:
            if qrcode and base64 and rec.text:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=3,
                    border=4,
                )
                qr.add_data(rec.text)
                qr.make(fit=True)
                img = qr.make_image()
                temp = BytesIO()
                img.save(temp, format="PNG")
                qr_image = base64.b64encode(temp.getvalue())
                rec.update({'qr_code': qr_image})
            else:
                raise UserError('Enter your text.')
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'qr.code.generator.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }

    def download_qr_code_btn(self):
        data = {
            'form_data': self.read()[0],
        }
        return self.env.ref('qr_code_generator.action_qr_code_pdf').report_action(self, data=data)

    def reset_btn(self):
        self.text = None
        self.qr_code = None
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'qr.code.generator.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }
