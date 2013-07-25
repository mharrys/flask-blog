define(
    [
        "marionette",
        "app",
        "collections/post",
        "views/post/create",
        "views/post/edit",
        "views/post/overview"
    ],
    function(
        Marionette,
        App,
        PostCollection,
        PostCreateView,
        PostEditView,
        PostOverviewView
    ) {
    PostController = Marionette.Controller.extend({
        initialize: function() {
            this.postCollection = new PostCollection();
        },
        reset: function() {
            this.postCollection.reset();
        },
        showPosts: function() {
            var postOverviewView = new PostOverviewView({
                collection: this.postCollection
            });
            App.contentRegion.show( postOverviewView );
        },
        showCreatePost: function() {
            var postCreateView = new PostCreateView({
                model: App.currentUser,
                collection: this.postCollection
            });
            App.contentRegion.show( postCreateView );
        },
        showEditPost: function( id ) {
            var post = this.postCollection.get( id );
            var postEditView = new PostEditView({
                model: post
            });
            App.contentRegion.show( postEditView );
        },
    });

    return PostController;
});

