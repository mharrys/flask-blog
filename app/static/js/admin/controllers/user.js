define(
    [
        "marionette",
        "app",
        "collections/user",
        "views/user/detail",
        "views/user/profile",
        "views/user/overview"
    ],
    function(
        Marionette,
        App,
        UserCollection,
        UserDetailView,
        UserProfileView,
        UserOverviewView
    ) {
    UserController = Marionette.Controller.extend({
        initialize: function() {
            this.userCollection = new UserCollection();
        },
        reset: function() {
            this.userCollection.reset();
        },
        showUsers: function() {
            var userOverviewView = new UserOverviewView({
                collection: this.userCollection
            });
            App.contentRegion.show( userOverviewView );
        },
        showUser: function( id ) {
            var user = this.userCollection.get( id );
            var userDetailView = new UserDetailView({
                model: user
            });
            App.contentRegion.show( userDetailView );
        },
        showProfile: function() {
            var userProfileView = new UserProfileView({
                model: App.currentUser
            });
            App.contentRegion.show( userProfileView );
        }
    });

    return UserController;
});

