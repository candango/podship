AdminLoginModel = can.Model({
    create : "POST /account/login"
},{});

var AdminLoginApp = can.Control.extend({
    defaults: {
        view:'/static/js/views/login_form.stache'
    }
},{
   init: function() {
       this.loginModel = new AdminLoginModel();
       this.element.html(can.view(this.options.view));
       $('#errorMessagePanel').hide();
    },
    '.authentication click' : function() {
        var form = this.element.find( 'form' );
        var values = can.deparam(form.serialize());

        $('#errorMessagePanel').hide();
        $('#errorMessagePanel').html('aa');
        $('#userNameFormGroup').removeClass('has-error');
        $('#passwordFormGroup').removeClass('has-error');

        var parameters = [];
        //values._xsrf = getCookie('_xsrf');
        this.loginModel.attr(values).save(
            function(login) {
                window.location = login.next_url;
            },
            function(response) {
                var errorMessage = '';
                if(response.responseJSON.errors.hasOwnProperty('username')) {
                    $('#userNameFormGroup').addClass('has-error');
                }
                if(response.responseJSON.errors.hasOwnProperty('password')) {
                    $('#passwordFormGroup').addClass('has-error');
                }
                var errors = new can.Map(response.responseJSON.errors);

                errors.each(
                    function(element, index, list) {
                        console.debug(element, index, list);
                        var source = new can.Map(list[index]);
                        var keys = can.Map.keys(source);
                        errorMessage += source.attr(keys[0]) + '<br>';
                    }
                );
                $('#errorMessagePanel').show();
                $('#errorMessagePanel').html(errorMessage);
            }
        );
    }
});

$(function(){
    new AdminLoginApp('.login');
});
