{
    'name': 'project_strativ',
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
    ],
    'installable': True,
    'application': True,
}