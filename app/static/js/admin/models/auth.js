define(
    [
        "backbone",
        "basicauth",
        "api",
        "models/user"
    ],
    function(
        Backbone,
        BasicAuth,
        API,
        UserModel
    ) {
    // The AuthModel is used for storing and handling the authorization
    // state. When successfully authorized the AuthModel can be used as a
    // resource for currently logged in user.
    AuthModel = UserModel.extend({
        url: function() {
            // When in logged out state the requests should always be for the
            // authorization API. However, when in logged in state, all
            // requests should be for the users API.
            if ( this.loggedIn ) {
                return API.users + "/" + this.get( "id" );
            } else {
                return API.auth;
            }
        },
        initialize: function() {
            this.logout();
        },
        // Return server response callback for the attempt to login with
        // specified username and password.
        login: function( username, password ) {
            BasicAuth.set( username, password );

            var self = this;
            return this.fetch({
                success: function() {
                    self.loggedIn = true;
                    self.username = username;
                    self.password = password;
                },
                error: function() {
                    self.logout();
                }
            });
        },
        // Reset model and global authorization header making all further
        // authorization requests invalid.
        logout: function() {
            BasicAuth.clear();

            this.clear();
            this.loggedIn = false;
            this.username = null;
            this.password = null;
        },
        // Change authorization username if logged in.
        changeUsername: function( username ) {
            if ( this.isLoggedIn ) {
                BasicAuth.set( username, this.password );
            }
        },
        // Change authorization password if logged in.
        changePassword: function( password ) {
            if ( this.isLoggedIn ) {
                BasicAuth.set( this.username, password );
            }
        },
        // Compare specified password with current used password.
        comparePassword: function( password ) {
            return ( this.password === password );
        },
        // Return true if this model has been successfully verified by the
        // server.
        isLoggedIn: function() {
            return this.loggedIn;
        }
    });

    return AuthModel;
});
