# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 GRAP (http://www.grap.coop)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from datetime import datetime

from odoo import SUPERUSER_ID, _, api, models
from odoo.exceptions import AccessDenied
from odoo.tools.safe_eval import safe_eval


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def _send_email_passkey(self, user_id):
        """ Send a email to the admin of the system and / or the user
            to inform passkey use."""
        mail_obj = self.env['mail.mail'].sudo()
        icp_obj = self.env['ir.config_parameter']

        admin_user = self.sudo().browse(SUPERUSER_ID)
        login_user = self.browse(user_id)

        send_to_admin = safe_eval(
            icp_obj.get_param('auth_admin_passkey.send_to_admin', '')
        )
        send_to_user = safe_eval(
            icp_obj.get_param('auth_admin_passkey.send_to_user', '')
        )

        mails = []
        if send_to_admin and admin_user.email:
            mails.append({'email': admin_user.email, 'lang': admin_user.lang})
        if send_to_user and login_user.email:
            mails.append({'email': login_user.email, 'lang': login_user.lang})
        for mail in mails:
            subject = _('Authentication user used')
            body = _(
                "Authentication user used to login with '%s'.\n\n"
                "\n\nTechnical information below: \n\n"
                "- Login date : %s\n\n"
            ) % (login_user.login, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            mail_obj.create({
                'email_to': mail['email'],
                'subject': subject,
                'body_html': '<pre>%s</pre>' % body
            })

    @api.model
    def _send_email_same_password(self, login):
        """ Send an email to the admin user to inform that
            another user has the same password as him."""
        mail_obj = self.env['mail.mail'].sudo()
        admin_user = self.sudo().browse(SUPERUSER_ID)

        if admin_user.email:
            mail_obj.create({
                'email_to': admin_user.email,
                'subject': _('[WARNING] Odoo Security Risk'),
                'body_html':
                    _("<pre>User with login '%s' has the same "
                      "password as the authentication user.</pre>") % login,
            })

    @api.model
    def check_credentials(self, password):
        """ Despite using @api.model decorator, this method
            is always called by a res.users record"""
        auth_user = self.env.ref('auth_user.auth_user')
        try:
            super(ResUsers, self).check_credentials(password)

            # If credentials are ok, try to log with user password as auth
            # user and send email if they are equal
            if self._uid != auth_user.id:
                try:
                    super(ResUsers, self).sudo(auth_user).check_credentials(
                        password)
                    self._send_email_same_password(self.login)
                except AccessDenied:
                    pass

        except AccessDenied:
            if self._uid in (SUPERUSER_ID, auth_user.id):
                raise

            # Just be sure that parent methods aren't wrong
            user = self.sudo().search([('id', '=', self._uid)])
            if not user:
                raise

            # Our user isn't using its own password, check if its auth one
            try:
                super(ResUsers, self).sudo(auth_user).check_credentials(
                    password)
                self._send_email_passkey(self._uid)
            except AccessDenied:
                raise
