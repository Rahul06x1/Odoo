from odoo import models, fields


class VehicleRentalReportWizard(models.TransientModel):
    _name = 'vehicle.rental.report.wizard'

    date_from = fields.Date("Date From")
    date_to = fields.Date("Date To")
    vehicle_id = fields.Many2one('vehicle.rental.property', 'Vehicle')

    # def print_sample_report(self):
    #
    #     data = {
    #         'model_id': self.id,
    #         'to_date': self.to_date,
    #         'from_date': self.from_date,
    #         'vehicle_id': self.vehicle_id.id,
    #         # 'vehicle_name': self.vehicle_id
    #     }
    #     # print(self.vehicle_id[])
    #     # docids = self.env['purchase.order'].search([]).ids
    #     return self.env.ref('vehicle_rental.action_report_vehicle_order').report_action(self, data=data)

    # def print_sample_report(self):
    #     print("self.env.cr.dbname",self.env.cr.dbname)
    #     rent_request_data = self.env['rent.request'].search_read()
    #     # vehicle_data = self.env['rent.request'].search([])
    #
    #     # print("self.read()[0]", self.read()[0])
    #     # for rec in rent_request_data:
    #         # print("111",rec)
    #     # print('rent_request_data', rent_request_data)
    #     data = {
    #         'form_data': self.read()[0],
    #         'rent_request_data': rent_request_data
    #     }
    #     return self.env.ref('vehicle_rental.action_report_vehicle_order').report_action(self, data=data)

    def print_sample_report(self):
        print("self.env.cr.dbname", self.env.cr.dbname)
        query = """SELECT * FROM public.rent_request"""
        self.env.cr.execute(query)
        print(self.env.cr.fetchall())
        rent_request_data = self.env.cr.dictfetchall()
        print(rent_request_data)


        # rent_request_data = self.env['rent.request'].search_read()
        # vehicle_data = self.env['rent.request'].search([])

        data = {
            'form_data': self.read()[0],
            'rent_request_data': rent_request_data
        }
        return self.env.ref('vehicle_rental.action_report_vehicle_order').report_action(self, data=data)
