{
    'name': 'vehicle rental',
    'version': '16.0.1.0.2',
    # 'category': 'Sales/CRM',
    'sequence': 5,
    'summary': 'Rent Vehicles',
    'description': "",
    # 'website': 'https://www.odoo.com/page/crm',
    'depends': [
        'base','fleet','account','sale'
        ],
    'data' : [
            'security/vehicle_rental_security_group.xml',
            'security/ir.model.access.csv',
             'views/vehicle_rental_property_views.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}