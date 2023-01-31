{
    'name': 'Sales Dashboard',
    'version': '16.0.1.0.0',
    'sequence': -50,
    'summary': 'Sales Dashboard',
    'description': "",
    'depends': [
        'base', 'sale_management', 'point_of_sale'
        ],
    'data': [

        'views/sale_dashboard.xml',

    ],
    'assets': {
        'web.assets_backend': [
            'sale_dashboard/static/src/js/sale_dashboard.js',
            'sale_dashboard/static/src/xml/sale_dashboard.xml',
            'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.bundle.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False
}