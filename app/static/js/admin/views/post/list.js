define(
    [
        "backbone",
        "marionette",
        "views/paginated/options",
        "views/paginated/pages",
        "views/post/edit",
        "tpl!templates/paginated/list.tpl",
        "tpl!templates/post/table.tpl",
        "tpl!templates/post/tablerow.tpl"
    ],
    function(
        Backbone,
        Marionette,
        PaginatedOptionsView,
        PaginatedPagesView,
        PostEditView,
        PaginatedListTemplate,
        PostTableTemplate,
        PostTableRowTemplate
    ) {
    PostTableRowView = Marionette.ItemView.extend({
        template: PostTableRowTemplate,
        tagName: "tr",
        events: {
            "click a.edit": "editPost",
            "click a.delete": "deletePost"
        },
        editPost: function( e ) {
            e.preventDefault();
            var url = "posts/" + this.model.id;
            Backbone.history.navigate( url, { trigger: true } );
        },
        deletePost: function( e ) {
            e.preventDefault();
            var title = this.model.get( "title" );
            var message = "Delete post \"" + title + "\"?";
            var confirmed = confirm( message );
            if ( confirmed ) {
                this.model.destroy();
            }
        }
    });

    PostTableView = Marionette.CompositeView.extend({
        template: PostTableTemplate,
        itemViewContainer: "tbody",
        itemView: PostTableRowView
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
            var tableView = new PostTableView({
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
