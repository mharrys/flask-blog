define(
    [
        "marionette",
        "tpl!templates/post/form.tpl"
    ],
    function(
        Marionette,
        PostFormTemplate
    ) {
    PostFormView = Marionette.ItemView.extend({
        template: PostFormTemplate,
        events: {
            "submit": "onSubmit"
        },
        ui: {
            success: ".text-success",
            error: ".text-error",
            title: "#title",
            markup: "#markup",
            visible: "#visible",
            button: "button"
        },
        initialize: function( options ) {
            this.buttonText = options.buttonText;
        },
        onRender: function() {
            this.ui.button.html( this.buttonText );
        },
        onSubmit: function() {
            this.ui.success.text( "" );
            this.ui.error.text( "" );
        },
        clear: function() {
            this.ui.success.text( "" );
            this.ui.error.text( "" );
            this.ui.title.val( "" );
            this.ui.markup.val( "" );
            this.ui.visible.attr( "checked", false );
        },
        setSuccess: function( text ) {
            this.ui.success.text( text );
        },
        setError: function( text ) {
            this.ui.error.text( text );
        },
        getTitle: function() {
            return this.ui.title.val();
        },
        getMarkup: function() {
            return this.ui.markup.val();
        },
        getVisible: function() {
            return this.ui.visible.prop( "checked" );
        }
    });

    return PostFormView;
});
