{
    'name': 'Tolerance',
    'version': '16.0.1.0.0',
    'sequence': 6,
    'summary': 'Tolerance',
    'description': "",
    'depends': [
        'base', "contacts", 'sale', 'stock', 'purchase'
        ],
    'data': [
        'views/tolerance.xml',

        'security/ir.model.access.csv',

        'wizard/tolerance_warning_wizard.xml'

    ],
    'installable': True,
    'application': True,
    'auto_install': False
}