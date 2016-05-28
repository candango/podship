/**
 * Copyright 2015-2016 Flavio Garcia
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

steal("jquery", "can", "can/util/fixture", "can/event",
    "components/navbar/searchbox/searchbox.stache",
    function($, can, can_fixture, can_event, template) {
    can.fixture({
        "POST /contact/search": function() {
            return "/assets/fixtures/search/results.json";
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
                        this.attr('isLoading', false);
                    }.bind(this)
                );
            }
        },
        events: {

            "#searchComponent focus": function(searchComponent, event) {
                if($("#searchQuery").val().length > 2) {
                    can.event.trigger($("#searchQuery"), "keyup");
                }
                steal.dev.log("Focused on the search Component!");
            },
            "#searchComponent blur": function() {
                steal.dev.log("Out of the search Component!");
            },
            "#searchComponent click.bs.dropdown": function(searchComponent,
                                                           event) {
                if($("#searchQuery").val().length > 2) {
                    if($("#searchDropdown").hasClass("open")){
                        $("#searchDropdown").toggleClass("open");
                        steal.dev.log("The search query size is bigger than " +
                            "2. Showing the dropdwon.");
                    }
                }
                else {
                    if(!$("#searchDropdown").hasClass("open")){
                        $("#searchDropdown").toggleClass("open");
                        steal.dev.log("The search query size is smaller " +
                            "than 3. Not showing the dropdwon.");
                    }
                }
            },
            "#searchQuery keyup": function(searchQuery, event) {
                if(searchQuery.val().length > 2) {
                    $("#searchDropdown").addClass("open");
                    this.viewModel.isLoading = true;
                    this.viewModel.search();
                    steal.dev.log("The search query size is bigger than " +
                        "2. Showing the dropdwon.");
                }
                else{
                    $("#searchDropdown").removeClass("open");
                    steal.dev.log("The search query size is smaller than 3. " +
                        "Not showing the dropdwon.");
                }
            }
        }
    });
});
