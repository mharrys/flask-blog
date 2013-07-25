define(
    [
        "api",
        "models/user",
        "collections/paginated"
    ],
    function(
        API,
        UserModel,
        PaginatedCollection
    ) {
    UserCollection = PaginatedCollection.extend({
        model: UserModel,
        url: API.users,
        extraParams: function() {
            var params = {};
            if ( this.query ) {
                params[ "name" ] = this.query;
            }
            return params;
        },
        parseData: function( response ) {
            return response.users;
        },
        serializeOrderingOptions: function() {
            return [
                { "text": "Id",        "value": "id" },
                { "text": "Id Desc",   "value": "-id" },
                { "text": "Name",      "value": "name" },
                { "text": "Name Desc", "value": "-name" }
            ];
        }
    });

    return UserCollection;
});
