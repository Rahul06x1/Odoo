# from odoo import http
# from odoo.http import request
#
#
# class Sales(http.Controller):
#     @http.route(['/total_product_sold'], type="json", auth="public")
#     def sold_total(self):
#         sale_obj = request.env['sale.order'].sudo().search([])
#         total_sold = sum(sale_obj.mapped('order_line.product_uom_qty'))
#         return total_sold

# class Snippet(http.Controller):
#     @http.route('/new_product', type="json", auth="public")
#     def get_new_product(self):
#         product = request.env['product.product'].sudo().search([], order='create_date desc', limit=1)
#         print('product', product)
#         print('product.list_price', product.list_price)
#         values = {'products': product.read()}
#         print(values)
#         # return values
#         response = http.Response(template='latest_elearning_courses_snippet.basic_snippet', qcontext=values)
#         return response.render()
#         # return product.list_price

# =================================================================================================================

from odoo import http


class YourHomeCities(http.Controller):

    @http.route("/latest_courses", auth="public", type="json", methods=['POST'])
    def all_cities(self):
        print('sssssssss')
        latest_course = http.request.env['slide.channel'].search_read([], ['name', 'image_1920', 'id'], order='create_date desc', limit=3)
        # print('s',latest_course)
        return latest_course

    # @http.route('/cities/<model("slide.channel")>', auth="public", type="json", methods=['POST'])
    # def get_events(self):
    @http.route("/latest_courses/<int:latest_course>", type="http", auth="public", website=True)
    def create_meeting_room(self, latest_course, **post):
        print('latest_course', latest_course)
        latest_course_new = http.request.env['slide.channel'].browse(latest_course)
        print('latest_course_new', latest_course_new)
        # return latest_course_new
        return http.request.render('website_slides.courses_main')

