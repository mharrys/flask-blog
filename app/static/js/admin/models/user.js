define(
    [
        "backbone"
    ],
    function(
        Backbone
    ) {
    // The UserModel represents a user resource.
    UserModel = Backbone.Model.extend({
        defaults: {
            "id": null,
            "name": null
        }
    });

    return UserModel;
});
