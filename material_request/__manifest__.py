{
    'name': 'Material Request',
    'version': '16.0.1.0.2',
    'sequence': 3,
    'summary': 'Material Request',
    'description': "",
    'depends': [
        'base', 'hr', "purchase", "stock"
        ],
    'data': [
        'security/material_request_security_group.xml',
        'security/ir.model.access.csv',

        'views/material_request.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False
}