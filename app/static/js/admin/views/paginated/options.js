define(
    [
        "marionette",
        "tpl!templates/paginated/options.tpl"
    ],
    function(
        Marionette,
        PaginatedOptionsTemplate
    ) {
    PaginatedOptionsView = Marionette.ItemView.extend({
        template: PaginatedOptionsTemplate,
        ui: {
            perPage: "#perPage",
            orderBy: "#orderBy",
            search: "#search"
        },
        events: {
            "change #perPage": "updatePerPage",
            "change #orderBy": "updateOrderBy",
            "keyup #search": "updateSearchFilter"
        },
        serializeData: function() {
            var options = {
                "orderingOptions": this.collection.serializeOrderingOptions()
            }
            return options;
        },
        onRender: function() {
            this.ui.perPage.val( this.collection.perPage );
            this.ui.orderBy.val( this.collection.orderBy );
            this.ui.search.val( this.collection.query );
        },
        updatePerPage: function( e ) {
            e.preventDefault();
            this.collection.updatePerPage( this.ui.perPage.val() );
        },
        updateOrderBy: function( e ) {
            e.preventDefault();
            this.collection.updateOrderBy( this.ui.orderBy.val() );
        },
        updateSearchFilter: function( e ) {
            e.preventDefault();
            this.collection.updateSearchFilter( this.ui.search.val() );
        }
    });

    return PaginatedOptionsView;
});
