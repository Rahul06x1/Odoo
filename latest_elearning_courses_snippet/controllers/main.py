from odoo import http


class ElearningSnippet(http.Controller):

    @http.route("/latest_courses", auth="public", type="json")
    def elearning_snippet(self):
        latest_course = http.request.env['slide.channel'].search_read([('website_published', '=', True)],
                                                                      ['name', 'image_1920', 'id', 'description'],
                                                                      order='create_date desc')
        return latest_course
