define(
    [
        "marionette",
        "tpl!templates/navbar.tpl"
    ],
    function(
        Marionette,
        NavbarTemplate
    ) {
    NavbarView = Marionette.ItemView.extend({
        template: NavbarTemplate
    });

    return NavbarView;
});
