steal("jquery", "can", "components/navbar/navbar.stache", function($, can, template) {
    var NavbarModel = can.Model.extend({
        create : "POST /user/login"
    },{});
    can.Component.extend({
        tag: "app-navbar",
        template: template,
        viewModel:{
            error: false,
            errorMessage: '',
            userNameError: false,
            passwordError: false,

        }
    });
    $("#mainNavbar").html(can.view("appNavbar", {}));
});