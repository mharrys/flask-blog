define(
    [
        "marionette",
        "app",
        "controllers/auth",
        "controllers/post",
        "controllers/user",
        "views/dashboard"
    ],
    function(
        Marionette,
        App,
        AuthController,
        PostController,
        UserController,
        DashboardView
    ) {
    var Router = Marionette.AppRouter.extend({
        routes: {
            "login": "showLogin",
            "logout": "showLogout",
            "dashboard": "showDashboard",
            "posts": "showPosts",
            "posts/create": "showCreatePost",
            "posts/:id": "showEditPost",
            "users": "showUsers",
            "users/:id": "showUser",
            "profile": "showProfile"
        },
        initialize: function() {
            this.authController = new AuthController();
            this.postController = new PostController();
            this.userController = new UserController();
        },
        requireAuthorization: function() {
            if ( this.authController.hasAuthorization() ) {
                return false;
            } else {
                Backbone.history.navigate( "login", { trigger: true } );
                return true;
            }
        },
        showLogin: function() {
            this.authController.showLogin();
        },
        showLogout: function() {
            if ( !this.requireAuthorization() ) {
                this.authController.showLogout();
                this.postController.reset();
                this.userController.reset();
            }
        },
        showDashboard: function() {
            if ( !this.requireAuthorization() ) {
                App.contentRegion.show( new DashboardView() );
            }
        },
        showPosts: function() {
            if ( !this.requireAuthorization() ) {
                this.postController.showPosts();
            }
        },
        showCreatePost: function() {
            if ( !this.requireAuthorization() ) {
                this.postController.showCreatePost();
            }
        },
        showEditPost: function( id ) {
            if ( !this.requireAuthorization() ) {
                this.postController.showEditPost( id );
            }
        },
        showUsers: function() {
            if ( !this.requireAuthorization() ) {
                this.userController.showUsers();
            }
        },
        showUser: function( id ) {
            if ( !this.requireAuthorization() ) {
                this.userController.showUser( id );
            }
        },
        showProfile: function() {
            if ( !this.requireAuthorization() ) {
                this.userController.showProfile();
            }
        }
    });

    App.addInitializer(function() {
        var router = new Router();
    });
});
