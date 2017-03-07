# -*- coding: utf-8 -*-
# Copyright 2016-2017 Versada <https://versada.eu/>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import urlparse

from odoo import http, models
from odoo.tools import config as odoo_config


def dsn_remove_secret_key(dsn):
    '''
    Returns the DSN with the secret key part removed.

    This is needed for client-side (publicly visible) Sentry integrations,
    eg. with raven-js.
    '''
    result = urlparse.urlsplit(dsn)
    return result._replace(
        netloc='{0.username}@{0.hostname}'.format(result),
    ).geturl()


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def webclient_rendering_context(self):
        res = super(IrHttp, self).webclient_rendering_context()
        user = http.request.env.user
        dsn = odoo_config.get('sentry_dsn')
        res.update({
            'sentry_data': {
                'dsn': dsn_remove_secret_key(dsn) if dsn else '',
                'user': {
                    'name': user.display_name,
                    'email': user.email,
                },
            }
        })
        return res
