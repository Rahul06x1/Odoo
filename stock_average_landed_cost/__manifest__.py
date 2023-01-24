{
    'name': 'Average Landed Cost',
    'version': '16.0.1.0.0',
    'sequence': -1,
    'summary': 'Average Landed Cost',
    'description': "",
    'depends': [
        'base', 'sale_management', 'stock', 'stock_landed_costs'
        ],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_average_landed_cost.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False
}