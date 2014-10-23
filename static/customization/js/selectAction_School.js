$( document ).ready(function() {

    function routeSchool(cityid) {
        console.log('city ', cityid);
        path = '/city/' + cityid + '/school';
        return window.location.href = path;
    }

//  Фильтр школ по городам

    $('#filterCityforSchool').change(function() {
        var cityid = $(this).val();
        if (typeof cityid === "undefined")
            cityid = 0;

        routeSchool(cityid);
    });

});