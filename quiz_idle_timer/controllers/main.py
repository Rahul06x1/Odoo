from odoo import http
from odoo.http import request


class IdleTimerController(http.Controller):
    @http.route('/survey/idle/timer', type='json', auth='public')
    def get_token_idle_timer(self, token):
        survey = request.env['survey.survey'].sudo().search([('access_token', '=', token)])
        values = {'idle_timer': survey.idle_timer,
                  'time_limit': survey.time_limit,
                  'pages': len(survey.question_ids.ids)
                  }
        return values

