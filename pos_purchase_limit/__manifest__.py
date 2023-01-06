{
    'name': 'POS Purchase Limit',
    'version': '16.0.1.0.0',
    'sequence': 1,
    'summary': 'POS Purchase Limit',
    'description': "",
    'depends': [
        'base', "contacts", 'point_of_sale'
        ],
    'data': [
        'views/purchase_limit.xml',

    ],
    'assets': {
        'point_of_sale.assets': [
            'pos_purchase_limit/static/src/js/check_customer.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False
}
