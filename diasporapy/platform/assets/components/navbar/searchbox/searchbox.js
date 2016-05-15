steal("jquery", "can", "components/navbar/searchbox/searchbox.stache",
    function($, can, template) {
    var SearchboxModel = can.Model.extend({
        findAll : "POST /contact/search"
    },{});
    can.Component.extend({
        tag: "nav-search-box",
        template: template,
        viewModel:{
            search: SearchboxModel(),
            error: false,
            noContacts: false,
            hasContacts: false,
            isLoading: true
        },
        events: {
            "#searchComponent focus": function() {
                console.debug(this);
                if($("#searchQuery").val().length > 2){
                    $("#searchDropdown").addClass("open");
                }
                steal.dev.log("Focused on the search Component!");
            },
            "#searchComponent blur": function() {
                steal.dev.log("Out of the search Component!");
            },
            "#searchComponent click.bs.dropdown": function(searchComponent,
                                                           event) {
                if($("#searchQuery").val().length < 3) {
                    $("#searchDropdown").removeClass("open");
                    event.stopPropagation();
                }
                else{
                    event.stopPropagation();
                    $("#searchDropdown").addClass("open");
                }
            },
            "#searchQuery keyup": function(searchQuery, event) {
                if(searchQuery.val().length > 2) {
                    $("#searchDropdown").addClass("open");
                    this.viewModel.isLoading = true;
                    steal.dev.log("The search query size is bigger than 2. " +
                        "Showing the dropdwon.");
                }
                else{
                    $("#searchDropdown").removeClass("open");
                    steal.dev.log("The search query size is smaller than 3. " +
                        "Not showing the dropdwon.");
                }
            }
        }
    });
    $("#navbarSearchbox").html(
        can.stache("<nav-search-box></nav-search-box>")()
    );
});
