steal("jquery", "can", "components/navbar/searchbox/searchbox.stache",
    function($, can, template) {
    var SearchboxModel = can.Model.extend({
        findAll : "POST /contact/search"
    },{});
    can.Component.extend({
        tag: "nav-search-box",
        template: template,
        search: SearchboxModel(),
        viewModel:{
            error: false,
            noContacts: false,
            hasContacts: false,
            isLoading: true
        },
        events: {
            "#searchComponent focus": function() {
                if($("#searchQuery").val().length>2){
                    $("#searchDropdown").addClass("open");
                }
                console.debug("Focused on the search Component!");
            },
            "#searchComponent blur": function() {
                console.debug("Out of the search Component!");
            },
            "#searchComponent click.bs.dropdown": function(searchComponent, event) {
                if($("#searchQuery").val().length<3) {
                    $("#searchDropdown").removeClass("open");
                    event.stopPropagation();
                }
                else{
                    event.stopPropagation();
                    $("#searchDropdown").addClass("open");
                }
            },
            "#searchQuery keyup": function(searchQuery, event) {
                if(searchQuery.val().length>2) {
                    $("#searchDropdown").addClass("open");
                }
                else{
                    $("#searchDropdown").removeClass("open");
                }
            }
        }
    });
    $("#navbarSearchbox").html(
        can.stache("<nav-search-box></nav-search-box>")());
});
