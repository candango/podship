System.config({
    paths: {
        "vendor/bootstrap/css/*.css": "/assets/bootstrap/css/*.css",
        "static/css/*.css": "/static/css/*.css",
        "can/*": "/vendor/canjs/steal/can/*.js",
        bootstrap: "/vendor/bootstrap/dist/js/bootstrap.js",
        i18next: "/vendor/i18next/i18next.js",
        "i18next/*": "/vendor/i18next/*",
        jquery: "/vendor/jquery/dist/jquery.js",
        "jquery/*": "/vendor/jquery/dist/*.js",
        "stylesheets/*.less": "/assets/stylesheets/*.less"
    },
    ext: {
        stache: 'can/view/stache/system'
    }
});
