{
    'name': 'Material Request',
    'version': '16.0.1.0.2',
    'sequence': 1,
    'summary': 'Material Request',
    'description': "",
    'depends': [
        'base','hr',"purchase"
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