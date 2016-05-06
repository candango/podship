steal("jquery", "can", "components/navbar/searchbox/searchbox.stache",
    function($, can, template) {
    var SearchboxModel = can.Model.extend({
        create : "POST /user/login"
    },{});
    can.Component.extend({
        tag: "nav-search-box",
        template: template,
        search: SearchboxModel(),
        viewModel:{
            error: false,
            errorMessage: '',
            userNameError: false,
            passwordError: false,

        },
        events: {
            "#searchComponent focus": function() {
                console.debug("Focused on the search Component!");
            },
            "#searchComponent blur": function() {
                console.debug("Out of the search Component!");
            }
        }
    });
    $("#navbarSearchbox").html(
        can.stache("<nav-search-box></nav-search-box>")());
});