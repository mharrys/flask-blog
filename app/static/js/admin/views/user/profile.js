define(
    [
        "marionette",
        "views/user/changeusername",
        "views/user/changepassword",
        "tpl!templates/user/profile.tpl"
    ],
    function(
        Marionette,
        ChangeUsernameView,
        ChangePasswordView,
        UserProfileTemplate
    ) {
    UserProfileLayout = Marionette.Layout.extend({
        template: UserProfileTemplate,
        regions: {
            changeUsernameRegion: "#changeUsernameRegion",
            changePasswordRegion: "#changePasswordRegion"
        },
        onRender: function() {
            var changeUsernameView = new ChangeUsernameView({
                model: this.model
            });
            var changePasswordView = new ChangePasswordView({
                model: this.model
            });
            this.changeUsernameRegion.show( changeUsernameView );
            this.changePasswordRegion.show( changePasswordView );
        }
    });

    return UserProfileLayout;
});
