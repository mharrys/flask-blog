define(
    [
        "marionette",
        "tpl!templates/dashboard.tpl"
    ],
    function(
        Marionette,
        DashboardTemplate
    ) {
    DashboardView = Marionette.ItemView.extend({
        template: DashboardTemplate
    });

    return DashboardView;
});
