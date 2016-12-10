
function navigatePageWithUrlParameters(page){
	'use strict';
    var previous_search_query = $('#previous_search_query').val();
    if (previous_search_query) {
    window.location.href = window.location.pathname +'?search='+previous_search_query+'&page='+page;
    }
    else {
	window.location.href = window.location.pathname +'?page='+page;
	}
}