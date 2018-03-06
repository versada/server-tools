# -*- coding: utf-8 -*-
# Copyright 2017 Versada UAB
# License AGPL-3 or later (https://www.gnu.org/licenses/agpl).

import sys
import threading

from odoo import http
from odoo.addons.sentry import sentry_client


_patch_lock = threading.Lock()


def install_serialize_exception_wrapper():
    # Sentry not configured/disabled.
    if not sentry_client:
        return

    with _patch_lock:
        original_func = http.serialize_exception

        # Don't wrap the function repeatedly.
        if getattr(original_func, '_sentry_user_feedback_wrapped', False):
            return

        def wrapper(e):
            res = original_func(e)
            # Here we double-check if the current exception should be captured
            # by Raven. It is necessary in order to avoid a case where the
            # exception is congfigured to be ignored by Raven, so the
            # last_event_id is from an older exception - this would mean that
            # the feedback would be logged on the wrong exception.
            if sentry_client.should_capture(sys.exc_info()):
                res.update(sentry_event_id=sentry_client.last_event_id)
            return res

        http.serialize_exception = wrapper

        wrapper._sentry_user_feedback_wrapped = True
