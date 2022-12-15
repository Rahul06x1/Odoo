# from odoo import models, api
#
#
# class VehicleReport(models.AbstractModel):
#     _name = 'report.vehicle_rental.report_vehicle_order'
#
#     @api.model
#     def _get_report_values(self, docids, data=None):
#         print("hhhh", data)
#         docs = self.env['rent.request'].search([])
#         print("ppp", docs)
#         return {
#             'vehicle': docs
#         }
