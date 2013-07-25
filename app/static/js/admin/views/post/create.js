define(
    [
        "marionette",
        "models/post",
        "views/post/form",
        "tpl!templates/post/create.tpl"
    ],
    function(
        Marionette,
        PostModel,
        PostFormView,
        PostCreateTemplate
    ) {
    PostCreateLayout = Marionette.Layout.extend({
        template: PostCreateTemplate,
        regions: {
            formRegion: "#formRegion"
        },
        events: {
            "submit": "createPost"
        },
        onRender: function() {
            var postFormView = new PostFormView({
                model: new PostModel(), // dummy model
                buttonText: "Create Post"
            });
            this.listenTo( postFormView, "submit" );
            this.formRegion.show( postFormView );
        },
        createPost: function( e ) {
            e.preventDefault();

            var formView = this.formRegion.currentView;

            var title = formView.getTitle();
            var markup = formView.getMarkup();
            var visible = formView.getVisible();

            if ( !title || !markup ) {
                formView.setError( "Enter title and markup." );
                return;
            }

            var post = new PostModel({
                title: title,
                markup: markup,
                visible: visible,
                author_id: this.model.get( "id" )
            });

            this.collection.create( post, {
                wait: true,
                success: function() {
                    formView.clear();
                    formView.setSuccess( "Successfully created post." );
                },
                error: function( model, xhr ) {
                    formView.setError( xhr.responseJSON.message );
                }
            });
        }
    });

    return PostCreateLayout;
});
