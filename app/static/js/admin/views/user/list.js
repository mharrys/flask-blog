define(
    [
        "marionette",
        "views/paginated/options",
        "views/paginated/pages",
        "tpl!templates/paginated/list.tpl",
        "tpl!templates/user/table.tpl",
        "tpl!templates/user/tablerow.tpl"
    ],
    function(
        Marionette,
        PaginatedOptionsView,
        PaginatedPagesView,
        PaginatedListTemplate,
        UserTableTemplate,
        UserTableRowTemplate
    ) {
    UserTableRowView = Marionette.ItemView.extend({
        template: UserTableRowTemplate,
        tagName: "tr",
        events: {
            "click a.detail": "viewUser",
            "click a.delete": "deleteUser"
        },
        viewUser: function( e ) {
            e.preventDefault();
            var url = "users/" + this.model.id;
            Backbone.history.navigate( url, { trigger: true } );
        },
        deleteUser: function( e ) {
            e.preventDefault();
            var name = this.model.get( "name" );
            var message = "Delete user \"" + name + "\"?";
            var confirmed = confirm( message );
            if ( confirmed ) {
                this.model.destroy();
            }
        }
    });

    UserTableView = Marionette.CompositeView.extend({
        template: UserTableTemplate,
        itemViewContainer: "tbody",
        itemView: UserTableRowView
    });

    PaginatedListLayout = Marionette.Layout.extend({
        template: PaginatedListTemplate,
        regions: {
            optionsRegion: "#optionsRegion",
            tableRegion: "#tableRegion",
            pagesRegion: "#pagesRegion"
        },
        onRender: function() {
            this.collection.fetch({ reset: true });

            var optionsView = new PaginatedOptionsView({
                collection: this.collection
            });
            var tableView = new UserTableView({
                collection: this.collection
            });
            var pagesView = new PaginatedPagesView({
                collection: this.collection
            });
            this.optionsRegion.show( optionsView );
            this.tableRegion.show( tableView );
            this.pagesRegion.show( pagesView );
        }
    });

    return PaginatedListLayout;
});
