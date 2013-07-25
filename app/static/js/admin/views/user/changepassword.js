define(
    [
        "marionette",
        "tpl!templates/user/changepassword.tpl"
    ],
    function(
        Marionette,
        ChangePasswordTemplate
    ) {
    ChangePasswordView = Marionette.ItemView.extend({
        template: ChangePasswordTemplate,
        events: {
            "submit": "changePassword"
        },
        ui: {
            success: ".text-success",
            error: ".text-error",
            newPassword: "#newPassword",
            confirmPassword: "#confirmPassword",
            password: "#password"
        },
        changePassword: function( e ) {
            e.preventDefault();

            this.ui.error.text( "" );
            this.ui.success.text( "" );

            var newPassword = this.ui.newPassword.val();
            var confirmPassword = this.ui.confirmPassword.val();
            var password = this.ui.password.val();

            if ( !newPassword || !confirmPassword || !password ) {
                this.ui.error.text( "Enter passwords." );
                return;
            }
            if ( newPassword !== confirmPassword ) {
                this.ui.error.text( "Passwords must match." );
                return;
            }
            if ( !this.model.comparePassword( password ) ) {
                this.ui.error.text( "Wrong password." );
                return;
            }

            var self = this;
            this.model.save({ "password": newPassword }, {
                patch: true,
                success: function() {
                    self.model.changePassword( newPassword );
                    self.ui.newPassword.val( "" );
                    self.ui.confirmPassword.val( "" );
                    self.ui.password.val( "" );
                    self.ui.error.text( "" );
                    self.ui.success.text( "Successfully changed password." );
                },
                error: function( model, xhr ) {
                    self.ui.error.text( xhr.responseJSON.message );
                }
            });
        }
    });

    return ChangePasswordView;
});
