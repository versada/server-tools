# -*- coding: utf-8 -*-
# Copyright 2017 Versada UAB
# License AGPL-3 or later (https://www.gnu.org/licenses/agpl).

import unittest

from ..utils import dsn_remove_secret_key


class TestUtils(unittest.TestCase):

    def test_dsn_remove_secret_key(self):
        self.assertNotIn(
            'secret_key', dsn_remove_secret_key(
                'https://<public_key>:<secret_key>@example.com/<project id>'))

    def test_dsn_remove_secret_key_supports_port(self):
        self.assertEqual(
            dsn_remove_secret_key('https://foo:bar@example.com:8080/baz'),
            'https://foo@example.com:8080/baz',
        )
