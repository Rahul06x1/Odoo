{
    'name': 'Advance stock move report',
    'version': '16.0.1.0.0',
    'sequence': -22,
    'summary': 'Advance stock move report',
    'description': "",
    'depends': [
        'base', 'stock'
        ],
    'data': [
            'security/ir.model.access.csv',

            'wizard/advance_stock_move_report_wizard.xml',

            'reports/advance_stock_move_pdf_report_template.xml',
            'reports/advance_stock_move_report.xml',

            'views/advanced_stock_move_report_menu.xml'

    ],


    'installable': True,
    'application': True,
    'auto_install': False
}
