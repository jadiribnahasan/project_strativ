{
    'name': 'Project Extension - Strativ',
    'version': '1.0',
    'summary': 'Odoo project addon customization',
    'description': 'Customizations for the Odoo project addon.',
    'author': 'Jadir Ibna Hasan',
    'category': 'Project',
    'depends': ['base', 'project'],
    'data': [

        'security/ir.model.access.csv',
        'security/project_record_rule.xml',

        'views/view_project_team.xml',
        'views/view_project_inherit.xml',
        'views/dashboard_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'project_ext/static/src/css/dashboard.css',
            'project_ext/static/src/js/dashboard.js',
            'project_ext/static/src/js/lib/Chart.bundle.js',
            'project_ext/static/src/xml/dashboard.xml'
        ],
    },
    'installable': True,
    'application': True,
}
