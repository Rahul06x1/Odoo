{
    'name': 'Inventory Repair',
    'version': '16.0.1.0.0',
    'sequence': -3,
    'summary': 'Inventory Repair',
    'description': "",
    'depends': [
        'base', 'sale_management', 'stock'
        ],
    'data': [
        'security/ir.model.access.csv',

        'views/inventory_repair.xml',
        'views/sale_order_inherit.xml'

    ],
    'installable': True,
    'application': True,
    'auto_install': False
}