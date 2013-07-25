define(
    [
        "marionette",
        "views/post/form",
        "tpl!templates/post/edit.tpl"
    ],
    function(
        Marionette,
        PostFormView,
        PostEditTemplate
    ) {
    PostEditLayout = Marionette.Layout.extend({
        template: PostEditTemplate,
        regions: {
            formRegion: "#formRegion"
        },
        events: {
            "submit": "editPost"
        },
        onRender: function() {
            var postFormView = new PostFormView({
                model: this.model,
                buttonText: "Update Post"
            });
            this.listenTo( postFormView, "submit" );
            this.formRegion.show( postFormView );
        },
        editPost: function( e ) {
            e.preventDefault();

            var formView = this.formRegion.currentView;

            var title = formView.getTitle();
            var markup = formView.getMarkup();
            var visible = formView.getVisible();

            if ( !title || !markup ) {
                formView.setError( "Enter title and markup." );
                return;
            }

            var updates = {
                "markup": markup,
                "visible": visible
            }
            // only update title when actually changed or else the server will
            // reject it as "title already exist"
            if ( title !== this.model.get( "title" ) ) {
                updates[ "title" ] = title;
            }

            this.model.save( updates, {
                patch: true,
                success: function() {
                    formView.setSuccess( "Successfully updated post." );
                },
                error: function( model, xhr ) {
                    formView.setError( xhr.responseJSON.message );
                }
            });
        }
    });

    return PostEditLayout;
});
