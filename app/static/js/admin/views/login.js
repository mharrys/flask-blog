define(
    [
        "backbone",
        "marionette",
        "tpl!templates/login.tpl"
    ],
    function(
        Backbone,
        Marionette,
        LoginTemplate
    ) {
    LoginView = Marionette.ItemView.extend({
        template: LoginTemplate,
        ui: {
            error: ".text-error",
            username: "#username",
            password: "#password"
        },
        events: {
            "submit": "loginUser"
        },
        loginUser: function( e ) {
            e.preventDefault();

            var username = this.ui.username.val();
            var password = this.ui.password.val();

            if ( !username || !password ) {
                this.ui.error.text( "Enter username and password." );
                return;
            }

            var self = this;
            var result = this.model.login( username, password );
            result.done(function() {
                self.ui.username.val( "" );
                self.ui.password.val( "" );
                self.ui.error.text( "" );
                self.trigger( "authorized" );
            });
            result.fail(function() {
                self.ui.error.text( "Wrong username or password." );
            });

        }
    });

    return LoginView;
});
