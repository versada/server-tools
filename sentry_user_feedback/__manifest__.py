# -*- coding: utf-8 -*-
# Copyright 2017 Versada UAB
# License AGPL-3 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Sentry User Feedback',
    'version': '10.0.1.0.0',
    'author': 'Versada',
    'category': 'Extra Tools',
    'website': 'https://versada.eu',
    'license': 'AGPL-3',
    'summary': 'Get user feedback on errors',
    'depends': [
        'web',
        'sentry_js',
    ],
    'data': [
        'views/templates.xml',
    ],
    'post_load': 'install_serialize_exception_wrapper',
    'installable': True,
}
