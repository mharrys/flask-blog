define(
    [
        "marionette",
        "tpl!templates/user/changeusername.tpl"
    ],
    function(
        Marionette,
        ChangeUsernameTemplate
    ) {
    ChangeUsernameView = Marionette.ItemView.extend({
        template: ChangeUsernameTemplate,
        events: {
            "submit": "changeUsername"
        },
        ui: {
            success: ".text-success",
            error: ".text-error",
            username: "#username",
            password: "#password"
        },
        changeUsername: function( e ) {
            e.preventDefault();

            this.ui.error.text( "" );
            this.ui.success.text( "" );

            var username = this.ui.username.val();
            var password = this.ui.password.val();

            if ( !username || !password ) {
                this.ui.error.text(
                    "Enter a new username and current password."
                );
                return;
            }
            if ( !this.model.comparePassword( password ) ) {
                this.ui.error.text( "Wrong password." );
                return;
            }

            var self = this;
            this.model.save({ "name": username }, {
                patch: true,
                success: function() {
                    self.model.changeUsername( username );
                    self.ui.username.val( "" );
                    self.ui.password.val( "" );
                    self.ui.success.text( "Successfully changed username." );
                },
                error: function( model, xhr ) {
                    self.ui.error.text( xhr.responseJSON.message );
                }
            });
        }
    });

    return ChangeUsernameView;
});
