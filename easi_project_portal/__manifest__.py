# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Easicoders Project Portal',
    'version': '1.0',
    'category': 'Services/Project',
    'summary': '',
    'description': """
    """,
    'depends': [
        'hr_timesheet'
    ],
    'data': [
        'views/project_views.xml',
        'views/hr_timesheet_portal_templates.xml',
        'views/project_portal_templates.xml',
        'views/project_sharing_views.xml',
        'views/hr_employee_views.xml',
        'security/easi_project_portal_security.xml',
        'security/ir.model.access.csv',
        'security/ir.model.access.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'assets': {
    },
    'license': 'LGPL-3',
}
