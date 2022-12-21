import json
import io
from odoo import fields, models
from odoo.exceptions import ValidationError
from odoo.tools import date_utils

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class VehicleRentalReportWizard(models.TransientModel):
    _name = 'vehicle.rental.report.wizard'

    date_from = fields.Date("Date From")
    date_to = fields.Date("Date To")
    vehicle_id = fields.Many2one('vehicle.rental.property', 'Vehicle')

    def print_xlsx(self):
        if bool(self.date_from) == True and bool(self.date_to) == True and self.date_from > self.date_to:
            raise ValidationError('Start Date must be less than End Date')
        query = """select fleet_vehicle.name as v_name,res_partner.name as c_name,rent_request.period,rent_request.request_state from rent_request
        inner join vehicle_rental_property on rent_request.vehicle = vehicle_rental_property.id
        inner join res_partner on rent_request.customer_name = res_partner.id
        inner join fleet_vehicle on vehicle_rental_property.vehicle = fleet_vehicle.id"""

        if self.vehicle_id:
            query += """ where fleet_vehicle.id = %d""" % self.vehicle_id.vehicle.id
        if self.date_from:
            query += """ and from_date >= '%s'""" % self.date_from
        if self.date_to:
            query += """ and to_date >= '%s'""" % self.date_to
        self.env.cr.execute(query)
        rent_request_data = self.env.cr.dictfetchall()
        data = {
            'form_data': self.read()[0],
            'rent_request_data': rent_request_data
        }
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
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})
        cell_format = workbook.add_format({'font_size': '12px'})
        head = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px'})
        sheet.merge_range('B2:I3', 'VEHICLE RENTAL REPORT', head)
        if data['form_data']['date_from']:
            sheet.write('B6', 'From:', cell_format)
            sheet.merge_range('C6:D6', data['form_data']['date_from'], txt)
        if data['form_data']['date_to']:
            sheet.write('F6', 'To:', cell_format)
            sheet.merge_range('G6:H6', data['form_data']['date_to'], txt)
        if data['form_data']['vehicle_id']:
            sheet.write('J6', 'Vehicle:', cell_format)
            sheet.merge_range('K6:L6', data['form_data']['vehicle_id'][1], txt)

        row = 8
        col = 3
        sheet.write(row, col, 'Vehicle', bold)
        sheet.write(row, col + 1, 'Customer', bold)
        sheet.write(row, col + 2, 'Period', bold)
        sheet.write(row, col + 3, 'State', bold)

        for rent_request_data in data['rent_request_data']:
            row += 1
            sheet.write(row, col, rent_request_data["v_name"])
            sheet.write(row, col + 1, rent_request_data["c_name"])
            sheet.write(row, col + 2, rent_request_data["period"])
            sheet.write(row, col + 3, rent_request_data["request_state"])

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

    def print_pdf_report(self):
        if bool(self.date_from) == True and bool(self.date_to) == True and self.date_from > self.date_to:
            raise ValidationError('Start Date must be less than End Date')

        query = """select fleet_vehicle.name as v_name,res_partner.name as c_name,rent_request.period,rent_request.request_state from rent_request
        inner join vehicle_rental_property on rent_request.vehicle = vehicle_rental_property.id
        inner join res_partner on rent_request.customer_name = res_partner.id
        inner join fleet_vehicle on vehicle_rental_property.vehicle = fleet_vehicle.id"""

        if self.vehicle_id:
            query += """ where fleet_vehicle.id = %d""" % self.vehicle_id.vehicle.id
        if self.date_from:
            query += """ and from_date >= '%s'""" % self.date_from
        if self.date_to:
            query += """ and to_date >= '%s'""" % self.date_to

        self.env.cr.execute(query)
        rent_request_data = self.env.cr.dictfetchall()

        data = {
            'form_data': self.read()[0],
            'rent_request_data': rent_request_data
        }
        return self.env.ref('vehicle_rental.action_report_vehicle_order').report_action(self, data=data)
