# -*- coding: utf-8 -*-
# Copyright 2017 Versada UAB
# License AGPL-3 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Sentry JS',
    'version': '10.0.1.0.0',
    'author': 'Versada,Odoo Community Association (OCA)',
    'category': 'Extra Tools',
    'website': 'https://versada.eu',
    'license': 'AGPL-3',
    'summary': 'Client-side Odoo errors in Sentry',
    'depends': [
        'sentry',
        'web',
    ],
    'data': [
        'views/templates.xml',
    ],
    'installable': True,
    'application': False,
}
