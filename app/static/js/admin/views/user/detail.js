define(
    [
        "marionette",
        "tpl!templates/user/detail.tpl"
    ],
    function(
        Marionette,
        UserDetailTemplate
    ) {
    DetailView = Marionette.ItemView.extend({
        template: UserDetailTemplate
    });

    return DetailView;
});
