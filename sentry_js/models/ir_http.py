# -*- coding: utf-8 -*-
# Copyright 2017 Versada <https://versada.eu/>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import http, models
from odoo.tools import config as odoo_config

from ..utils import dsn_remove_secret_key


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def webclient_rendering_context(self):
        res = super(IrHttp, self).webclient_rendering_context()
        if odoo_config.get('sentry_enabled'):
            user = http.request.env.user
            dsn = odoo_config.get('sentry_dsn')
            res.update(sentry_config={
                'dsn': dsn_remove_secret_key(dsn) if dsn else '',
                'user': {
                    'name': user.display_name,
                    'email': user.email,
                },
            })
        return res
