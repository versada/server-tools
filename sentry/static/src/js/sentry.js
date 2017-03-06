odoo.define('sentry.sentry_user_feedback', function (require) {
    'use strict';

    var core = require('web.core'),
        CrashManager = require('web.CrashManager');

    var replace_crashmanager = function() {
        CrashManager.include({
            show_error: function(error) {
                if (!this.active) {
                    return;
                }
                var sentry_event_id = error.data.sentry_event_id;

                if (sentry_event_id && !core.debug) {
                    Raven.showReportDialog({
                        eventId: error.data.sentry_event_id,
                        user: odoo.sentry_data.user,
                    });
                } else {
                    this._super(error);
                }
            },
        });
    };

    replace_crashmanager();
});
