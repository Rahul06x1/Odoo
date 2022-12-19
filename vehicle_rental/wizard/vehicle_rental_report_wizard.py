# from odoo import models, fields
# import json
# from odoo.tools import date_utils
import time
import json
import datetime
import io
from odoo import fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools import date_utils

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


# --------------------------------------------------------------------------------------------------
class VehicleRentalReportWizard(models.TransientModel):
    _name = 'vehicle.rental.report.wizard'

    date_from = fields.Date("Date From")
    date_to = fields.Date("Date To")
    vehicle_id = fields.Many2one('vehicle.rental.property', 'Vehicle')

    def print_xlsx(self):
        # if self.date_from > self.date_to:
        #     raise ValidationError('Start Date must be less than End Date')

        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'vehicle_id': self.vehicle_id

        }
        print('data',data)
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'vehicle.rental.report.wizard',
                     'options': json.dumps(data, default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        print('ssssssssssssssss')
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format({'font_size': '12px'})
        head = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px'})
        sheet.merge_range('B2:I3', 'EXCEL REPORT', head)
        sheet.write('B6', 'From:', cell_format)
        sheet.merge_range('C6:D6', data['date_from'], txt)
        print( data['date_from'],'sssssssssss1aaaaaaaaaaaa')
        sheet.write('F6', 'To:', cell_format)
        sheet.merge_range('G6:H6', data['date_to'], txt)
        print(data['date_to'], 'sssssssssss2aaaaaaaaaaaaa')
        sheet.write('J6', 'Vehicle:', cell_format)
        sheet.merge_range('K6:L6', data['vehicle_id'], txt)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

    # ---------------------------------------------------------------------

    def print_pdf_report(self):
        print("self.env.cr.dbname", self.env.cr.dbname)

        query = """select fleet_vehicle.name as v_name,res_partner.name as c_name,rent_request.period,rent_request.request_state from rent_request
        inner join vehicle_rental_property on rent_request.vehicle = vehicle_rental_property.id
        inner join res_partner on rent_request.customer_name = res_partner.id
        inner join fleet_vehicle on vehicle_rental_property.vehicle = fleet_vehicle.id"""

        if self.vehicle_id:
            query += """ where fleet_vehicle.id = %d""" % self.vehicle_id.vehicle.id
        if self.date_from:
            query += """ and from_date > '%s'""" % self.date_from
        if self.date_to:
            query += """ and from_date < '%s'""" % self.date_to
        self.env.cr.execute(query)

        rent_request_data = self.env.cr.dictfetchall()

        data = {
            'form_data': self.read()[0],
            'rent_request_data': rent_request_data
        }
        return self.env.ref('vehicle_rental.action_report_vehicle_order').report_action(self, data=data)

    # def print_xlsx_report(self):
    #     data = {
    #         'form_data': self.read()[0]
    #     }
    #     return {'type': 'ir.actions.report', 'report_type': 'XLSX',
    #             'data': {'model': 'vehicle.rental.report.wizard', 'output_format': 'XLSX',
    #                      'options': json.dumps(data, default=date_utils.json_default),
    #                      'report_name': 'Excel Report Name',
    #                      }, }
