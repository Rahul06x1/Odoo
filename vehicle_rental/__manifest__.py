{
    'name': 'Vehicle Rental',
    'version': '16.0.1.0.2',
    'sequence': -21,
    'summary': 'Rent Vehicles',
    'description': "",
    'depends': [
        'base', 'fleet', 'account', 'sale', 'website'
        ],
    'data': [
            'security/vehicle_rental_security_group.xml',
            'security/ir.model.access.csv',

            'wizard/vehicle_rental_report_wizard.xml',

            'reports/vehicle_rental_report_template.xml',
            'reports/vehicle_rental_report.xml',

            'views/vehicle_rental_property_views.xml',
            'views/vehicle_rental_website_form.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'vehicle_rental/static/src/js/action_manager.js',
        ],
        'web.assets_frontend': [
            'vehicle_rental/static/src/js/vehicle_rental_website.js',
        ]
    },

    'installable': True,
    'application': True,
    'auto_install': False
}
