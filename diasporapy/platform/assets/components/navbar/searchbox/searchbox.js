steal("jquery", "can", "can/util/fixture",
    "components/navbar/searchbox/searchbox.stache",
    function($, can, fixture, template) {

    can.fixture({
        "POST /contact/search": "/assets/fixtures/search/results.json",
        "DELETE /tasks/{id}": function() {
            return {};
        }
    });

    var SearchboxModel = can.Model.extend({
        findAll : "POST /contact/search"
    },{});

    can.Component.extend({
        tag: "nav-search-box",
        template: template,
        viewModel:{
            error: false,
            retults: [],
            noContacts: false,
            hasResults: false,
            isLoading: true,
            search: function() {
                SearchboxModel.findAll(
                    {}, function( response ){
                        this.attr('hasResults', true);
                        this.attr('results', response[0].results);
                        console.debug(this);
                        this.attr('isLoading', false);
                    }.bind(this)
                );
            }
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
                    this.viewModel.search();
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
