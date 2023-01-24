import json
import io
from odoo import fields, models
from odoo.exceptions import ValidationError
from odoo.tools import date_utils

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class AdvanceStockMoveReportWizard(models.TransientModel):
    _name = 'advance.stock.move.report.wizard'

    date_from = fields.Date("Start Date")
    date_to = fields.Date("End Date")
    product_id = fields.Many2one('product.template', string='Product')
    location_id = fields.Many2one('stock.location', string='Location Type')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('assigned', 'Ready'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string="Status")

    def print_pdf_report(self):
        print('location', self.location_id.usage)
        if bool(self.date_from) == True and bool(self.date_to) == True and self.date_from > self.date_to:
            raise ValidationError('Start Date must be less than End Date')
        query = """SELECT date, reference, product_id as p_id, product_template.name ::jsonb->> 'en_US' as p_name, 
                    sl.complete_name as from, sdl.complete_name as to, sdl.usage as usage,
                    state as status FROM stock_move sm
                    inner join product_template on sm.product_id = product_template.id
                    inner join stock_location sl on sm.location_id = sl.id
                    inner join stock_location sdl on sm.location_dest_id = sdl.id order by usage"""

        if self.product_id:
            query += """ and product_template.id = %d""" % self.product_id.id
        if self.location_id:
            query += """ and sdl.id = %d""" % self.location_id.id
        if self.state:
            print(self.state)
            query += """ and sm.state = '%s'""" % self.state
        if self.date_from:
            query += """ and date >= '%s'""" % self.date_from
        if self.date_to:
            query += """ and date <= '%s'""" % self.date_to

        self.env.cr.execute(query)
        stock_move_data = self.env.cr.dictfetchall()
        print('self.read()[0]', self.read()[0])
        print('stock_move_data', stock_move_data)

        data = {
            'form_data': self.read()[0],
            'stock_move_data': stock_move_data,
        }
        return self.env.ref('stock_advance_stock_move_report.advance_stock_move_pdf_report_action').report_action(self,
                                                                                                                  data=data)

    def print_xlsx(self):
        if bool(self.date_from) == True and bool(self.date_to) == True and self.date_from > self.date_to:
            raise ValidationError('Start Date must be less than End Date')
        query = """SELECT date, reference, product_id as p_id, product_template.name ::jsonb->> 'en_US' as p_name, 
                            sl.complete_name as from, sdl.complete_name as to, sdl.usage as usage,
                            state as status FROM stock_move sm
                            inner join product_template on sm.product_id = product_template.id
                            inner join stock_location sl on sm.location_id = sl.id
                            inner join stock_location sdl on sm.location_dest_id = sdl.id order by usage"""

        if self.product_id:
            query += """ and product_template.id = %d""" % self.product_id.id
        if self.location_id:
            query += """ and sdl.id = %d""" % self.location_id.id
        if self.state:
            print(self.state)
            query += """ and sm.state = '%s'""" % self.state
        if self.date_from:
            query += """ and date >= '%s'""" % self.date_from
        if self.date_to:
            query += """ and date <= '%s'""" % self.date_to
        self.env.cr.execute(query)
        stock_move_data = self.env.cr.dictfetchall()
        data = {
            'form_data': self.read()[0],
            'stock_move_data': stock_move_data
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'advance.stock.move.report.wizard',
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
        sheet.merge_range('B2:I3', 'STOCK MOVE REPORT', head)
        if data['form_data']['date_from']:
            sheet.write('B6', 'From:', cell_format)
            sheet.merge_range('C6:D6', data['form_data']['date_from'], txt)
        if data['form_data']['date_to']:
            sheet.write('F6', 'To:', cell_format)
            sheet.merge_range('G6:H6', data['form_data']['date_to'], txt)
        # if data['form_data']['product_id']:
        #     sheet.write('J6', 'Product:', cell_format)
        #     sheet.merge_range('K6:L6', data['form_data']['product_id'], txt)

        row = 8
        col = 3
        sheet.write(row, col, 'DATE', bold)
        sheet.write(row, col + 3, 'REFERENCE', bold)
        sheet.write(row, col + 6, 'PRODUCT', bold)
        sheet.write(row, col + 9, 'FROM', bold)
        sheet.write(row, col + 13, 'TO', bold)
        if not (data['form_data']['state']):
            sheet.write(row, col + 16, 'STATUS', bold)

        heading_customer = False
        heading_internal = False
        for stock_move_data in data['stock_move_data']:
            row += 1
            if stock_move_data["usage"] == 'customer':
                if not heading_customer:
                    sheet.write(row+1, col, 'Customer', bold)
                    heading_customer = True
                sheet.write(row+2, col, stock_move_data["date"])
                sheet.write(row+2, col + 3, stock_move_data["reference"])
                sheet.write(row+2, col + 6, stock_move_data["p_name"])
                sheet.write(row+2, col + 9, stock_move_data["from"])
                sheet.write(row+2, col + 13, stock_move_data["to"])
                if not (data['form_data']['state']):
                    sheet.write(row+2, col + 16, stock_move_data["status"])
            row += 1
            if stock_move_data["usage"] == 'internal':
                if not heading_internal:
                    sheet.write(row+1, col, 'Internal', bold)
                    heading_internal = True
                sheet.write(row+2, col, stock_move_data["date"])
                sheet.write(row+2, col + 3, stock_move_data["reference"])
                sheet.write(row+2, col + 6, stock_move_data["p_name"])
                sheet.write(row+2, col + 9, stock_move_data["from"])
                sheet.write(row+2, col + 13, stock_move_data["to"])
                if not (data['form_data']['state']):
                    sheet.write(row+2, col + 16, stock_move_data["status"])

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
