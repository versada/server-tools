odoo.define('sentry_js.web_client', function (require) {
    'use strict';

    var WebClient = require('web.WebClient');

    WebClient.include({
        //We install Raven after Odoo installs it's own window.onerror handler,
        //otherwise ours (traceKitWindowOnError) is simply overwritten.
        bind_events: function() {
            this._super();
            var sentry_configured = Boolean(odoo.sentry_config);
            if (sentry_configured) {
                Raven.config(odoo.sentry_config.dsn, {
                    tags: {
                        database: odoo.session_info.db
                    }
                }).install();
                Raven.setUserContext({
                    email: odoo.sentry_config.user.email,
                    id: odoo.session_info.uid
                });
            }
        }
    });

    return WebClient;
});
