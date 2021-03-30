# -*- coding: utf-8 -*-
# Copyright (C) 2018 Akretion
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models
from datetime import timedelta, datetime


class MailMessage(models.Model):
    _name = "mail.message"
    _inherit = ["mail.message", "autovacuum.mixin"]
    _autovacuum_relation = 'message_ids'

    @api.multi
    def _get_autovacuum_domain(self, rule):
        domain = super(MailMessage, self)._get_autovacuum_domain(rule)
        today = datetime.now()
        limit_date = today - timedelta(days=rule.retention_time)
        domain += [('date', '<', fields.Datetime.to_string(limit_date))]
        if rule.message_type != 'all':
            domain += [('message_type', '=', rule.message_type)]
        if rule.model_ids:
            models = rule.model_ids.mapped('model')
            domain += [('model', 'in', models)]
        subtype_ids = rule.message_subtype_ids.ids
        if subtype_ids and rule.empty_subtype:
            domain = [
                '|', ('subtype_id', 'in', subtype_ids),
                ('subtype_id', '=', False)]
        elif subtype_ids and not rule.empty_subtype:
            domain += [('subtype_id', 'in', subtype_ids)]
        elif not subtype_ids and not rule.empty_subtype:
            domain += [('subtype_id', '!=', False)]
        return domain
