define(
    [
        "jquery",
        "backbone",
        "marionette",
    ],
    function(
        $,
        Backbone,
        Marionette
    ) {
    var App = new Marionette.Application();

    App.addRegions({
        navigationRegion: "#navigation",
        contentRegion: "#content"
    });

    App.addInitializer(function() {
        $.ajaxSetup({
            statusCode: {
                401: function() {
                    Backbone.history.navigate( "login" , { trigger: true } );
                },
                403: function() {
                    alert( "403 Forbidden!" );
                }
            }
        });
    });

    App.on( "initialize:after", function() {
        if ( Backbone.history ) {
            Backbone.history.start();
            // Authorization required for every new application instance.
            Backbone.history.navigate( "login" , { trigger: true } );
        }
    });

    return App;
});
