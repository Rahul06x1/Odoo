{
    'name': 'Latest Elearning Courses',
    'version': '16.0.1.0.2',
    'sequence': 1,
    'summary': 'Latest Elearning Courses',
    'description': "",
    'depends': [
        'base', 'website', 'website_slides'
        ],
    'data': [
            # 'views/latest_elearning_courses_snippet.xml',
            'snippets/latest_elearning_courses.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            'latest_elearning_courses_snippet/static/src/js/latest_elearning_courses_snippet.js',
            'latest_elearning_courses_snippet/static/src/css/style.css',
        ],
    },

    'installable': True,
    'application': True,
    'auto_install': False
}
