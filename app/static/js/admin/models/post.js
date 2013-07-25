define(
    [
        "backbone"
    ],
    function(
        Backbone
    ) {
    // The PostModel represents a blog post resource.
    PostModel = Backbone.Model.extend({
        defaults: {
            "id": null,
            "title": null,
            "markup": null,
            "author_id": null,
            "visible": false
        }
    });

    return PostModel;
});
