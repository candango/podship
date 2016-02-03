steal("jquery", "can", "can/model", "can/view/stache", "./post_form", function($, can) {

    var StreamPostModel = can.Model.extend({
        create : "POST /account/login"
    },{});

    can.Component.extend({
        tag: "stream-post",
        template: can.view("/static/js/views/stream/post_form.stache"),
        viewModel:{
            error: false,
            errorMessage: '',
            userNameError: false,
            passwordError: false,
            stream_post: new StreamPostModel(),
            processLogin: function(login) {
                window.location = login.next_url;
            },
            processLoginError: function(response) {
                var errorMessage = '';
                if(response.responseJSON.errors.hasOwnProperty('username')) {
                    this.viewModel.attr('userNameError', true);
                }
                if(response.responseJSON.errors.hasOwnProperty('password')) {
                    this.viewModel.attr('passwordError', true);
                }
                var errors = new can.Map(response.responseJSON.errors);
                errors.each(
                    function(element, index, list) {
                        if(!this.viewModel.attr('error')){
                            this.viewModel.attr('error', true);
                        }
                        errorMessage += element[0] + '<br>';
                    }.bind(this)
                );
                this.viewModel.attr('errorMessage', errorMessage);
            }
        },
        events: {
            "#login_button click": function() {
                this.viewModel.attr('error', false);
                this.viewModel.attr('errorMessage', '');
                this.viewModel.attr('userNameError', false);
                this.viewModel.attr('passwordError', false);
                var form = this.element.find( 'form' );
                var values = can.deparam(form.serialize());
                var parameters = [];
                //values._xsrf = getCookie('_xsrf');
                this.viewModel.login.attr(values).save(
                    this.viewModel.processLogin.bind(this),
                    this.viewModel.processLoginError.bind(this)
                );
            }
        }
    });

});