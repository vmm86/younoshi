$( document ).ready(function() {

    function routeTeam(cityid, schoolid) {
        console.log('city ', cityid, 'school', schoolid);
        path = '/city/' + cityid + '/school/' + schoolid + '/team';
        return window.location.href = path;
    }

//  Фильтр школ по городам

    $('#filterCityforTeam').change(function() {
        var cityid = $(this).val();
        if (typeof cityid === "undefined")
            cityid = 0;

        var schoolid = 0;

        routeTeam(cityid, schoolid);
    });

//  Фильтр команд по школам

    $('#filterSchoolforTeam').change(function() {
        var cityid = $('#filterCityforTeam').val();
        if (typeof cityid === "undefined")
            cityid = 0;

        var schoolid = $(this).val();
        if (typeof schoolid === "undefined")
            schoolid = 0;

        routeTeam(cityid, schoolid);
    });

});