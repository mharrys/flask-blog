define(
    [
        "backbone",
        "marionette",
        "api",
        "app",
        "models/auth",
        "views/login",
        "views/navbar"
    ],
    function(
        Backbone,
        Marionette,
        API,
        App,
        AuthModel,
        LoginView
    ) {
    AuthController = Marionette.Controller.extend({
        initialize: function() {
            App.currentUser = new AuthModel();
        },
        showLogin: function() {
            var loginView = new LoginView({
                model: App.currentUser
            });
            this.listenTo( loginView, "authorized", this.onAuthorized );
            App.contentRegion.show( loginView );
        },
        showLogout: function() {
            App.currentUser.logout();
            App.navigationRegion.close();
            Backbone.history.navigate( "login", { trigger: true } );
        },
        hasAuthorization: function() {
            return App.currentUser.isLoggedIn();
        },
        onAuthorized: function() {
            Backbone.history.navigate( "dashboard", { trigger: true } );
            App.navigationRegion.show ( new NavbarView() );
        }
    });

    return AuthController;
});

