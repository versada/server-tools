# -*- coding: utf-8 -*-
# Copyright 2017 Versada UAB
# License AGPL-3 or later (https://www.gnu.org/licenses/agpl).

import urlparse


def dsn_remove_secret_key(dsn):
    '''
    Returns the DSN with the secret key part removed.

    This is needed for client-side (publicly visible) Sentry integrations,
    eg. with raven-js.
    '''
    result = urlparse.urlsplit(dsn)
    return result._replace(
        netloc='{0.username}@{0.hostname}{port}'.format(
            result,
            port='' if result.port is None else ':%d' % result.port),
    ).geturl()
