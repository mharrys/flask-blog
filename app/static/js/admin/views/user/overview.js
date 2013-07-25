define(
    [
        "marionette",
        "views/user/create",
        "views/user/list",
        "tpl!templates/user/overview.tpl"
    ],
    function(
        Marionette,
        UserCreateView,
        UserListView,
        UserOverviewTemplate
    ) {
    UserOverviewLayout = Marionette.Layout.extend({
        template: UserOverviewTemplate,
        regions: {
            userCreateRegion: "#userCreateRegion",
            userListRegion: "#userListRegion"
        },
        onRender: function() {
            var userCreateView = new UserCreateView({
                collection: this.collection
            });
            var userListView = new UserListView({
                collection: this.collection
            });
            this.userCreateRegion.show( userCreateView );
            this.userListRegion.show( userListView );
        }
    });

    return UserOverviewLayout;
});
