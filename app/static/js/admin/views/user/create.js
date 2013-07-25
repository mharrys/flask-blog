define(
    [
        "marionette",
        "models/user",
        "tpl!templates/user/create.tpl"
    ],
    function(
        Marionette,
        UserModel,
        UserCreateTemplate
    ) {
    UserCreateView = Marionette.ItemView.extend({
        template: UserCreateTemplate,
        events: {
            "submit": "createUser"
        },
        ui: {
            success: ".text-success",
            error: ".text-error",
            name: "#name",
            password: "#password"
        },
        createUser: function( e ) {
            e.preventDefault();

            this.ui.success.text( "" );
            this.ui.error.text( "" );

            var name = this.ui.name.val();
            var password = this.ui.password.val();

            if ( !name || !password ) {
                this.ui.error.text( "Enter name and password." );
                return;
            }

            var user = new UserModel({
                name: name,
                password: password
            });

            var self = this;
            this.collection.create( user, {
                wait: true,
                success: function() {
                    self.ui.name.val( "" );
                    self.ui.password.val( "" );
                    self.ui.error.text( "" );
                    self.ui.success.text( "Succsesfully created user." );
                },
                error: function( model, xhr ) {
                    self.ui.error.text( xhr.responseJSON.message );
                }
            });
        }
    });

    return UserCreateView;
});
