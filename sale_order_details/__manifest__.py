{
    'name': 'Sale Order Details',
    'version': '16.0.1.0.0',
    'sequence': -20,
    'summary': 'Sale Order Details',
    'description': "",
    'depends': [
        'base', 'sale_management', 'contacts'
        ],
    'data': [


        'views/sale_order_details.xml',
        'views/product_template.xml'

    ],
    'installable': True,
    'application': True,
    'auto_install': False
}