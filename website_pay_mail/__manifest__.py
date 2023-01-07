{
    'name': 'Website Pay Mail',
    'version': '16.0.1.0.0',
    'sequence': 1,
    'summary': 'Website Pay Mail',
    'description': "",
    'depends': [
        'base', 'website', 'sale_management'
        ],
    'data': [
            'data/website_pay_mail_email_template.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False
}
