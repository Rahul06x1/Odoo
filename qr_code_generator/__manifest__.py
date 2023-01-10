{
    'name': 'QR Code Generator',
    'version': '16.0.1.0.0',
    'sequence': -1,
    'summary': 'QR Code Generator',
    'description': "",
    'depends': [
        'base', "sale_management"
        ],
    'data': [
            'security/ir.model.access.csv',
            'reports/qr_code_pdf_template.xml',
            'reports/qr_code_pdf.xml',
            'wizard/wizard.xml',
    ],
    'assets': {
        'web.assets_backend': {
            '/qr_code_generator/static/src/xml/systray.xml',
            '/qr_code_generator/static/src/js/systray.js',
        },
    },
    'installable': True,
    'application': True,
    'auto_install': False
}
