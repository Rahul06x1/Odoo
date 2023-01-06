{
    'name': 'POS Product Owner',
    'version': '16.0.1.0.0',
    'sequence': 1,
    'summary': 'POS Product Owner',
    'description': "",
    'depends': [
        'base', 'product', "contacts", 'point_of_sale'
        ],
    'data': [
        'views/product_owner.xml',

    ],
    'assets': {
        'point_of_sale.assets': [
            'pos_product_owner/static/src/js/pos_product_owner_receipt.js',
            'pos_product_owner/static/src/xml/pos_product_owner.xml',
            'pos_product_owner/static/src/xml/pos_product_owner_receipt.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False
}
