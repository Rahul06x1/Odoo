# -*- coding: utf-8 -*-

from odoo import models, api


class SaleDashboard(models.Model):
    _inherit = 'sale.order'

    @api.model
    def get_sale_order_state(self, option):
        if option == 'draft':
            query = '''select res_partner.name as customer,count(sale_order.id) as no_of_sale_order from sale_order 
                        inner join res_partner on res_partner.id = sale_order.partner_id WHERE state='draft' GROUP BY 
                        res_partner.name ORDER BY no_of_sale_order DESC;'''
            label = 'DRAFT'
        elif option == 'sent':
            query = '''select res_partner.name as customer,count(sale_order.id) as no_of_sale_order from sale_order 
            inner join res_partner on res_partner.id = sale_order.partner_id WHERE state='sent' GROUP BY 
            res_partner.name ORDER BY no_of_sale_order DESC;'''
            label = 'SENT'
        else:
            query = '''select res_partner.name as customer,count(sale_order.id) as no_of_sale_order from sale_order 
                        inner join res_partner on res_partner.id = sale_order.partner_id WHERE state='sale' GROUP BY 
                        res_partner.name ORDER BY no_of_sale_order DESC;'''
            label = 'SALE'
        self._cr.execute(query)
        docs = self._cr.dictfetchall()
        customer = []
        for record in docs:
            customer.append(record.get('customer'))
        no_of_sale_order = []
        for record in docs:
            no_of_sale_order.append(record.get('no_of_sale_order'))
        final = [no_of_sale_order, customer, label]
        return final

    @api.model
    def get_invoice_state(self, option):
        if option == 'draft':
            query = '''select res_partner.name as customer,count(account_move.id) as no_of_invoice from account_move 
                        inner join res_partner on res_partner.id = account_move.partner_id WHERE state='draft' GROUP BY 
                        res_partner.name ORDER BY no_of_invoice DESC;'''
            label = 'DRAFT'
        else:
            query = '''select res_partner.name as customer,count(account_move.id) as no_of_invoice from account_move 
                        inner join res_partner on res_partner.id = account_move.partner_id WHERE state='posted' GROUP BY 
                        res_partner.name ORDER BY no_of_invoice DESC;'''
            label = 'POSTED'
        self._cr.execute(query)
        docs = self._cr.dictfetchall()
        customer = []
        for record in docs:
            customer.append(record.get('customer'))
        no_of_invoice = []
        for record in docs:
            no_of_invoice.append(record.get('no_of_invoice'))
        final = [no_of_invoice, customer, label]
        return final

    @api.model
    def get_the_top_customer(self, ):
        query = '''select res_partner.name as customer,sale_order.partner_id,
                    sum(sale_order.amount_total) as amount_total from sale_order 
                    inner join res_partner on res_partner.id = sale_order.partner_id GROUP BY sale_order.partner_id,
                    res_partner.name ORDER BY amount_total DESC LIMIT 10;'''
        self._cr.execute(query)
        docs = self._cr.dictfetchall()

        order = []
        for record in docs:
            order.append(record.get('amount_total'))
        day = []
        for record in docs:
            day.append(record.get('customer'))
        final = [order, day]
        return final

    @api.model
    def get_the_top_selling_products(self):

        query = '''select DISTINCT(product_template.name) ::jsonb->> 'en_US' as product_name,
                    sum(product_uom) as total_quantity from sale_order_line 
                    inner join product_product on product_product.id=sale_order_line.product_id inner join 
                    product_template on product_product.product_tmpl_id = product_template.id
                    group by product_template.id ORDER 
                    BY total_quantity DESC Limit 5'''

        self._cr.execute(query)
        top_selling_product = self._cr.dictfetchall()

        total_quantity = []
        for record in top_selling_product:
            total_quantity.append(record.get('total_quantity'))
        product_name = []
        for record in top_selling_product:
            product_name.append(record.get('product_name'))
        final = [total_quantity, product_name]
        return final

    @api.model
    def get_the_least_selling_products(self):

        query = '''select DISTINCT(product_template.name) ::jsonb->> 'en_US' as product_name,
                    sum(product_uom) as total_quantity from sale_order_line 
                    inner join product_product on product_product.id=sale_order_line.product_id 
                    inner join product_template on product_product.product_tmpl_id = product_template.id 
                    group by product_template.id ORDER BY total_quantity ASC Limit 5'''

        self._cr.execute(query)
        least_selling_product = self._cr.dictfetchall()

        total_quantity = []
        for record in least_selling_product:
            total_quantity.append(record.get('total_quantity'))
        product_name = []
        for record in least_selling_product:
            product_name.append(record.get('product_name'))
        final = [total_quantity, product_name]
        return final

    @api.model
    def get_the_top_selling_products(self):

        query = '''select DISTINCT(product_template.name) ::jsonb->> 'en_US' as product_name,
                        sum(product_uom) as total_quantity from sale_order_line 
                        inner join product_product on product_product.id=sale_order_line.product_id inner join 
                        product_template on product_product.product_tmpl_id = product_template.id
                        group by product_template.id ORDER 
                        BY total_quantity DESC Limit 5'''

        self._cr.execute(query)
        top_selling_product = self._cr.dictfetchall()

        total_quantity = []
        for record in top_selling_product:
            total_quantity.append(record.get('total_quantity'))
        product_name = []
        for record in top_selling_product:
            product_name.append(record.get('product_name'))
        final = [total_quantity, product_name]
        return final

    @api.model
    def get_sales_by_sales_team(self):

        query = '''select crm_team.name ::jsonb->> 'en_US' as sales_team,sum(sale_order.amount_total) as amount_total 
                    from sale_order 
                    inner join crm_team on crm_team.id = sale_order.team_id GROUP BY sale_order.team_id,
                    crm_team.name ORDER BY amount_total DESC LIMIT 10;'''

        self._cr.execute(query)
        sales_by_sales_team = self._cr.dictfetchall()

        amount_total = []
        for record in sales_by_sales_team:
            amount_total.append(record.get('amount_total'))
        sales_team = []
        for record in sales_by_sales_team:
            sales_team.append(record.get('sales_team'))
        final = [amount_total, sales_team]
        return final

    @api.model
    def get_sales_by_sales_person(self):
        query = '''select res_partner.name as salesperson,sum(sale_order.amount_total) as amount_total from sale_order
                    inner join res_users on res_users.id = sale_order.user_id
                    inner join res_partner on res_partner.id = res_users.partner_id GROUP BY 
                    res_partner.name  ORDER BY amount_total DESC LIMIT 10;'''

        self._cr.execute(query)
        sales_by_sales_person = self._cr.dictfetchall()

        amount_total = []
        for record in sales_by_sales_person:
            amount_total.append(record.get('amount_total'))
        sales_person = []
        for record in sales_by_sales_person:
            sales_person.append(record.get('salesperson'))
        final = [amount_total, sales_person]
        return final
