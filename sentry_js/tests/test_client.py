# -*- coding: utf-8 -*-
# Copyright 2017 Versada UAB
# License AGPL-3 or later (https://www.gnu.org/licenses/agpl).

import contextlib
import copy

import odoo


@contextlib.contextmanager
def mutate_config(config):
    '''Context manager which restores original Odoo config state on exit.'''
    _old_options = copy.deepcopy(config.options)
    _old_misc = copy.deepcopy(config.misc)
    yield config
    config.options = _old_options
    config.misc = _old_misc


def setup_with_context_manager(testcase, cm):
    '''
    Use a contextmanager to setUp a test case.

    Recipe by Ned Batchelder: goo.gl/RnDX4Q
    '''
    val = cm.__enter__()
    testcase.addCleanup(cm.__exit__, None, None, None)
    return val


class TestClient(odoo.tests.common.HttpCase):

    def setUp(self):
        super(TestClient, self).setUp()
        self.config = setup_with_context_manager(
            self, mutate_config(odoo.tools.config))
        self.dsn = 'https://test_dsn@example.com/1'
        self.config['sentry_dsn'] = self.dsn
        self.authenticate('admin', 'admin')

    def test_webclient_sentry_config_is_set(self):
        self.config['sentry_enabled'] = True
        html = self.url_open('/web').read()
        self.assertIn('sentry_config', html)
        self.assertIn(self.dsn, html)

    def test_sentry_disabled_webclient_sentry_config_is_not_set(self):
        self.config['sentry_enabled'] = False
        html = self.url_open('/web').read()
        self.assertNotIn('sentry_config', html)
        self.assertNotIn(self.dsn, html)
