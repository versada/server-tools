odoo.define('sentry_user_feedback.crash_manager', function (require) {
    'use strict';

    var core = require('web.core'),
        CrashManager = require('web.CrashManager');

    CrashManager.include({
        get_last_sentry_event_id: function(error) {
            return error.data.sentry_event_id || Raven.lastEventId();
        },
        should_ask_user_feedback: function(error) {
            /* Only show the user feedback dialog if:
               - For backend errors - only if it is an unexpected exception (not ValidationError, UserError, etc.);
               - raven-js is setup;
               - We have a Sentry event ID;
               - The user is not in debug mode;
            */
            var is_backend_error = Boolean(error.data.sentry_event_id),
                sentry_event_id = is_backend_error ? error.data.sentry_event_id : Raven.lastEventId(),
                raven_enabled = Raven && Raven.isSetup(),
                need_user_feedback = sentry_event_id && raven_enabled && !core.debug;
            return is_backend_error ? need_user_feedback && error.data.exception_type === 'internal_error' : need_user_feedback;
        },
        show_user_feedback_dialog: function(error) {
            Raven.showReportDialog({
                eventId: this.get_last_sentry_event_id(error),
                user: odoo.sentry_config.user
            });
        },
        show_error: function(error) {
            if (!this.active) {
                return;
            }

            if (this.should_ask_user_feedback(error)) {
                this.show_user_feedback_dialog(error);
            } else {
                this._super(error);
            }
        }
    });

});
