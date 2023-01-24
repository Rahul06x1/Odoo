{
    'name': 'Quiz - Idle Timer',
    'version': '16.0.1.0.0',
    'sequence': -2,
    'summary': 'Quiz - Idle Timer',
    'description': "",
    'depends': [
            'base', 'survey'
        ],
    'data': [
        'views/survey_survey.xml',
        'static/src/xml/survey_templates_inherit.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            'quiz_idle_timer/static/src/js/quiz_idle_timer.js',
            # 'quiz_idle_timer/static/src/xml/survey_templates_inherit.xml'
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False
}
