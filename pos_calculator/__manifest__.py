{
    'name': 'POS Calculator',
    'version': '16.0.1.0.0',
    'sequence': 1,
    'summary': 'POS Calculator',
    'description': "",
    'depends': [
        'base', 'point_of_sale'
        ],
    'data': [
            'views/res_config_settings.xml'
    ],
    'assets': {

        'point_of_sale.assets': [

            'pos_calculator/static/src/js/CalculatorNumberBuffer.js',
            'pos_calculator/static/src/js/pos_calculator.js',
            'pos_calculator/static/src/js/pos_calculator_popup.js',
            'pos_calculator/static/src/xml/pos_calculator.xml',
            'pos_calculator/static/src/xml/pos_calculator_popup.xml',

        ],
    },

    'installable': True,
    'application': True,
    'auto_install': False
}
