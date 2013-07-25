define(
    [
        "backbone"
    ],
    function(
        Backbone
    ) {
    // The PaginatedCollection abstracts a collection for use with paginated
    // resources.
    PaginatedCollection = Backbone.Collection.extend({
        initialize: function() {
            this.perPage = 5;
            this.orderBy = "-id";
            this.totalCount = null;
            this.resetPages();

            this.on( "add", this.fetchOnAdd);
            this.on( "destroy", this.fetchOnDestroy);
        },
        resetPages: function() {
            this.firstPage = 1;
            this.currentPage = this.firstPage;
            this.nextPage = null;
            this.prevPage = null;
            this.lastPage = null;
        },
        fetch: function( options ) {
            var params = {
                "page": this.currentPage,
                "per_page": this.perPage,
                "order_by": this.orderBy
            }
            options.data = _.extend( params, this.extraParams() );
            return Backbone.Collection.prototype.fetch.call( this, options );
        },
        parse: function( response, options ) {
            var link = options.xhr.getResponseHeader( "Link" );
            if ( link ) {
                this.parseLinkHeader( link );
            }
            this.totalCount = options.xhr.getResponseHeader( "X-Total-Count" );
            return this.parseData( response, options );
        },
        parseLinkHeader: function( link ) {
            // http://tools.ietf.org/html/rfc5988
            var linkPattern = /<(.*?)>; rel="(\w+)"/g;
            var paramPattern = /[?&](\w+)=([\w-]+)/g;

            var matchLink = "";
            var links = {};
            var pages = {};
            while ( matchLink = linkPattern.exec( link ) ) {
                var url = matchLink[ 1 ];
                var rel = matchLink[ 2 ];
                links[ rel ] = url;

                var matchParam = "";
                while ( matchParam = paramPattern.exec( url ) ) {
                    var param = matchParam[ 1 ];
                    var value = matchParam[ 2 ];
                    switch ( param ) {
                    case "page":
                        pages[ rel ] = value;
                        break;
                    }
                }
            }

            this.nextPage = pages[ "next" ];
            this.prevPage = pages[ "prev" ];
            this.lastPage = pages[ "last" ];
        },
        parseData: function( response ) {
            return response;
        },
        fetchPage: function( page ) {
            if ( page >= this.firstPage && page <= this.lastPage ) {
                this.currentPage = page;
                this.fetch({ reset: true });
            }
        },
        fetchNextPage: function() {
            if ( this.nextPage ) {
                this.currentPage = this.nextPage;
                this.fetch({ reset: true });
            }
        },
        fetchPrevPage: function() {
            if ( this.prevPage ) {
                this.currentPage = this.prevPage;
                this.fetch({ reset: true });
            }
        },
        fetchOnAdd: function() {
            this.fetchPage( this.currentPage );
        },
        fetchOnDestroy: function() {
            // Move back one page (or stay on first page) if the destruction
            // of a model causes the current page to be empty and if there is
            // no next page to replace the current page.
            if ( this.length == 0 && !this.nextPage ) {
                this.fetchPrevPage();
            } else {
                this.fetchPage( this.currentPage );
            }
        },
        updatePerPage: function( perPage ) {
            this.perPage = perPage;

            this.resetPages();
            this.fetch({ reset: true });
        },
        updateOrderBy: function( orderBy ) {
            this.orderBy = orderBy;

            this.resetPages();
            this.fetch({ reset: true });
        },
        updateSearchFilter: function( query ) {
            if ( this.query != query ) {
                this.query = query;

                this.resetPages();
                this.fetch({ reset: true });
            }
        },
        serializePaginationState: function() {
            return {
                "perPage": this.perPage,
                "orderBy": this.orderBy,
                "firstPage": this.firstPage,
                "currentPage": this.currentPage,
                "nextPage": this.nextPage,
                "prevPage": this.prevPage,
                "lastPage": this.lastPage,
                "totalCount": this.totalCount
            }
        },
        serializeOrderingOptions: function() {
            return [
                { "text": "Id",      "value": "id" },
                { "text": "Id Desc", "value": "-id" }
            ];
        }
    });

    return PaginatedCollection;
});
