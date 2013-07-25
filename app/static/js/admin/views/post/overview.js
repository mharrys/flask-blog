define(
    [
        "marionette",
        "views/post/list",
        "tpl!templates/post/overview.tpl"
    ],
    function(
        Marionette,
        PostListView,
        PostOverviewTemplate
    ) {
    PostOverviewLayout = Marionette.Layout.extend({
        template: PostOverviewTemplate,
        regions: {
            postListRegion: "#postListRegion"
        },
        onRender: function() {
            var postListView = new PostListView({
                collection: this.collection
            });
            this.postListRegion.show( postListView );
        }
    });

    return PostOverviewLayout;
});
