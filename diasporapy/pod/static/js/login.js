steal("jquery", "can", "can/model", "can/view/stache", function($, can) {
    var LoginModel = can.Model.extend({
        create : "POST /account/login"
    },{});

    can.Component.extend({
        tag: "pod-login",
        template: can.view("/static/js/views/login_form.stache"),
        viewModel:{
            error: false,
            errorMessage: '',
            userNameError: false,
            passwordError: false,
            login: new LoginModel()
        },
        events: {
            "#login_button click": function() {
                $('#form_login').data('component', this);
                this.viewModel.attr('error', false);
                this.viewModel.attr('errorMessage', '');
                this.viewModel.attr('userNameError', false);
                this.viewModel.attr('passwordError', false);
                var form = this.element.find( 'form' );
                var values = can.deparam(form.serialize());
                var parameters = [];
                //values._xsrf = getCookie('_xsrf');
                this.viewModel.login.attr(values).save(
                    function(login, data) {
                        window.location = login.next_url;
                    },
                    function(response) {
                        var component = $('#form_login').data('component');
                        $('#form_login').removeData('component');
                        var errorMessage = '';
                        if(response.responseJSON.errors.hasOwnProperty('username')) {
                            component.viewModel.attr('userNameError', true);
                        }
                        if(response.responseJSON.errors.hasOwnProperty('password')) {
                            component.viewModel.attr('passwordError', true);
                        }
                        var errors = new can.Map(response.responseJSON.errors);
                        errors.each(
                            function(element, index, list) {
                                if(!component.viewModel.attr('error')) {
                                    component.viewModel.attr('error', true);
                                }
                                errorMessage += element[0] + '<br>';
                            }
                        );
                        component.viewModel.attr('errorMessage', errorMessage);
                    }
                );
            }
        }
    });

    $("#podLogin").html(can.stache("<pod-login></pod-login>")());
});
