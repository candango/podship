steal("jquery", "can", "can/model", "can/view/stache", "./post_form", function($, can) {

    var StreamPostModel = can.Model.extend({
        create : "POST /account/login"
    },{});

    can.Component.extend({
        tag: "stream-post",
        template: can.view("/static/js/views/stream/post_form.stache"),
        viewModel:{
            error: false,
            postContainerFocus: false,
            errorMessage: '',
            userNameError: false,
            passwordError: false,
            blurTimeout: null,
            stream_post: new StreamPostModel(),
            blurControls: function() {
                var viewModel = this;
                var doBlur = function() {
                    viewModel.attr("postContainerFocus", false);
                }
                this.blurTimeout = window.setTimeout(doBlur, 100);
            },
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
            "#controlsContainer mouseover": function() {
                clearTimeout(this.viewModel.blurTimeout);
                this.viewModel.attr("postContainerFocus", true);
            },

            "#cancelButton click": function() {
                this.viewModel.blurControls();
            },
            "#postForm focusin": function() {
                clearTimeout(this.viewModel.blurTimeout);
                this.viewModel.attr("postContainerFocus", true);
            },
            "#postForm focusout": function() {
                console.debug($("#postContainer"));
                this.viewModel.blurControls();
            }
        }
    });

});
