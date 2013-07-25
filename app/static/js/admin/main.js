require.config({
    paths: {
        jquery: "libs/jquery",
        underscore: "libs/underscore",
        tpl: "libs/tpl",
        backbone: "libs/backbone",
        marionette: "libs/backbone.marionette",
        basicauth: "libs/backbone.basicauth",
        moment: "libs/moment"
    },
    shim: {
        jquery: {
            exports: "jQuery"
        },
        underscore: {
            exports: "_"
        },
        backbone: {
            deps: [ "jquery", "underscore" ],
            exports: "Backbone"
        },
        marionette: {
            deps: [ "backbone" ],
            exports: "Marionette"
        },
        basicauth: {
            deps: [ "backbone" ],
            exports: "Backbone.BasicAuth"
        }
    }
});

require( [ "app", "router", "moment" ], function( App ) {
    App.start();
});
