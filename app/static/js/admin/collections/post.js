define(
    [
        "api",
        "models/post",
        "collections/paginated"
    ],
    function(
        API,
        PostModel,
        PaginatedCollection
    ) {
    PostCollection = PaginatedCollection.extend({
        model: PostModel,
        url: API.posts,
        extraParams: function() {
            var params = {};
            if ( this.query ) {
                params[ "title" ] = this.query;
            }
            return params;
        },
        parseData: function( response ) {
            return response.posts;
        },
        serializeOrderingOptions: function() {
            return [
                { "text": "Id",         "value": "id" },
                { "text": "Id Desc",    "value": "-id" },
                { "text": "Title",      "value": "title" },
                { "text": "Title Desc", "value": "-title" }
            ];
        }
    });

    return PostCollection;
});
