define(
    [
        "marionette",
        "tpl!templates/paginated/pages.tpl"
    ],
    function(
        Marionette,
        PaginatedPagesTemplate
    ) {
    PaginatedPagesView = Marionette.ItemView.extend({
        template: PaginatedPagesTemplate,
        events: {
            "click a.prev": "gotoPrevPage",
            "click a.page": "gotoPage",
            "click a.next": "gotoNextPage"
        },
        collectionEvents: {
            "reset": "render"
        },
        serializeData: function() {
            return this.collection.serializePaginationState();
        },
        gotoNextPage: function( e ) {
            e.preventDefault();
            this.collection.fetchNextPage();
        },
        gotoPage: function( e ) {
            e.preventDefault();
            var page = $( e.target ).text();
            this.collection.fetchPage( page );
        },
        gotoPrevPage: function( e ) {
            e.preventDefault();
            this.collection.fetchPrevPage();
        }
    });

    return PaginatedPagesView;
});

